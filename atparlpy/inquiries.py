"""Parliamentary inquiries dataset wrapper."""

from __future__ import annotations

from ._filter_api import FilterApiDataset, build_payload, int_to_roman, normalize_dimensions
from ._record import ParliamentRecord


class Inquiry(ParliamentRecord):
    """Represents a single parliamentary inquiry row from the API."""


class Inquiries(FilterApiDataset):
    """Wrapper for the parliamentary inquiries dataset."""

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
        "vhg": "VHG",
    }

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
            gp_code=gp_code if gp_code is not None else (self._roman_gp(gp) if gp is not None else None),
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

    @staticmethod
    def _roman_gp(value: int) -> str:
        return int_to_roman(value)

    def _inquiry_vhg(self) -> list[str] | None:
        """Return the fixed VHG value for the current chamber selection."""

        nrbr_values = normalize_dimensions(self._filters.get("nrbr"))
        if not nrbr_values:
            return None
        if "BR" in nrbr_values:
            return ["J_JPR_M-BR"]
        if "NR" in nrbr_values:
            return ["J_JPR_M"]
        return None

    def _payload(self) -> dict[str, list[str]]:
        payload = build_payload(self._filters, self.aliases, {})
        vhg = self._inquiry_vhg()
        if vhg:
            payload["VHG"] = vhg
        return payload

    def gp(self, value: int | None) -> "Inquiries":
        if value is None:
            return self._set_filter("gp_code", None)
        return self._set_filter("gp_code", self._roman_gp(value))

    def nrbr(self, value: list[str] | tuple[str, ...] | str | None) -> "Inquiries":
        return self._set_filter("nrbr", value)

    def gp_code(self, value: list[str] | tuple[str, ...] | str | None) -> "Inquiries":
        return self._set_filter("gp_code", value)

    def themen(self, value: list[str] | tuple[str, ...] | str | None) -> "Inquiries":
        return self._set_filter("themen", value)

    def doktyp(self, value: list[str] | tuple[str, ...] | str | None) -> "Inquiries":
        return self._set_filter("doktyp", value)

    def pad_intern(self, value: list[str] | tuple[str, ...] | str | None) -> "Inquiries":
        return self._set_filter("pad_intern", value)

    def inrnum(self, value: list[str] | tuple[str, ...] | str | None) -> "Inquiries":
        return self._set_filter("inrnum", value)

    def sw(self, value: list[str] | tuple[str, ...] | str | None) -> "Inquiries":
        return self._set_filter("sw", value)

    def eurovoc(self, value: list[str] | tuple[str, ...] | str | None) -> "Inquiries":
        return self._set_filter("eurovoc", value)

    def frak_code(self, value: list[str] | tuple[str, ...] | str | None) -> "Inquiries":
        return self._set_filter("frak_code", value)

    def vhg(self, value: list[str] | tuple[str, ...] | str | None) -> "Inquiries":
        return self._set_filter("vhg", value)

    def AsList(self) -> list[Inquiry]:
        """Return inquiries matching the configured filters."""

        return self._list_records(Inquiry)
