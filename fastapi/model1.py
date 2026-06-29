
# ORM =Object Relational Mapping

from sqlalchemy import Column, Integer, String,Text,Boolean,Float,Numeric,Date,DateTime,Time,LargeBinary
from database import Base
from datetime import datetime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
class User(Base): #(SQLAlchemy 1.x)
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))  # Column(String)
     role = Column(String, default="user")
    username = Column(String(50),unique=True,nullable=False)
    description = Column(Text)
    is_active = Column(Boolean, default=True)
    price = Column(Float)
    price = Column(Numeric(10, 2)) # is Decimal للقيم المالية بدقة أعلى
    birth_date = Column(Date) #2026-06-27
    start_time = Column(Time) #14:30:00
    created_at = Column(DateTime) #2026-06-27 14:30:00
    created_at = Column(DateTime,  default=datetime.utcnow)
    file_data = Column(LargeBinary) #يستخدم للملفات والصور (رغم أن الأفضل عادة تخزين مسار الملف فقط).



# primary_key=True
# unique=True
# nullable=False
# default=True

# =================  Relationships   ================= 

# ---------------- One To One ----------------
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    profile = relationship("Profile", back_populates="user", uselist=False)

class Profile(Base):
    __tablename__ = "profiles"
    id = Column(Integer, primary_key=True)
    user_id = Column( Integer, ForeignKey("users.id"), unique=True)
    user = relationship(  "User",  back_populates="profile" )

# ---------------- One To Many ----------------
from sqlalchemy import Column, Integer, String,ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String)
    posts = relationship( "Post", back_populates="owner")


class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    user_id = Column(  Integer,  ForeignKey("users.id") )
    owner = relationship(    "User",     back_populates="posts" )

# print(user.posts) user = db.query(User).first()
# print(post.owner.username) post = db.query(Post).first()


# posts = db.query(Post).join(User).all()
# users = db.query(User).all()
# count = db.query(User).count()
# user = db.query(User).filter(User.id == 1).first()
# users = db.query(User).filter(User.name == "Ali").all()
# users = db.query(User).filter(User.email.like("%gmail%")).all()
# result = db.query(User, Post).join(Post, User.id == Post.user_id).all()
# users = db.query(User).order_by(User.id.desc()).all()
# users = db.query(User).offset(10).limit(5).all()
# post = db.query(Post).first()
# print(post.owner.name)
# user = db.query(User).filter(User.id == 1).first()
# print(user.posts)
# new_user = User(name="Ahmed", email="ahmed@gmail.com")
# db.add(new_user)
# db.commit()
# db.refresh(new_user)
# user = db.query(User).filter(User.id == 1).first()
# user.name = "New Name"
# db.commit()
# user = db.query(User).filter(User.id == 1).first()
# db.delete(user)
# db.commit()




user = User(username="ali")
post1 = Post(title="FastAPI", owner=user)
post2 = Post(title="RAG", owner=user)
db.add(user)
db.commit()



# ---------------- Many To Many ----------------
from sqlalchemy import Table
student_course = Table("student_course",Base.metadata,
    Column( "student_id", Integer, ForeignKey("students.id")),
    Column(   "course_id",   Integer,   ForeignKey("courses.id")))


class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True)
    courses = relationship( "Course",   secondary=student_course,   back_populates="students" )

class Course(Base):
    __tablename__ = "courses"
    id = Column(Integer, primary_key=True)
    students = relationship( "Student", secondary=student_course, back_populates="courses")    