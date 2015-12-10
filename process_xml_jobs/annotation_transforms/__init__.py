from .normalize_headings import normalize_headings
from .make_statutes import make_statutes

transforms = [
    normalize_headings,
    make_statutes,
]
