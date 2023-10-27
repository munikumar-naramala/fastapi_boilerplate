from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
# Define your MySQL connection details
mysql_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Anandini@512',
    'database': 'sampledata'
}

# Construct the MySQL connection URL
DATABASE_URL = f"mysql+mysqlconnector://{mysql_config['user']}:{mysql_config['password']}@{mysql_config['host']}/{mysql_config['database']}"

# Create a database engine
engine = create_engine(DATABASE_URL)

# Create a SessionLocal class to manage the database session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
