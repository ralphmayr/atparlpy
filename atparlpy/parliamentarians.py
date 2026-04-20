"""Parliamentarians dataset wrapper."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Any

from ._filter_api import (
    FilterApiDataset,
    build_detail_url,
    build_payload,
    fetch_json_url,
    normalize_dimensions,
    parse_date,
    row_to_kwargs,
)


@dataclass(slots=True)
class Mandate:
    """Represents a single mandate entry in a person detail view."""

    funktion_text: str | None = None
    mandat: str | None = None
    klub: str | None = None
    wahlkreis: str | None = None
    wahlpartei: str | None = None
    wahlpartei_text: str | None = None
    gremium: str | None = None
    funktion: str | None = None
    bez: str | None = None
    mandat_von: date | None = None
    mandat_bis: date | None = None
    funktion_von: date | None = None
    funktion_bis: date | None = None
    aktiv: bool | None = None
    zeitraum: str | None = None

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> "Mandate":
        return cls(
            funktion_text=value.get("funktion_text"),
            mandat=value.get("mandat"),
            klub=value.get("klub"),
            wahlkreis=value.get("wahlkreis"),
            wahlpartei=value.get("wahlpartei"),
            wahlpartei_text=value.get("wahlpartei_text"),
            gremium=value.get("gremium"),
            funktion=value.get("funktion"),
            bez=value.get("bez"),
            mandat_von=parse_date(value.get("mandatVon")),
            mandat_bis=parse_date(value.get("mandatBis")),
            funktion_von=parse_date(value.get("funktion_von")),
            funktion_bis=parse_date(value.get("funktion_bis")),
            aktiv=value.get("aktiv"),
            zeitraum=value.get("zeitraum"),
        )


@dataclass(slots=True)
class Person:
    """Represents the detailed person view."""

    typ: str | None = None
    gremium: str | None = None
    pad_intern: Any = None
    aktiv: bool | None = None
    sitzplatz: str | None = None
    image: str | None = None
    mandate: list[Mandate] | None = None

    @classmethod
    def from_api_response(cls, payload: dict[str, Any]) -> "Person":
        content = payload.get("content", {})
        meta = payload.get("meta", {})
        person_info = content.get("personInfo", {})
        banner = content.get("banner", {})
        mandates = banner.get("mandate") or []
        return cls(
            typ=person_info.get("personTyp"),
            gremium=person_info.get("gremium"),
            pad_intern=person_info.get("pad_intern"),
            aktiv=person_info.get("aktiv"),
            sitzplatz=person_info.get("sitzplatz"),
            image=(meta.get("openGraph") or {}).get("image"),
            mandate=[Mandate.from_dict(item) for item in mandates],
        )


@dataclass(slots=True)
class _ParliamentarianBase:
    """Shared fields for parliamentarian records."""

    name: str | None = None
    wahlkreis: str | None = None
    bundesland: str | None = None
    pad_sortier: str | None = None
    link: str | None = None

    @classmethod
    def from_api_row(cls, header: list[dict[str, Any]], row: list[Any]) -> "_ParliamentarianBase":
        return cls(**row_to_kwargs(header, row))

    def GetDetails(self) -> Person:
        """Return the detailed person view for this parliamentarian."""

        if not self.link:
            raise ValueError(f"{self.__class__.__name__} does not expose a detail URL")
        return Person.from_api_response(fetch_json_url(build_detail_url(self.link)))


@dataclass(slots=True)
class MemberOfParliament(_ParliamentarianBase):
    """Represents an NR parliamentarian."""

    klub: str | None = None
    liste: str | None = None
    rss_description: str | None = None
    rss_pfad: str | None = None
    rss_titel: str | None = None
    sort_fr: str | None = None
    sort_wp: str | None = None


@dataclass(slots=True)
class MemberOfTheNationalCouncil(_ParliamentarianBase):
    """Represents a BR parliamentarian."""

    pad_intern: str | None = None
    fraktion: str | None = None
    wahlpartei: str | None = None


class Parliamentarians(FilterApiDataset):
    """Wrapper for the parliamentarians dataset."""

    NR_ENDPOINT = "https://www.parlament.gv.at/Filter/api/json/post?jsMode=EVAL&FBEZ=WFW_002&listeId=10002"
    BR_ENDPOINT = "https://www.parlament.gv.at/Filter/api/json/post?jsMode=EVAL&FBEZ=WFW_005&listeId=10005"
    aliases = {
        "funk": "FUNK",
        "fr": "FR",
        "wp": "WP",
        "bl": "BL",
        "wk": "WK",
    }

    def __init__(
        self,
        nrbr: str | None = None,
        gender: str | None = None,
        funk: str | list[str] | tuple[str, ...] | None = None,
        fr: str | list[str] | tuple[str, ...] | None = None,
        wp: str | list[str] | tuple[str, ...] | None = None,
        bl: str | list[str] | tuple[str, ...] | None = None,
        wk: str | list[str] | tuple[str, ...] | None = None,
    ) -> None:
        super().__init__(
            nrbr=nrbr or "NR",
            gender=gender,
            funk=funk,
            fr=fr,
            wp=wp,
            bl=bl,
            wk=wk,
        )

    def _normalize_gender(self, value: str | None) -> str | None:
        if value is None:
            return None

        normalized = value.strip().lower()
        if normalized not in {"m", "w"}:
            raise ValueError("gender must be 'm' or 'w'")
        return normalized

    def _normalized_nrbr(self) -> str:
        values = normalize_dimensions(self._filters.get("nrbr"))
        if not values:
            return "NR"
        if any(value.upper() == "BR" for value in values):
            return "BR"
        return "NR"

    @property
    def endpoint(self) -> str:
        return self.BR_ENDPOINT if self._normalized_nrbr() == "BR" else self.NR_ENDPOINT

    def _payload(self) -> dict[str, list[str]]:
        gender = self._normalize_gender(self._filters.get("gender"))
        payload = build_payload(
            {
                "funk": self._filters.get("funk"),
                "fr": self._filters.get("fr"),
                "wp": self._filters.get("wp"),
                "bl": self._filters.get("bl"),
                "wk": self._filters.get("wk"),
            },
            self.aliases,
            {},
        )
        if gender == "m":
            payload["M"] = ["M"]
            return payload
        if gender == "w":
            payload["W"] = ["W"]
            return payload
        payload["M"] = ["M"]
        payload["W"] = ["W"]
        return payload

    def nrbr(self, value: str | list[str] | tuple[str, ...] | None) -> "Parliamentarians":
        return self._set_filter("nrbr", value or "NR")

    def gender(self, value: str | None) -> "Parliamentarians":
        return self._set_filter("gender", self._normalize_gender(value))

    def funk(self, value: str | list[str] | tuple[str, ...] | None) -> "Parliamentarians":
        return self._set_filter("funk", value)

    def fr(self, value: str | list[str] | tuple[str, ...] | None) -> "Parliamentarians":
        return self._set_filter("fr", value)

    def wp(self, value: str | list[str] | tuple[str, ...] | None) -> "Parliamentarians":
        return self._set_filter("wp", value)

    def bl(self, value: str | list[str] | tuple[str, ...] | None) -> "Parliamentarians":
        return self._set_filter("bl", value)

    def wk(self, value: str | list[str] | tuple[str, ...] | None) -> "Parliamentarians":
        return self._set_filter("wk", value)

    def AsList(self) -> list[MemberOfParliament] | list[MemberOfTheNationalCouncil]:
        """Return parliamentarians matching the configured filters."""

        data = self._post(self._payload())
        header = data.get("header", [])
        rows = data.get("rows", [])

        if self._normalized_nrbr() == "BR":
            return [MemberOfTheNationalCouncil.from_api_row(header, row) for row in rows]
        return [MemberOfParliament.from_api_row(header, row) for row in rows]
