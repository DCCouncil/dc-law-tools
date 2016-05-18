from .clean_annos import clean_annos
from .normalize_headings import normalize_headings
from .process_history import process_history
from .move_stat_info import move_stat_info

transforms = [
    normalize_headings,
    clean_annos,
    process_history,
    move_stat_info,
]
