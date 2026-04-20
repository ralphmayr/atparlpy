"""Shared detail response models."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class Name:
    """Represents a name entry inside a detail response."""

    funktext: str = ''
    name: str = ''
    frak_code: str = ''
    url: str = ''

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> "Name":
        return cls(
            funktext=value.get("funktext", ""),
            name=value.get("name", ""),
            frak_code=value.get("frak_code", ""),
            url=value.get("url", ""),
        )


@dataclass(slots=True)
class Reference:
    """Represents a reference entry inside a detail response."""

    text: str | None = None
    subject: str | None = None
    zitation: str | None = None
    url: str | None = None
    art: str | None = None

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> "Reference":
        return cls(
            text=value.get("text"),
            subject=value.get("subject"),
            zitation=value.get("zitation"),
            url=value.get("url"),
            art=value.get("art"),
        )


@dataclass(slots=True)
class Details:
    """Generic detail response."""

    pagetype: str | None = None
    meta: dict[str, Any] | None = None
    content: dict[str, Any] | None = None
    names: list[Name] | None = None
    references: list[Reference] | None = None

    @classmethod
    def from_api_response(cls, payload: dict[str, Any]) -> "Details":
        content = payload.get("content") or {}
        names = content.get("names") or []
        references = content.get("references") or content.get("reference") or []
        return cls(
            pagetype=payload.get("pagetype"),
            meta=payload.get("meta") or {},
            content=content,
            names=[Name.from_dict(item) for item in names],
            references=[Reference.from_dict(item) for item in references],
        )
