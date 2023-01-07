import logging

file_logger_v = logging.getLogger('info logger')
file_logger_v.setLevel(logging.INFO)

fh = logging.FileHandler('logs.log')
fh.setLevel(logging.INFO)
fh.setFormatter(logging.Formatter('%(asctime)s | %(levelname)s | %(message)s'))
file_logger_v.addHandler(fh)

file_logger_v.info('logger start')
