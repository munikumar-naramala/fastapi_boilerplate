import logging

from logstash_async.handler import AsynchronousLogstashHandler


def configure_logging(settings, log_level=logging.DEBUG):
    logger = logging.getLogger(settings.PROJECT_NAME)
    logger.setLevel(log_level)

    handler = AsynchronousLogstashHandler(
        settings.LOGSTASH_HOST,
        settings.LOGSTASH_PORT,
        database_path=''
    )

    logger.addHandler(handler)
    logger.info(f'{settings.PROJECT_NAME} startup')
    return logger
