#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Newsletter

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///newsletters.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)


class Index(Resource):

    def get(self):

        response_dict = {
            "index": "Welcome to the Newsletter RESTful API",
        }

        response = make_response(
            jsonify(response_dict),
            200
        )

        return response


api.add_resource(Index, '/')


class Newsletters(Resource):

    def get(self):
        response_dict_list = [newsletter.to_dict()
                              for newsletter in Newsletter.query.all()]

        return make_response(jsonify(response_dict_list), 200)

    def post(self):

        new_record = Newsletter(
            title=request.form["title"],
            body=request.form["body"]
        )

        db.session.add(new_record)
        db.session.commit()

        response_dict = new_record.to_dict()

        return make_response(
            jsonify(response_dict),
            201
        )


api.add_resource(Newsletters, "/newsletters")


class NewsletterById(Resource):

    def get(self, id):
        response_dict = Newsletter.query.filter_by(id=id).first().to_dict()
        return make_response(jsonify(response_dict), 200)

    def patch(self, id):
        newsletter = Newsletter.query.filter_by(id=id).first()
        for attr in request.form:
            setattr(newsletter, attr, request.form.get(attr))
            db.session.add(newsletter)
            db.session.commit()

            newsletter_dict = newsletter.to_dict()

            return make_response(jsonify(newsletter_dict), 200)

    def delete(self, id):
        newsletter = Newsletter.query.filter_by(id=id).first()
        db.session.delete(newsletter)
        db.session.commit()

        return make_response(["Newsleter deleted"], 200)


api.add_resource(NewsletterById, "/newsletters/<int:id>")
