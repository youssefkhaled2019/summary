# pip install sqlalchemy psycopg2-binary #PostgreSQL
# pip install sqlalchemy pymysql #MySQL

# =================
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass
# =================
from sqlalchemy import String,Text,Integer,Boolean,Float,Numeric,Date,DateTime
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime

from uuid import UUID
from sqlalchemy import UUID as SQLUUID
class User(Base): #SQLAlchemy 2.0
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    age: Mapped[int] = mapped_column(Integer)
    bio: Mapped[str] = mapped_column(Text)
    is_active: Mapped[bool] = mapped_column(Boolean,default=True)
    rating: Mapped[float] = mapped_column(Float)
    price: Mapped[float] = mapped_column(Numeric(10, 2)) #DECIMAL(10,2)
    birth_date: Mapped[date] = mapped_column(Date)
    created_at: Mapped[datetime] = mapped_column(DateTime,default=datetime.utcnow)
    id: Mapped[UUID] = mapped_column(   SQLUUID,    primary_key=True)
    phone: Mapped[str | None] = mapped_column( nullable=True) # nullable=False
    email: Mapped[str] = mapped_column(String(255),unique=True,index=True)

# =================  Relationships   ================= 
# ------------------------  
# One-to-Many
User
#  ├── Post 1
#  ├── Post 2
#  └── Post 3

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import relationship
from sqlalchemy.orm import mapped_column

# users         posts
# -----         -----
# id            id
# name          title
#               user_id
class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column( primary_key=True)
    name: Mapped[str]
    posts: Mapped[list["Post"]] = relationship(back_populates="owner")


from sqlalchemy import ForeignKey

class Post(Base):
    __tablename__ = "posts"
    id: Mapped[int] = mapped_column( primary_key=True )
    title: Mapped[str]
    user_id: Mapped[int] = mapped_column( ForeignKey("users.id"))
    owner: Mapped["User"] = relationship( back_populates="posts" )    
# ------------------------
# One-to-One    
class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column( primary_key=True)
    profile: Mapped["Profile"] = relationship( back_populates="user",cascade="all, delete-orphan")

class Profile(Base):
    __tablename__ = "profiles"
    id: Mapped[int] = mapped_column( primary_key=True )
    bio: Mapped[str]
    user_id: Mapped[int] = mapped_column( ForeignKey("users.id"),  unique=True) #unique=True 
    user: Mapped["User"] = relationship(  back_populates="profile" )    
# ------------------------    
# Many-to-Many

from sqlalchemy import Table
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import ForeignKey

student_course = Table("student_course",Base.metadata,
    Column("student_id",  ForeignKey("students.id"),  primary_key=True ),
    Column( "course_id", ForeignKey("courses.id"),primary_key=True  )
)

class Student(Base):
    __tablename__ = "students"
    id: Mapped[int] = mapped_column(  primary_key=True  )
    courses: Mapped[list["Course"]] = relationship(   secondary=student_course,back_populates="students")

class Course(Base):
    __tablename__ = "courses"
    id: Mapped[int] = mapped_column( primary_key=True  )
    students: Mapped[list["Student"]] = relationship( secondary=student_course, back_populates="courses" )    
# -------------------
# user.posts بيعمل مشكله Lazy Loading  الحل  لحل مشكلة N+1 Query.
    # joinedload()
# selectinload()
# -------------------
