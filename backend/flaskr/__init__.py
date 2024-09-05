import os
from config import Config
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flaskr.models import setup_db, Question, Category

import random

db = SQLAlchemy()

QUESTIONS_PER_PAGE = 10

def paginate_questions(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    formatted_questions = [question.format() for question in selection]
    current_questions = formatted_questions[start:end]

    return current_questions

def create_app(config_class=Config, test_config=None):
    app = Flask(__name__)
    app.config.from_object(config_class)

    if test_config is None:
        setup_db(app)
    else:
        database_path = test_config.get('SQLALCHEMY_DATABASE_URI')
        setup_db(app, database_path=database_path)

    CORS(app)

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
        response.headers.add('Access-Control-Allow-Methods', 'GET,POST,PATCH,DELETE,OPTIONS')
        return response
    
    @app.route('/categories')
    def get_categories():
        categories = Category.query.all()

        if categories is None:
            abort(404)

        formatted_categories = {category.id: category.type for category in categories}
        return jsonify({
            'success': True,
            'categories': formatted_categories
        })

    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """
    @app.route('/questions')
    def get_questions():
        questions = Question.query.all()
        current_questions = paginate_questions(request, questions)
        categories = Category.query.all()
        formatted_categories = {category.id: category.type for category in categories}

        return jsonify({
            'success': True,
            'questions': current_questions,
            'total_questions': len(questions),
            'categories': formatted_categories,
            'current_category': None
        })
    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            question = Question.query.get(question_id)
            if question is None:
                abort(404)
            question.delete()
            updated_questions = Question.query.all()
            current_questions = paginate_questions(request, updated_questions)
            return jsonify({
                'success': True,
                'deleted': question_id,
                'questions': current_questions
            })
        
        except:
            abort(422)
    
    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """

    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """
    @app.route('/questions', methods=['POST'])
    def create_question():
        body = request.get_json()

        search_term = body.get('searchTerm', None)
        if search_term:
            questions = Question.query.filter(Question.question.ilike(f'%{search_term}%')).all()
            formatted_questions = [question.format() for question in questions]

            return jsonify({
                'success': True,
                'questions': formatted_questions,
                'total_questions': len(formatted_questions),
                'current_category': None
            })
        
        question = body.get('question', None)
        answer = body.get('answer', None)
        category = body.get('category', None)
        difficulty = body.get('difficulty', None)

        if question is None or answer is None or category is None or difficulty is None:
            abort(422)

        try:
            new_question = Question(question=question, answer=answer, category=category, difficulty=difficulty)
            new_question.insert()
            updated_questions = Question.query.all()
            current_questions = paginate_questions(request, updated_questions)
            return jsonify({
                'success': True,
                'created': new_question.id,
                'questions': current_questions
            })
        
        except:
            abort(422)

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route('/categories/<int:category_id>/questions')
    def get_questions_by_category(category_id):
        questions = Question.query.filter(Question.category == category_id).all()
        category = Category.query.get(category_id)
        current_questions = paginate_questions(request, questions)

        return jsonify({
            'success': True,
            'questions': current_questions,
            'total_questions': len(current_questions),
            'current_category': category.type
        })
    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """
    @app.route('/quizzes', methods=['POST'])
    def play_quiz():
        body = request.get_json()
        previous_questions = body.get('previous_questions', [])
        quiz_category = body.get('quiz_category', None)

        if quiz_category is None:
            abort(400)

        if quiz_category['id'] == 0:
            questions = Question.query.all()
        else:
            questions = Question.query.filter(Question.category == quiz_category['id']).all()

        formatted_questions = [question.format() for question in questions]
        random_question = None

        for question in formatted_questions:
            if question['id'] not in previous_questions:
                random_question = question
                break

        return jsonify({
            'success': True,
            'question': random_question
        })
    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'Resource not found'
        }), 404
    
    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'Unprocessable entity'
        }), 422
    
    return app
