"""Committee reports dataset wrapper."""

from __future__ import annotations

from .._filter_api import FilterApiDataset, int_to_roman
from .._record import ParliamentRecord


class CommitteeReport(ParliamentRecord):
    """Represents a single committee report row from the API."""


class CommitteeReports(FilterApiDataset):
    """Wrapper for the committee reports dataset."""

    aliases = {
        "nrbr": "NRBR",
        "vhg": "VHG",
        "gp_code": "GP_CODE",
        "themen": "THEMEN",
        "sw": "SW",
        "eurovoc": "EUROVOC",
    }

    def __init__(
        self,
        gp: int | None = None,
        nrbr: list[str] | tuple[str, ...] | str | None = None,
        vhg: list[str] | tuple[str, ...] | str | None = None,
        gp_code: list[str] | tuple[str, ...] | str | None = None,
        themen: list[str] | tuple[str, ...] | str | None = None,
        sw: list[str] | tuple[str, ...] | str | None = None,
        eurovoc: list[str] | tuple[str, ...] | str | None = None,
    ) -> None:
        super().__init__(
            gp_code=gp_code if gp_code is not None else (int_to_roman(gp) if gp is not None else None),
            nrbr=nrbr,
            vhg=vhg,
            themen=themen,
            sw=sw,
            eurovoc=eurovoc,
        )

    def gp(self, value: int | None) -> "CommitteeReports":
        if value is None:
            return self._set_filter("gp_code", None)
        return self._set_filter("gp_code", int_to_roman(value))

    def nrbr(self, value: list[str] | tuple[str, ...] | str | None) -> "CommitteeReports":
        return self._set_filter("nrbr", value)

    def vhg(self, value: list[str] | tuple[str, ...] | str | None) -> "CommitteeReports":
        return self._set_filter("vhg", value)

    def gp_code(self, value: list[str] | tuple[str, ...] | str | None) -> "CommitteeReports":
        return self._set_filter("gp_code", value)

    def themen(self, value: list[str] | tuple[str, ...] | str | None) -> "CommitteeReports":
        return self._set_filter("themen", value)

    def sw(self, value: list[str] | tuple[str, ...] | str | None) -> "CommitteeReports":
        return self._set_filter("sw", value)

    def eurovoc(self, value: list[str] | tuple[str, ...] | str | None) -> "CommitteeReports":
        return self._set_filter("eurovoc", value)

    def AsList(self) -> list[CommitteeReport]:
        """Return committee reports matching the configured filters."""

        return self._list_records(CommitteeReport)
