import asyncio
import os
import sys

from playlist_creator import PlaylistCreator, configuration

_ALLOWED_FORMATS = {'MP3', 'WAV', 'ALAC', 'AIFF'}


def main():
    max_parallel_tasks = os.cpu_count()

    if len(sys.argv) > 4:
        max_parallel_tasks_argv = int(sys.argv[4])
        if max_parallel_tasks_argv > 0:
            max_parallel_tasks = max_parallel_tasks_argv

    config_argv = configuration.Config(
        _ALLOWED_FORMATS, sys.argv[1], sys.argv[2], sys.argv[3], max_parallel_tasks
    )

    asyncio.run(PlaylistCreator.main(config_argv))


if __name__ == '__main__':
    sys.exit(main())
