import logging

# custom logger
logger = logging.getLogger(__name__)

# set log level
logger.setLevel(logging.DEBUG)

# create handlers
# c_handler = logging.StreamHandler()
f_handler = logging.FileHandler(r"E:\Pavan Learnings\Braineest\week_01\auto_email_transfer\emaillog.log")
# i_handler = logging.StreamHandler()
# c_handler.setLevel(logging.WARNING)
# f_handler.setLevel(logging.ERROR)
# i_handler.setLevel(logging.INFO)


# create formatters and add it to handlers
# c_format = logging.Formatter("%(asctime)s — %(name)s — %(levelname)s — %(funcName)s:%(lineno)d — %(message)s")
f_format = logging.Formatter("%(asctime)s — %(name)s — %(levelname)s — %(message)s")
# i_format = logging.Formatter("%(asctime)s — %(name)s — %(levelname)s — %(funcName)s:%(lineno)d — %(message)s")
# c_handler.setFormatter(c_format)
f_handler.setFormatter(f_format)
# i_handler.setFormatter(i_format)

# filter to only log info and above
# i_handler.addFilter(lambda record: record.levelno >= logging.INFO)

# add handlers to the logger
# logger.addHandler(c_handler)
logger.addHandler(f_handler)
# logger.addHandler(i_handler)