import asyncio
import datetime
import logging.handlers
import os
import pathlib
import sys
import time

from playlist_creator import configuration, PlaylistCreator

logger = logging.getLogger(__name__)

_ALLOWED_FORMATS = {'MP3', 'WAV', 'ALAC', 'AIFF'}


def _set_up_logging():
    logs_directory = 'logs'

    pathlib.Path(logs_directory).mkdir(parents=True, exist_ok=True)

    log_filename = os.path.join(logs_directory, 'playlist_creator.log')
    log_filename_exists = os.path.isfile(log_filename)
    rotating_file_handler = logging.handlers.RotatingFileHandler(
        log_filename, backupCount=10, encoding='utf-8'
    )
    rotating_file_handler.setLevel(logging.DEBUG)

    if log_filename_exists:
        rotating_file_handler.doRollover()

    std_out_handler = logging.StreamHandler(sys.stdout)
    std_out_handler.setLevel(logging.INFO)
    std_out_handler.addFilter(lambda record: record.levelno <= logging.INFO)

    std_err_handler = logging.StreamHandler()
    std_err_handler.setLevel(logging.WARNING)

    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s:%(levelname)s:%(name)s: %(message)s',
        handlers=[rotating_file_handler, std_out_handler, std_err_handler]
    )


def main():
    _set_up_logging()

    started_at = time.time()

    max_parallel_tasks = os.cpu_count()

    if len(sys.argv) > 4:
        max_parallel_tasks_argv = int(sys.argv[4])
        if max_parallel_tasks_argv > 0:
            max_parallel_tasks = max_parallel_tasks_argv

    config_argv = configuration.Config(
        _ALLOWED_FORMATS, sys.argv[1], sys.argv[2], sys.argv[3], max_parallel_tasks
    )

    asyncio.run(PlaylistCreator.main(config_argv))

    finished_at = time.time()
    elapsed_time = finished_at - started_at
    logger.info(f"Done in {datetime.timedelta(seconds=elapsed_time)}")


if __name__ == '__main__':
    sys.exit(main())
