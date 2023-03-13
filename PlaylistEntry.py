from PlaylistEntryMetadata import PlaylistEntryMetadata


class PlaylistEntry:
    metadata: PlaylistEntryMetadata

    def __init__(self, file, title, length):
        self.file: str = file
        self.title: str = title
        self.length: str = length
