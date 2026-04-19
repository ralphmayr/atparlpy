"""Shared helpers for the Parliament filter API datasets."""

from __future__ import annotations

import json
import re
import unicodedata
from dataclasses import asdict, is_dataclass
from datetime import date, datetime
from typing import Any, Callable, Mapping
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

API_URL = "https://www.parlament.gv.at/Filter/api/filter/data/101"
API_QUERY = "?js=eval&showAll=true"
_ROMAN_NUMERALS: tuple[tuple[int, str], ...] = (
    (1000, "M"),
    (900, "CM"),
    (500, "D"),
    (400, "CD"),
    (100, "C"),
    (90, "XC"),
    (50, "L"),
    (40, "XL"),
    (10, "X"),
    (9, "IX"),
    (5, "V"),
    (4, "IV"),
    (1, "I"),
)


def slugify_label(value: str) -> str:
    """Convert an API label into a stable Python attribute name."""

    translated = (
        value.replace("ä", "ae")
        .replace("ö", "oe")
        .replace("ü", "ue")
        .replace("Ä", "Ae")
        .replace("Ö", "Oe")
        .replace("Ü", "Ue")
        .replace("ß", "ss")
    )
    normalized = unicodedata.normalize("NFKD", translated).encode("ascii", "ignore").decode("ascii")
    slug = re.sub(r"[^0-9A-Za-z]+", "_", normalized).strip("_").lower()
    return slug or "field"


def normalize_value(value: Any) -> Any:
    """Convert generic API row values into more convenient Python values."""

    if value is None:
        return None

    if isinstance(value, str):
        stripped = value.strip()
        if stripped.startswith("[") and stripped.endswith("]"):
            try:
                return json.loads(stripped)
            except json.JSONDecodeError:
                return value

    return value


def parse_date(value: Any) -> date | None:
    """Parse the API's date formats into a Python date."""

    if value is None:
        return None
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    if not isinstance(value, str):
        return None

    text = value.strip()
    for fmt in ("%d.%m.%Y", "%Y-%m-%d", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%dT%H:%M:%S.%f"):
        try:
            return datetime.strptime(text, fmt).date()
        except ValueError:
            continue

    try:
        return datetime.fromisoformat(text).date()
    except ValueError:
        return None


def parse_datetime(value: Any) -> datetime | None:
    """Parse the API's sysdate format into a Python datetime."""

    if value is None:
        return None
    if isinstance(value, datetime):
        return value
    if not isinstance(value, str):
        return None

    text = value.strip()
    for fmt in (
        "%a %b %d %H:%M:%S %Z %Y",
        "%a %b %d %H:%M:%S %Y",
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%dT%H:%M:%S.%f",
    ):
        try:
            return datetime.strptime(text, fmt)
        except ValueError:
            continue

    try:
        return datetime.fromisoformat(text)
    except ValueError:
        return None


def int_to_roman(value: int) -> str:
    """Convert a positive integer into a roman numeral."""

    if not isinstance(value, int):
        raise TypeError("gp must be an integer")
    if value <= 0:
        raise ValueError("gp must be a positive integer")

    remaining = value
    parts: list[str] = []
    for arabic, roman in _ROMAN_NUMERALS:
        while remaining >= arabic:
            parts.append(roman)
            remaining -= arabic
    return "".join(parts)


def normalize_dimensions(values: list[str] | tuple[str, ...] | str | None) -> list[str] | None:
    """Normalize user-provided dimensions to the API's list format."""

    if values is None:
        return None
    if isinstance(values, str):
        items = [item.strip() for item in values.split(",")]
    else:
        items = [item.strip() for item in values]

    return [item for item in items if item]


def build_payload(
    dimensions: Mapping[str, list[str] | tuple[str, ...] | str | None],
    aliases: Mapping[str, str],
    fixed_dimensions: Mapping[str, list[str] | tuple[str, ...] | str],
) -> dict[str, list[str]]:
    """Build the POST body expected by the filter API."""

    payload: dict[str, list[str]] = {}

    for param_name, values in dimensions.items():
        normalized = normalize_dimensions(values)
        if not normalized:
            continue
        api_key = aliases.get(param_name)
        if api_key:
            payload[api_key] = normalized

    for api_key, values in fixed_dimensions.items():
        normalized = normalize_dimensions(values)
        if normalized:
            payload[api_key] = normalized

    return payload


def row_to_kwargs(
    header: list[dict[str, Any]],
    row: list[Any],
    converters: Mapping[str, Callable[[Any], Any]] | None = None,
) -> dict[str, Any]:
    """Map a generic API row into keyword arguments for the record model."""

    converters = converters or {}
    values: dict[str, Any] = {}

    for index, header_item in enumerate(header):
        label = header_item.get("label") or header_item.get("feld_name") or f"field_{index}"
        field_name = slugify_label(str(label))
        raw_value = row[index] if index < len(row) else None
        converter = converters.get(field_name)
        values[field_name] = converter(raw_value) if converter else normalize_value(raw_value)

    return values


class FilterApiClient:
    """Small HTTP client for the Parliament filter API."""

    endpoint = API_URL
    timeout = 30

    def _post(self, payload: dict[str, list[str]]) -> dict[str, Any]:
        request = Request(
            f"{self.endpoint}{API_QUERY}",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json", "Accept": "application/json"},
            method="POST",
        )

        try:
            with urlopen(request, timeout=self.timeout) as response:
                return json.loads(response.read().decode("utf-8"))
        except HTTPError as exc:  # pragma: no cover - network failure path
            raise RuntimeError(f"{self.__class__.__name__} API returned HTTP {exc.code}") from exc
        except URLError as exc:  # pragma: no cover - network failure path
            raise RuntimeError(f"Could not reach {self.__class__.__name__} API: {exc.reason}") from exc


class FilterApiDataset(FilterApiClient):
    """Base class for stateful, chainable dataset wrappers."""

    aliases: Mapping[str, str] = {}
    fixed_dimensions: Mapping[str, list[str] | tuple[str, ...] | str] = {}

    def __init__(self, **filters: list[str] | tuple[str, ...] | str | None) -> None:
        self._filters: dict[str, list[str] | tuple[str, ...] | str | None] = {}
        for name, value in filters.items():
            self._filters[name] = value

    def _set_filter(self, name: str, value: list[str] | tuple[str, ...] | str | None) -> "FilterApiDataset":
        self._filters[name] = value
        return self

    def _payload(self) -> dict[str, list[str]]:
        return build_payload(self._filters, self.aliases, self.fixed_dimensions)

    def _list_records(self, record_cls: type[Any]) -> list[Any]:
        data = self._post(self._payload())
        header = data.get("header", [])
        rows = data.get("rows", [])
        return [record_cls.from_api_row(header, row) for row in rows]

    def AsDataFrame(self) -> Any:
        """Return the configured dataset as a Pandas DataFrame."""

        try:
            import pandas as pd
        except ImportError as exc:  # pragma: no cover - optional dependency
            raise RuntimeError("Pandas is required for AsDataFrame()") from exc

        records = self.AsList()
        rows = [asdict(record) if is_dataclass(record) else dict(record) for record in records]
        return pd.DataFrame(rows)
