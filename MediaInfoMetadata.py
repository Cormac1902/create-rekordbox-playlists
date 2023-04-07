import json
import os
import subprocess

from MediaInfo import MediaInfo


def get_tag(tags, tag):
    return tags.get(tag) or tags.get(tag.upper())


class MediaInfoMetadata(MediaInfo):
    metadata = dict()

    def get_metadata(self):
        if not os.path.exists(self.filename) or not os.path.exists(self.cmd):
            return None

        cmd_name = os.path.basename(self.cmd)

        if cmd_name == 'ffprobe' or 'ffprobe.exe':
            self._ffprobe_get_metadata()

        return self.metadata

    def _ffprobe_get_metadata(self):
        ffprobe_output = self._run_ffprobe()
        info_dict = json.loads(ffprobe_output)

        tags = info_dict.get('format').get('tags')

        self.metadata['album_artist'] = get_tag(tags, 'album_artist')
        self.metadata['album'] = get_tag(tags, 'album')
        self.metadata['track'] = get_tag(tags, 'track')
        self.metadata['disc'] = get_tag(tags, 'disc')
        self.metadata['title'] = get_tag(tags, 'title')

    def _run_ffprobe(self) -> str:
        cmd = '"' + self.cmd + \
              '" -loglevel quiet -print_format json -show_format -show_error -i "' + \
              self.filename + \
              '"'

        try:
            output_bytes = subprocess.check_output(cmd, shell=True)
        except subprocess.CalledProcessError:
            return ''

        return output_bytes.decode('utf-8')
