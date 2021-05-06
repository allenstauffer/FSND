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
        self.DB_HOST = os.getenv('DB_HOST', '127.0.0.1:5432')  
        self.DB_USER = os.getenv('DB_USER', 'postgres')  
        self.DB_NAME = os.getenv('DB_NAME', 'trivia_test')  
        self.database_path = "postgresql://{}@{}/{}".format(self.DB_USER, self.DB_HOST, self.DB_NAME)

        setup_db(self.app, self.database_path)

        self.new_question = {
            'question': 'Who let the dogs out',
            'answer': 'Who Who',
            'category': 5,
            'difficulty': 1
        }

        self.error_question = {
            'question': 'Who let the dogs out',
            'answer': 'Who Who',
            'category': "This is a category",
            'difficulty': 1
        }

        self.search = {
            'searchTerm': 'Actor',
        }

        self.error_search = {
            'searchTerm': 'ZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZ',
        }        

        self.quiz_obj = {
            "quiz_category":{'id': 5, 'type': 'Entertainment'},
            "previous_questions":[]
        }

        self.error_quiz_obj= {
            "quiz_category":{'id': 500, 'type': 'Nonexistent'},
            "previous_questions":[1,2,3]
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_categories(self):
        self.assertTrue(True)    
        res = self.client().get('/categories')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])

    def test_get_paginated_questions(self):
        self.assertTrue(True)    
        res = self.client().get('/questions?page=1')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertEqual(len(data['questions']), 16)    
        self.assertTrue(data['questions'])    
        self.assertEqual(len(data['questions']), 10)    
        self.assertTrue(data['categories'])    
        self.assertEqual(data['categories'], 6)
        self.assertEqual(data['current_category'], None)

    def test_get_paginated_questions(self):
        self.assertTrue(True)    
        res = self.client().get('/questions?page=1000')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_delete_question(self):
        self.assertTrue(True)    
        res = self.client().delete('/questions/2')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_delete_question_unprocessed(self):
        self.assertTrue(True)    
        res = self.client().delete('/delete/10000')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_add_new_question(self):
        res = self.client().post('/questions', json=self.new_question)
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)

    def test_add_new_question_error(self):
        res = self.client().post('/questions', json=self.error_question)
        self.assertEqual(res.status_code, 422)
        data = json.loads(res.data)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_search_question(self):
        res = self.client().post('/questions', json=self.search)
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])    
        self.assertEqual(data['total_questions'], 1)    
        self.assertEqual(data['current_category'], None)

    def test_add_new_question_error(self):
        res = self.client().post('/questions', json=self.error_search)
        self.assertEqual(res.status_code, 422)
        data = json.loads(res.data)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')       
    
    def test_get_categories_error(self):
        res = self.client().get('/categories/15/questions')
        self.assertEqual(res.status_code, 404)
        data = json.loads(res.data)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')  

    def test_get_categories(self):
        res = self.client().get('/categories/5/questions')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])       
        self.assertEqual(len(data['questions']),3)       
        self.assertTrue(data['total_questions'])       
        self.assertEqual(data['total_questions'],3)       
        self.assertEqual(data['current_category'],5)   

    def test_get_quiz(self):    
        res = self.client().post('/quizzes', json=self.quiz_obj)
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])  

    def test_get_quiz_error(self):    
        res = self.client().post('/quizzes', json=self.error_quiz_obj)
        self.assertEqual(res.status_code, 404)
        data = json.loads(res.data)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_get_quiz_error_missing_data(self):    
        res = self.client().post('/quizzes', json=self.error_search)
        self.assertEqual(res.status_code, 422)
        data = json.loads(res.data)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')
    

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()