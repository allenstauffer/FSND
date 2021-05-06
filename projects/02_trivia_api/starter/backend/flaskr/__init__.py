import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
import sys

from models import setup_db, Question, Category, db

QUESTIONS_PER_PAGE = 10


# modified this for use from paginate_books from the examples
def paginate_questions(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions


def get_catagories():
    categories = Category.query.all()
    returnCatagories = {category.id: category.type for category in categories}
    return returnCatagories


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app, resources={r"*": {'origins': '*'}})
    # CORS Headers

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,DELETE, POST')
        return response

    @app.route('/categories', methods=['GET'])
    def get_categories():
        setCatagories = get_catagories()

        if len(setCatagories) == 0:
            abort(404)

        return jsonify({
          'success': True,
          'categories': setCatagories
        })

    @app.route('/questions', methods=['GET'])
    def get_questions():
        selection = Question.query.all()
        current_questions = paginate_questions(request, selection)

        if len(current_questions) == 0:
            abort(404)

        setCatagories = get_catagories()
        return jsonify({
          'success': True,
          'questions': current_questions,
          'total_questions': len(selection),
          'categories': setCatagories,
          'current_category': None
        })

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            question = Question.query.get(question_id)
            if question is None:
                abort(404)

            question.delete()
            return jsonify({
              'success': True,
              })
        except Exception:
            print(sys.exc_info())
            abort(422)

    @app.route('/questions', methods=['POST'])
    def add_new_question():
        try:
            body = request.get_json()

            search = body.get('searchTerm', None)
            if search is None:
                new_question = body.get('question', None)
                new_answer = body.get('answer', None)
                new_category = body.get('category', None)
                new_difficulty = body.get('difficulty', None)

                question = Question(question=new_question,
                                    answer=new_answer,
                                    category=new_category,
                                    difficulty=new_difficulty)
                question.insert()
                return jsonify({
                  'success': True,
                })
            else:
                selection = Question.query.filter(
                    Question.question.ilike('%{}%'.format(search))
                ).all()
                if len(selection) == 0:
                    abort(404)
                current_questions = paginate_questions(request, selection)
                return jsonify({
                  'success': True,
                  'questions': current_questions,
                  'total_questions': len(selection),
                  'current_category': None
                })
        except Exception:
            print(sys.exc_info())
            abort(422)

    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def get_by_category(category_id):
        if Category.query.get(category_id) is None:
            abort(404)
        selection = Question.query.filter(
            Question.category == str(category_id)
        ).all()
        current_questions = paginate_questions(request, selection)
        return jsonify({
          'success': True,
          'questions': current_questions,
          'total_questions': len(selection),
          'current_category': category_id
        })

    @app.route('/quizzes', methods=['POST'])
    def get_quiz():
        body = request.get_json()
        quiz_category = body.get('quiz_category', None)
        previous_questions = body.get('previous_questions', None)

        if quiz_category is None or previous_questions is None:
            abort(422)
        category_id = quiz_category['id']
        if Category.query.get(category_id) is None:
            abort(404)
        if category_id == 0:
            questions = Question.query.order_by(
                Question.id
            ).filter(
                Question.id.notin_(previous_questions)
            ).all()
        else:
            questions = Question.query.order_by(
                Question.id
            ).filter(
                Question.category == category_id
            ).filter(
                Question.id.notin_(previous_questions)
            ).all()

        if len(questions) == 0:
            question = None
        else:
            rand = random.randrange(0, len(questions))
            question = questions[rand].format()
        return jsonify({
          "success": True,
          "question": question
        })

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
          "success": False,
          "error": 400,
          "message": "bad request"
          }), 400

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
          "success": False,
          "error": 422,
          "message": "unprocessable"
          }), 422

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
          "success": False,
          "error": 404,
          "message": "resource not found"
          }), 404

    return app
