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

    @app.route('/questions')
    def get_questions():
        questions = Question.query.all()
        current_questions = paginate_questions(request, questions)
        categories = Category.query.all()
        formatted_categories = {category.id: category.type for category in categories}

        if current_questions is None or formatted_categories is None:
            abort(404)

        return jsonify({
            'success': True,
            'questions': current_questions,
            'total_questions': len(questions),
            'categories': formatted_categories,
            'current_category': None
        })

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        question = Question.query.get(question_id)
        if question is None:
            abort(404)
        try:    
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
            abort(404)

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

    @app.route('/categories/<int:category_id>/questions')
    def get_questions_by_category(category_id):
        questions = Question.query.filter(Question.category == category_id).all()
        category = Category.query.get(category_id)

        if questions is None or category is None:
            abort(404)

        current_questions = paginate_questions(request, questions)

        return jsonify({
            'success': True,
            'questions': current_questions,
            'total_questions': len(current_questions),
            'current_category': category.type
        })

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

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'Bad request'
        }), 400

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
