from crypt import methods
import os
import re
from unicodedata import category
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category, db

QUESTIONS_PER_PAGE = 10

def paginate_questions(request, selection):
    page = request.args.get("page", 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    books = [book.format() for book in selection]
    current_books = books[start:end]

    return current_books

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app, resource={r"/*":{ "origins":"*" }})

    @app.after_request
    def after_request(response):
        response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization,true")
        response.headers.add("Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS")
        return response

    @app.route("/categories")
    def get_categories():
        try:
            all_categories =  Category.query.order_by(Category.id).all()
            categories = {}
            for category in all_categories:
                categories[category.type] = category.type

            if(len(categories) == 0):
                abort(404)

            return jsonify({
                "success": True,
                "categories": categories,
                "total_categories": len(categories),
            })
        except:
            abort(422)

    @app.route("/questions")
    def get_questions():
        try:
            questions = Question.query.order_by(Question.id).all()
            current_questions = paginate_questions(request, questions)
            all_categories = Category.query.all()
            current_category = paginate_questions(request, all_categories)
            categories = {}
            for category in all_categories:
                categories[category.id] = category.type

            if len(current_questions) == 0:
                abort(404)


            return jsonify({
                "success": True,
                "questions": current_questions,
                "total_questions": len(Question.query.all()),
                "current_category": current_category,
                "categories": categories
            })
        except:
            db.session.rollback()
            abort(422)
        finally:
            db.session.cloe()

    @app.route("/question/<int:question_id>", methods=['DELETE'])
    def delete_question(question_id):
        try:
            question = Question.query.filter_by(Question.id==question_id).one_or_more()
            if question is None:
                abort(404)

            question.delete()
            remaining_questions = Question.query.order_by(Question.id).all()
            current_questions = paginate_questions(request, remaining_questions)

            return jsonify({
                "success": True,
                "deleted": question_id,
                "questions": current_questions,
                "total_questions": len(Question.query.all())
                })
        except:
            db.session.rollback()
            abort(422)
        finally:
            db.session.close()

    @app.route("/questions", methods=["POST"])
    def create_question():
        body = request.get_json()
        new_question = body.get("question", None)
        new_answer = body.get("answer", None)
        new_category = body.get("category", None)
        new_difficulty = body.get("difficulty", None)

        try:
            if new_question:
                question = Question(question=new_question, answer=new_answer, 
                                    category=new_category,difficulty=new_difficulty)
                question.insert()
                select_questions = Question.query.order_by(Question.id).all()
                current_questions = paginate_questions(request, select_questions)

                return jsonify({
                    "success": True,
                    "question_created": Question.id,
                    "Questions": current_questions,
                    "total_questions": len(Question.query.all())
                })
            else:
                abort(405)
        except:
            db.session.rollback()
            abort(422)
        finally:
            db.session.close()

    @app.route("/search", methods=["POST"])
    def search_question():
        try:
            body = request.get_json()
            search_question = body.get("search_question", None)
            
            if search_question:
                questions = Question.query.filter_by(Question.question).ilike(f'%{search_question}').all()
        
            return jsonify({
                "success": True,
                "questions": questions,
                "total_questions": len(questions),
            })
        except:
            db.session.rollback()
            abort(422)
        finally:
            db.session.close()


    @app.route("/categories/<int:category_id>/questions")
    def get_questions_by_category(category_id):
        try:
            categories = Category.query.filter_by(Category.id==category_id).one_or_none()
            questions = Question.query.all()
            categorised_questions = {}

            for category in categories:
                if category.type == questions.category:
                    categorised_questions.append(category)

            selected_questions = paginate_questions(request, categorised_questions)

            return jsonify({
                "success": True,
                "questions": selected_questions,
                "total_questions": len(categorised_questions),
                "current_category": categories.type
            })
        except:
            db.session.rollback()
            abort(404)
        finally:
            db.session.close()

    @app.route("/quiz_questions", methods=["POST"])
    def create_quizes():
        try:
            body = request.get_json()
            quiz_category = body.get("quiz_category", None)
            previous_question = body.get('previous_question')

            if quiz_category['type']:
                questions = Question.query.filtera((Question.id).notin_(previous_question)).all()
            else:
                questions= Question.query.filter(quiz_category=quiz_category['id']).filter(
                            Question.id.notin_(previous_question)).all()      

            return jsonify({
                "success": True,
                "question": questions,
            })
        except:
            db.session.rollback()
            abort(405)
        finally:
            db.session.close()


    @app.errorhandler(404)
    def not_found(error):
        return (
            jsonify({"success": False, "error": 404, "message": "resource not found"}),
            404,
        )

    @app.errorhandler(422)
    def unprocessable(error):
        return (
            jsonify({"success": False, "error": 422, "message": "unprocessable"}),
            422,
        )

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({"success": False, "error": 400, "message": "bad request"}), 400

    @app.errorhandler(405)
    def not_found(error):
        return (
            jsonify({"success": False, "error": 405, "message": "method not allowed"}),
            405,
        )

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            "success": False,
            'error': 500,
            "message": "Internal server error!"
        }), 500

    return app

