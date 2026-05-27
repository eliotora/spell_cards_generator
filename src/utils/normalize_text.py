from unicodedata import normalize, category

REPLACEMENTS = {
    '\u2019': "'",  # ' apostrophe typographique → apostrophe droite
    '\u2018': "'",  # ' guillemet simple ouvrant
    '\u201C': '"',  # " guillemet double ouvrant
    '\u201D': '"',  # " guillemet double fermant
    '\u00AB': '"',  # « guillemet français ouvrant
    '\u00BB': '"',  # » guillemet français fermant
    '\u2013': '-',  # – tiret demi-cadratin
    '\u2014': '-',  # — tiret cadratin
    '\u2026': '...',# … points de suspension
}

def normalize_text(text: str) -> str:
    # 1. Manual normalization
    for orig, repl in REPLACEMENTS.items():
        text = text.replace(orig, repl)

    nfkd = normalize("NFKD", text)
    return ''.join(c for c in nfkd if category(c) != 'Mn')