from sqlalchemy import Column, Integer, String, Text, Float, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base


class Opportunity(Base):
    __tablename__ = "opportunities"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    university = Column(String(100), nullable=False)
    domain = Column(String(100), nullable=False)
    posted_date = Column(Date, nullable=False)
    
    applications = relationship("Application", back_populates="opportunity")


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=True)
    domain_interest = Column(String(100), nullable=False)
    skills = Column(Text, nullable=True)  # Comma-separated skills
    bio = Column(Text, nullable=True)
    resume_url = Column(String(500), nullable=True)
    hackathons = Column(Integer, default=0)
    internships = Column(Integer, default=0)
    research_papers = Column(Integer, default=0)
    coding_score = Column(Float, default=0.0)
    
    applications = relationship("Application", back_populates="student")
    posts = relationship("Post", back_populates="author")
    comments = relationship("Comment", back_populates="author")


class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    opportunity_id = Column(Integer, ForeignKey("opportunities.id"), nullable=False)
    status = Column(String(50), default="submitted")  # submitted, under_review, accepted, rejected
    applied_at = Column(DateTime, default=datetime.utcnow)
    
    student = relationship("Student", back_populates="applications")
    opportunity = relationship("Opportunity", back_populates="applications")


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    author_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    domain = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    author = relationship("Student", back_populates="posts")
    comments = relationship("Comment", back_populates="post", cascade="all, delete-orphan")


class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey("posts.id"), nullable=False)
    author_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    post = relationship("Post", back_populates="comments")
    author = relationship("Student", back_populates="comments")
