"""
Check status of all the services required for the initialization of service like DB, logger, file paths etc
"""
import logging
from app.config import settings
from app.logging.loggingconfig import configure_logging
from app.db.session import SessionLocal

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(settings.PROJECT_NAME)


def init_logging(settings) -> None:
    try:
        configure_logging(settings)
    except Exception as e:
        logger.error(e)
        raise e


def init_messaging(settings) -> None:
    # Initialize Message Listeners
    pass


def db_status() -> None:
    """
    Checks the status of DB
    """
    try:
        db = SessionLocal()
        # Try to create session to check if DB is awake
        # command can be changed according to the DB server used
        db.execute("SELECT 1")
    except Exception as e:
        logger.error(e)
        raise e


def check_env_file():
    pass


def init(settings):
    init_logging(settings)
    db_status()
    #init_messaging(settings)
    logger.info("Verifying the env file")
    #check_env_file()


def main() -> None:
    logger.info("Initializing the Micro Service <name> ")
    app = init(settings)
    logger.info("Micro Service <name> Initialization finished")
    return app


if __name__ == "__main__":
    main()
