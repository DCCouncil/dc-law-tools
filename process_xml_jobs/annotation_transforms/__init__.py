from .normalize_headings import normalize_headings
from .make_statutes import make_statutes
from .move_leghistory import move_leghistory
transforms = [
    normalize_headings,
    make_statutes,
    move_leghistory,
]
