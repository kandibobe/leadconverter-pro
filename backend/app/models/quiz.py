from sqlalchemy import Column, Integer, String, Text, func
from sqlalchemy.orm import relationship

from app.db.base import Base

class Quiz(Base):
    __tablename__ = "quizzes"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    description = Column(Text, nullable=True)
    
    # --- НОВЫЕ ПОЛЯ ДЛЯ МЕТРИК ---
    views = Column(Integer, nullable=False, default=0, server_default='0')
    starts = Column(Integer, nullable=False, default=0, server_default='0')
    # -----------------------------

    questions = relationship("Question", back_populates="quiz", cascade="all, delete-orphan")

class Question(Base):
    __tablename__ = "questions"
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    question_type = Column(String, default="single-choice")
    order = Column(Integer, nullable=False)
    quiz_id = Column(Integer, ForeignKey("quizzes.id"))
    quiz = relationship("Quiz", back_populates="questions")
    options = relationship("Option", back_populates="question", cascade="all, delete-orphan")

class Option(Base):
    __tablename__ = "options"
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, nullable=False)
    price_impact = Column(Float, default=0.0)
    order = Column(Integer, nullable=False)
    question_id = Column(Integer, ForeignKey("questions.id"))
    question = relationship("Question", back_populates="options")