from loguru import logger


logger.add("debug.log", format="{time} {level} {message}", level="DEBUG", rotation="10Kb", compression="zip")