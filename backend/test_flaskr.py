import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_paginated_questions(self):
        res = self.client().get("/questions")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["total_questions"])
        self.assertTrue(len(data["total_questions"]))
        self.assertTrue(len(data["categories"]))

    def test_404_get_paginated_questions(self):
        res = self.client().get("/questions?page=1000", json={"difficulty": 1})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")

    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['categories']))

    def test_get_questions_by_category(self):
        res = self.client().get('/categories/2/question')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['current_category'], 'Art')
     
    def test_get_404_questions_by_category(self):
        res = self.client().get('/categories/1000/question')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['message'], 'Page not found!')
        self.assertEqual(data['success'], False)

    def test_delete_question(self):
        res = self.client().delete('/questions/2')
        data = json.loads(res.data)
        question =Question.query.filter(Question.id == 2).one_or_none()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data["deleted"], 2)
        self.assertEqual(data["total_questions"])
        self.assertEqual(question,None)

    def test_delete_question_422(self):
        res = self.client().delete('/question/1000')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_create_question(self):
        new_question = {
            'question': 'what have you learnt in ALX?',
            'answer': 'API evelopment and Testing',
            'difficulty': 3,
            'category': 5
        }
        res = self.client().post('/questions', json=new_question)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question_created'])
        self.assertTrue(len(data['total_questions']))

    def test_405_create_question(self):
        new_question = {
            'question': '',
            'answer': 'API evelopment and Testing',
            'difficulty': 3,
            'category': 5
        }
        res = self.client().post('/questions', json=new_question)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'method not allowed')
        
    def test_search(self):
        search = {'searchTerm': 'title', }
        res = self.client().post('/search', json=search)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['total_questions']))


    def test_405_search_not_found(self):
        new_search = {
            'searchTerm': '',
        }
        res = self.client().post('/search', json=new_search)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'method not allowed')

    def test_quiz(self):
        new_quiz = {
            'previous_questions': 5,
            'quiz_category': {
                'type': 'History',
                'id': 4
            }
        }
        res = self.client().post('/quizzes', json=new_quiz)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['question']['category'], 4)

    def test_405_quiz_not_allowed(self):
        new_quiz = {
            'previous_questions': 100,
            'quiz_category': {
                'type': 'games',
                'id': 100
            }
        }
        res = self.client().post('/quizzes', json=new_quiz)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()