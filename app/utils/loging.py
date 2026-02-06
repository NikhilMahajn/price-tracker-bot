import logging

def getLogger(dir):
	logger = logging.getLogger(dir)
	logger.setLevel(logging.INFO)
	return logger