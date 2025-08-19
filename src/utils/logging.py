import logging
import logging.handlers


def setup_logger():
    logger = logging.getLogger('app')
    logger.setLevel(logging.INFO)
    
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
    
    handler = logging.handlers.TimedRotatingFileHandler(
        filename='logs/app.log',
        when='D',
        backupCount=5,
        encoding='utf-8'
    )
    
    formatter = logging.Formatter(
        "[%(asctime)s] - |%(levelname)s| - %(message)s",
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    handler.setFormatter(formatter)
    
    logger.addHandler(handler)
    return logger


logger = setup_logger()