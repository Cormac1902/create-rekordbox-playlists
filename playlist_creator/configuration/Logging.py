import logging
import os
import pathlib
import sys

def logging_listener_configurer():
    root = logging.getLogger()

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

    formatter = logging.Formatter('%(asctime)s:%(processName)s:%(name)s:%(levelname)s: %(message)s')

    root.addHandler(rotating_file_handler)
    root.addHandler(std_out_handler)
    root.addHandler(std_err_handler)

    [handler.setFormatter(formatter) for handler in root.handlers]



def logger_listener_process(queue, configurer):
    configurer()
    while True:
        record = queue.get()
        if record is None:
            break
        logger = logging.getLogger(record.name)
        logger.handle(record)


def process_logging_configurer(queue):
    root = logging.getLogger()
    if not root.hasHandlers():
        handler = logging.handlers.QueueHandler(queue)
        root.addHandler(handler)
        root.setLevel(logging.DEBUG)