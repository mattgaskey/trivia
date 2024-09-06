import os
import subprocess
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from flaskr.models import setup_db, Question, Category, db

from sqlalchemy import create_engine, text
from sqlalchemy.exc import ProgrammingError


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""
    
    def setUp(self):
        """Define test variables and initialize app."""
        self.create_test_db()
        self.populate_test_db()
        self.app = create_app(test_config={
            'SQLALCHEMY_DATABASE_URI': 'postgresql://postgres:postgres@db:5432/trivia_test',
            'SQLALCHEMY_TRACK_MODIFICATIONS': False,
            'TESTING': True
        })
        self.client = self.app.test_client

        # binds the app to the current context
        with self.app.app_context():
            self.db = db
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass


    """Automating the test db creation and population"""
    def create_test_db(self):
        """Create the test database if it doesn't exist."""
        engine = create_engine('postgresql://postgres:postgres@db:5432/postgres')
        conn = engine.connect()
        conn = conn.execution_options(isolation_level="AUTOCOMMIT")
        try:
            conn.execute(text("CREATE DATABASE trivia_test"))
        except ProgrammingError:
            pass  # Database already exists
        conn.close()

    def populate_test_db(self):
        """Populate the trivia_test database using the trivia.psql file."""
        drop_tables_command = """
        psql -U postgres -h db -d trivia_test -c "
        DROP TABLE IF EXISTS questions CASCADE;
        DROP TABLE IF EXISTS categories CASCADE;
        "
        """
        populate_command = "psql -U postgres -h db -d trivia_test -f ./trivia.psql"
        
        subprocess.run(drop_tables_command, shell=True, check=True, env={"PGPASSWORD": "postgres"})
        subprocess.run(populate_command, shell=True, check=True, env={"PGPASSWORD": "postgres"})

    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['categories'])
        self.assertEqual(data['success'], True)

    def test_get_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['categories'])
        self.assertTrue(data['questions'])
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])

    def test_get_paginated_questions(self):
        res = self.client().get('/questions?page=1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['categories'])
        self.assertTrue(data['questions'])
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])

    def test_get_questions_404_page_not_found(self):
        res = self.client().get('/questions?page=999')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found')

    def test_delete_question(self):
        res = self.client().delete('/questions/12')
        data = json.loads(res.data)

        with self.app.app_context():
            question = Question.query.filter(Question.id == 12).one_or_none()
        self.assertEqual(question, None)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['deleted'], 12)
        self.assertTrue(data['questions'])
        self.assertEqual(data['success'], True)

    def test_422_unprocessable_question_delete(self):
        res = self.client().delete('/questions/999')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable entity')

    def test_search_questions(self):
        res = self.client().post('/questions', json={'searchTerm': 'what'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['questions'])
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])

    def test_create_question(self):
        res = self.client().post('/questions', json={
            'question': 'How many sides does a triangle have?',
            'answer': 'Three',
            'difficulty': 1,
            'category': 1
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['created'])
        self.assertTrue(data['questions'])
        self.assertEqual(data['success'], True)

    def test_422_create_question_failed(self):
        res = self.client().post('/questions', json={})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable entity')

    def test_get_questions_by_category(self):
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['current_category'])
        self.assertTrue(data['questions'])
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])

    def test_404_category_not_found(self):
        res = self.client().get('/categories/999/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found')

    def test_play_quiz(self):
        res = self.client().post('/quizzes', json={
            'previous_questions': [],
            'quiz_category': {'id': 1, 'type': 'Science'}
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['question'])
        self.assertEqual(data['success'], True)

    def test_400_bad_request(self):
        res = self.client().post('/quizzes', json={})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad request')

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()