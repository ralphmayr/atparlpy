"""Motions dataset wrapper."""

from __future__ import annotations

from .._filter_api import FilterApiDataset, int_to_roman
from .._record import ParliamentRecord


class Motion(ParliamentRecord):
    """Represents a single motion row from the API."""


class Motions(FilterApiDataset):
    """Wrapper for the motions dataset."""

    aliases = {
        "nrbr": "NRBR",
        "gp_code": "GP_CODE",
        "themen": "THEMEN",
        "doktyp": "DOKTYP",
        "pad_intern": "PAD_INTERN",
        "inrnum": "INRNUM",
        "sw": "SW",
        "eurovoc": "EUROVOC",
        "frak_code": "FRAK_CODE",
    }

    fixed_dimensions = {"VHG": ["ANTR"]}

    def __init__(
        self,
        gp: int | None = None,
        nrbr: list[str] | tuple[str, ...] | str | None = None,
        gp_code: list[str] | tuple[str, ...] | str | None = None,
        themen: list[str] | tuple[str, ...] | str | None = None,
        doktyp: list[str] | tuple[str, ...] | str | None = None,
        pad_intern: list[str] | tuple[str, ...] | str | None = None,
        inrnum: list[str] | tuple[str, ...] | str | None = None,
        sw: list[str] | tuple[str, ...] | str | None = None,
        eurovoc: list[str] | tuple[str, ...] | str | None = None,
        frak_code: list[str] | tuple[str, ...] | str | None = None,
        vhg: list[str] | tuple[str, ...] | str | None = None,
    ) -> None:
        super().__init__(
            gp_code=gp_code if gp_code is not None else (int_to_roman(gp) if gp is not None else None),
            nrbr=nrbr,
            themen=themen,
            doktyp=doktyp,
            pad_intern=pad_intern,
            inrnum=inrnum,
            sw=sw,
            eurovoc=eurovoc,
            frak_code=frak_code,
            vhg=vhg,
        )

    def gp(self, value: int | None) -> "Motions":
        if value is None:
            return self._set_filter("gp_code", None)
        return self._set_filter("gp_code", int_to_roman(value))

    def nrbr(self, value: list[str] | tuple[str, ...] | str | None) -> "Motions":
        return self._set_filter("nrbr", value)

    def gp_code(self, value: list[str] | tuple[str, ...] | str | None) -> "Motions":
        return self._set_filter("gp_code", value)

    def themen(self, value: list[str] | tuple[str, ...] | str | None) -> "Motions":
        return self._set_filter("themen", value)

    def doktyp(self, value: list[str] | tuple[str, ...] | str | None) -> "Motions":
        return self._set_filter("doktyp", value)

    def pad_intern(self, value: list[str] | tuple[str, ...] | str | None) -> "Motions":
        return self._set_filter("pad_intern", value)

    def inrnum(self, value: list[str] | tuple[str, ...] | str | None) -> "Motions":
        return self._set_filter("inrnum", value)

    def sw(self, value: list[str] | tuple[str, ...] | str | None) -> "Motions":
        return self._set_filter("sw", value)

    def eurovoc(self, value: list[str] | tuple[str, ...] | str | None) -> "Motions":
        return self._set_filter("eurovoc", value)

    def frak_code(self, value: list[str] | tuple[str, ...] | str | None) -> "Motions":
        return self._set_filter("frak_code", value)

    def vhg(self, value: list[str] | tuple[str, ...] | str | None) -> "Motions":
        return self._set_filter("vhg", value)

    def AsList(self) -> list[Motion]:
        """Return motions matching the configured filters."""

        return self._list_records(Motion)
