from sqlalchemy import Column, Integer, String, Float, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.db.base import Base

class Quiz(Base):
    __tablename__ = "quizzes"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    questions = relationship("Question", back_populates="quiz")

class Question(Base):
    __tablename__ = "questions"
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String)
    question_type = Column(String, default="single-choice")  # single-choice, slider
    quiz_id = Column(Integer, ForeignKey("quizzes.id"))
    quiz = relationship("Quiz", back_populates="questions")
    options = relationship("Option", back_populates="question")

class Option(Base):
    __tablename__ = "options"
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String)
    value = Column(Float, default=0.0) # Ценовое влияние этого ответа
    question_id = Column(Integer, ForeignKey("questions.id"))
    question = relationship("Question", back_populates="options")

class Lead(Base):
    __tablename__ = "leads"
    id = Column(Integer, primary_key=True, index=True)
    client_email = Column(String, index=True)
    estimated_cost = Column(Float)
codex/check-models-for-single-choice-usage
    details = Column(JSON)  # Здесь будем хранить все ответы квиза

    details = Column(JSON) # Здесь будем хранить все ответы квиза
main
