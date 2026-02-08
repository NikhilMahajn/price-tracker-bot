import logging
logging.basicConfig(level=logging.INFO)
def getLogger(dir):
	logger = logging.getLogger(dir)
	logger.setLevel(logging.INFO)
	return logger