"""This file contains the test cases for the trivia app."""

import json
import subprocess
import unittest
from flaskr import create_app
from flaskr.models import Question, db
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
        """Test the GET /categories endpoint."""
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['categories'])
        self.assertEqual(data['success'], True)

    def test_get_questions(self):
        """Test the GET /questions endpoint."""
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['categories'])
        self.assertTrue(data['questions'])
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])

    def test_get_paginated_questions(self):
        """Test the GET /questions?page=1 endpoint."""
        res = self.client().get('/questions?page=1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['categories'])
        self.assertTrue(data['questions'])
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])

    def test_get_questions_422_unprocessable(self):
        """Test the GET /questions?page=999 endpoint."""
        res = self.client().get('/questions?page=999')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable entity')

    def test_delete_question(self):
        """Test the DELETE /questions/12 endpoint."""
        res = self.client().delete('/questions/12')
        data = json.loads(res.data)

        with self.app.app_context():
            question = Question.query.filter(Question.id == 12).one_or_none()
        self.assertEqual(question, None)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['deleted'], 12)
        self.assertTrue(data['questions'])
        self.assertEqual(data['success'], True)

    def test_404_not_found_question_delete(self):
        """Test the DELETE /questions/999 endpoint."""
        res = self.client().delete('/questions/999')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found')

    def test_search_questions(self):
        """Test the POST /questions/search endpoint."""
        res = self.client().post('/questions/search', json={'searchTerm': 'what'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['questions'])
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])

    def test_create_question(self):
        """Test the POST /questions endpoint."""
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

    def test_create_question_empty_string_400(self):
        """Test the POST /questions endpoint with empty strings."""
        res = self.client().post('/questions', json={
            'question': '',
            'answer': '',
            'difficulty': 1,
            'category': 1
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad request')

    def test_400_create_question_failed(self):
        """Test the POST /questions endpoint with missing fields."""
        res = self.client().post('/questions', json={})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad request')

    def test_get_questions_by_category(self):
        """Test the GET /categories/1/questions endpoint."""
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['current_category'])
        self.assertTrue(data['questions'])
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])

    def test_422_category_unprocessable(self):
        """Test the GET /categories/999/questions endpoint."""
        res = self.client().get('/categories/999/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable entity')

    def test_play_quiz(self):
        """Test the POST /quizzes endpoint."""
        res = self.client().post('/quizzes', json={
            'previous_questions': [],
            'quiz_category': {'id': 1, 'type': 'Science'}
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['question'])
        self.assertEqual(data['success'], True)

    def test_422_quiz_unprocessable(self):
        """Test the POST /quizzes endpoint with missing fields."""
        res = self.client().post('/quizzes', json={})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable entity')

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
