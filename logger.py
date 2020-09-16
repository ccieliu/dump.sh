import logging

formatter = logging.Formatter(
    "%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s : %(message)s")
logFile = logging.FileHandler("./logs/runtime.log")
logFile.setFormatter(formatter)
# Setup a log console handler and set level/formater
logConsole = logging.StreamHandler()
logConsole.setFormatter(formatter)
# Setup a logger
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logger.addHandler(logFile)
logger.addHandler(logConsole)
