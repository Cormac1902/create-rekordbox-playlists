from dataclasses import dataclass


@dataclass(frozen=True)
class Config:
    allowed_formats: set[str]
    playlists_directory: str = None
    transcodes_output_directory: str = None
    playlists_output_directory: str = None
    max_parallel_tasks: int = None
