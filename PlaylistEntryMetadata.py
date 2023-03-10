import os

from MediaInfoMetadata import MediaInfoMetadata


class PlaylistEntryMetadata:
    album_artist: str
    album: str
    track: int
    disc: int
    title: str

    def __init__(self, media_info: MediaInfoMetadata):
        metadata = media_info.get_metadata()
        self.album_artist = metadata.get('album_artist')
        self.album = metadata.get('album')
        self.track = int(metadata.get('track').rsplit('/')[0])
        self.disc = int(metadata.get('disc').rsplit('/')[0])
        self.title = metadata.get('title')

    def filename(self) -> str:
        return os.sep.join([self.album_artist, self.album,
                            ' '.join(['-'.join([str(self.disc), f"{self.track:02d}"]), self.title])])
