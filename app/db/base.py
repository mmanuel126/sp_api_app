from app.db.models import user  # Import models here
from app.db.session import engine
from sqlalchemy.orm import declarative_base

Base = declarative_base()

def init_db():
    Base.metadata.create_all(bind=engine)