import multiprocessing.managers
from dataclasses import dataclass


@dataclass(frozen=True)
class PlaylistEntryLocks:
    lock: multiprocessing.Lock = None
    media_info_adapter_lock: multiprocessing.Lock = None
    media_info_adapter_dict: multiprocessing.managers.DictProxy = None
