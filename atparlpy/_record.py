"""Shared record model for Parliament filter API datasets."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
from typing import Any

from ._filter_api import parse_date, parse_datetime, row_to_kwargs


@dataclass(slots=True)
class ParliamentRecord:
    """Common record shape returned by the filter API."""

    gp_code: str | None = None
    ityp: str | None = None
    inr: str | None = None
    zukz: str | None = None
    datum: date | None = None
    art: str | None = None
    betreff: str | None = None
    nummer: str | None = None
    datumsort: str | None = None
    phasen_bis: str | None = None
    status: str | None = None
    doktyp: str | None = None
    zust: str | None = None
    doktyp_lang: str | None = None
    his_url: str | None = None
    rss_desc: str | None = None
    datum_von: date | None = None
    vhg: str | None = None
    vhg2: str | None = None
    lz_buttons: str | None = None
    personen: list[str] | None = None
    fraktionen: list[str] | None = None
    themen: list[str] | None = None
    sw: list[str] | None = None
    eurovoc: list[str] | None = None
    sysdate: datetime | None = None
    wentry_id: str | None = None
    inrnum: str | None = None
    nr_gp_code: str | None = None
    nrbr: str | None = None
    gruppe: str | None = None
    abstimmung_3_lesung: str | None = None
    dafuer: str | None = None
    dagegen: str | None = None
    abstimmungstext: str | None = None
    abstimmungskommentar: str | None = None

    @classmethod
    def from_api_row(cls, header: list[dict[str, Any]], row: list[Any]) -> "ParliamentRecord":
        """Build a record from one generic API row."""

        values = row_to_kwargs(
            header,
            row,
            converters={
                "datum": parse_date,
                "datum_von": parse_date,
                "sysdate": parse_datetime,
            },
        )
        return cls(**values)
