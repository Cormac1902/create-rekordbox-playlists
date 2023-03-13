import json
import os
import subprocess

from MediaInfo import MediaInfo


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

        self.metadata['album_artist'] = tags.get('album_artist')
        self.metadata['album'] = tags.get('album')
        self.metadata['track'] = tags.get('track')
        self.metadata['disc'] = tags.get('disc')
        self.metadata['title'] = tags.get('title')

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
