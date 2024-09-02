class Config:
    playlists_directory: str
    transcodes_output_directory: str
    playlists_output_directory: str
    max_parallel_tasks: int

    def __init__(self,
                 playlists_directory, transcodes_output_directory, playlists_output_directory, max_parallel_tasks):
        self.playlists_directory = playlists_directory
        self.transcodes_output_directory = transcodes_output_directory
        self.playlists_output_directory = playlists_output_directory
        self.max_parallel_tasks = int(max_parallel_tasks)
