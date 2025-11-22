import re


ARABIC_DIACRITICS_RE = re.compile(
    r'[\u0610-\u061A\u064B-\u065F\u0670\u06D6-\u06ED]'
)

def normalize_arabic_spelling(text: str) -> str:
    if not text:
        return ""

    s = text.strip()
    s = re.sub(r'\s+', '', s)

    s = ARABIC_DIACRITICS_RE.sub('', s)

    return s
