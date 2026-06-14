from __future__ import annotations

from flask import request, session

from app.translations.en import EN
from app.translations.pl import PL

TRANSLATIONS = {"pl": PL, "en": EN}


def get_locale() -> str:
    lang = session.get("lang") or request.args.get("lang") or "pl"
    return lang if lang in TRANSLATIONS else "pl"


def t(key: str, **kwargs: object) -> str:
    locale = get_locale()
    text = TRANSLATIONS.get(locale, PL).get(key, PL.get(key, key))
    if kwargs:
        return text.format(**kwargs)
    return text
