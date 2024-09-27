from dataclasses import dataclass, field


@dataclass(frozen=True)
class Config:
    allowed_formats: set[str] = field(default_factory=set)
    playlists_directory: str = None
    transcodes_output_directory: str = None
    playlists_output_directory: str = None
    max_parallel_tasks: int = None
