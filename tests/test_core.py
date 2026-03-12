import pytest
import os
import sqlite3
from src.db import db_setup

def test_db_setup():
    # Test table creation
    db_setup.create_tables()
    
    # Test user registration
    db_setup.add_user(12345, "testuser", "Test", "User")
    user = db_setup.get_user(12345)
    assert user is not None
    assert user[1] == "testuser"
    
    # Test subject retrieval
    db_setup.add_question("TEST_SUB", 1, "Q?", "A", "B", "C", "D", "A")
    subjects = db_setup.get_subjects()
    assert "TEST_SUB" in subjects

def test_quiz_logic_init():
    from src.core import QuizClass
    quiz = QuizClass.Quiz(12345, subject="TEST_SUB")
    assert quiz.user_id == 12345
    assert quiz.subject == "TEST_SUB"
    assert quiz.ToatlQuestionInQuiz == 10
