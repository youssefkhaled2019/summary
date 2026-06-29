# database.py

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase,declarative_base,sessionmaker


DATABASE_URL = "sqlite:///app.db"                                      #"sqlite:///./test.db"
#DATABASE_URL = "postgresql+psycopg2://postgres:1234@localhost/mydb" #PostgreSQL "postgresql://user:password@localhost/dbname"
                                            #"mysql+pymysql://user:password@localhost/db_name" #MySQL
# Engine
engine = create_engine(DATABASE_URL,connect_args={"check_same_thread": False}) #مسؤول عن الاتصال بقاعدة البيانات.
# engine = create_engine( DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {})
"""
echo=True يجعل SQLAlchemy يطبع SQL في الـ Terminal.
"""


# Session Factory
SessionLocal = sessionmaker(bind=engine,autoflush=False,autocommit=False)

# Base Class
# class Base(DeclarativeBase):
#     pass
Base = declarative_base()

# Dependency for FastAPI
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()


#  ------------ main.py
# Base.metadata.create_all(bind=engine)       

# ------------------
# new_user = User(name="Ahmed")
# db.add(new_user)
# db.commit()
# db.refresh(new_user) يجلب البيانات الجديدة من قاعدة البيانات.





# db.query()
# db.get()
# db.delete()
# db.close()
# ------------------
# from fastapi import Depends
# from sqlalchemy.orm import Session
# @app.get("/")
# def read_users(   db: Session = Depends(get_db) ):
#     pass