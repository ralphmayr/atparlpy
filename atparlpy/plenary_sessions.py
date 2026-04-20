"""Plenary sessions dataset wrapper."""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import date
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from ._filter_api import FilterApiDataset, build_payload, int_to_roman, parse_date, row_to_kwargs


@dataclass(slots=True)
class PlenarySession:
    """Represents a single plenary session row from the API."""

    datum: date | None = None
    sitzung: str | None = None
    tagesordnung: str | None = None
    gp_code: str | None = None
    ityp: str | None = None
    inr: str | None = None
    zukz: str | None = None
    datum_sort: str | None = None
    pfad: str | None = None
    sitzungstag: str | None = None
    link: str | None = None

    @classmethod
    def from_api_row(cls, header: list[dict[str, Any]], row: list[Any]) -> "PlenarySession":
        return cls(
            **row_to_kwargs(
                header,
                row,
                converters={
                    "datum": parse_date,
                },
            )
        )


class PlenarySessions(FilterApiDataset):
    """Wrapper for plenary sessions."""

    NR_ENDPOINT = "https://www.parlament.gv.at/Filter/api/json/post?jsMode=EVAL&FBEZ=WFP_007&listeId=11070&showAll=true"
    BR_ENDPOINT = "https://www.parlament.gv.at/Filter/api/json/post?jsMode=EVAL&FBEZ=WFP_007&listeId=11070&showAll=true"

    aliases = {
        "nrbrbv": "NRBRBV",
        "gp_code": "GP",
    }

    def __init__(
        self,
        nrbr: str | list[str] | tuple[str, ...] | None = None,
        gp: int | None = None,
        gp_code: str | list[str] | tuple[str, ...] | None = None,
    ) -> None:
        super().__init__(
            nrbrbv=nrbr or "NR",
            gp_code=gp_code if gp_code is not None else (int_to_roman(gp) if gp is not None else None),
        )

    def _normalized_nrbrbv(self) -> str:
        values = self._filters.get("nrbrbv")
        if isinstance(values, str):
            values = [values]
        elif isinstance(values, tuple):
            values = list(values)
        if not values:
            return "NR"
        if any(str(value).upper() == "BR" for value in values):
            return "BR"
        return "NR"

    @property
    def endpoint(self) -> str:
        return self.BR_ENDPOINT if self._normalized_nrbrbv() == "BR" else self.NR_ENDPOINT

    def _post(self, payload: dict[str, list[str]]) -> dict[str, Any]:
        request = Request(
            self.endpoint,
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

    def _payload(self) -> dict[str, list[str]]:
        payload = build_payload(
            {
                "nrbrbv": self._filters.get("nrbrbv"),
                "gp_code": self._filters.get("gp_code"),
            },
            self.aliases,
            {},
        )
        return payload

    def nrbrbv(self, value: str | list[str] | tuple[str, ...] | None) -> "PlenarySessions":
        return self._set_filter("nrbrbv", value or "NR")

    def gp(self, value: int | None) -> "PlenarySessions":
        if value is None:
            return self._set_filter("gp_code", None)
        return self._set_filter("gp_code", int_to_roman(value))

    def gp_code(self, value: str | list[str] | tuple[str, ...] | None) -> "PlenarySessions":
        return self._set_filter("gp_code", value)

    def AsList(self) -> list[PlenarySession]:
        """Return plenary sessions matching the configured filters."""

        data = self._post(self._payload())
        header = data.get("header", [])
        rows = data.get("rows", [])
        return [PlenarySession.from_api_row(header, row) for row in rows]
