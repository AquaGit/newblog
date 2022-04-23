from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)


class ArticleModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    views = db.Column(db.Integer, nullable=False)
    likes = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Article(name = {name}, views = {views}, likes = {likes})"


article_put_args = reqparse.RequestParser()
article_put_args.add_argument(
    "name", type=str, help="Name Article", required=True)
article_put_args.add_argument(
    "likes", type=int, help="Likes Article", required=True)
article_put_args.add_argument(
    "views", type=int, help="Views Article", required=True)

article_update_args = reqparse.RequestParser()
article_update_args.add_argument(
    "name", type=str, help="Name Article")
article_update_args.add_argument(
    "likes", type=int, help="Likes Article")
article_update_args.add_argument(
    "views", type=int, help="Views Article")

resource_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'views': fields.Integer,
    'likes': fields.Integer
}


class Article(Resource):
    @marshal_with(resource_fields)
    def get(self, article_id):
        result = ArticleModel.query.filter_by(id=article_id).first()
        if not result:
            abort(404, message="Could not find article with that id")
        return result

    @marshal_with(resource_fields)
    def put(self, article_id):
        args = article_put_args.parse_args()
        result = ArticleModel.query.filter_by(id=article_id).first()
        if result:
            abort(409, message="Article id taken...")

        article = ArticleModel(
            id=article_id, name=args['name'], views=args['views'], likes=args['likes'])
        db.session.add(article)
        db.session.commit()
        return article, 201

    @marshal_with(resource_fields)
    def patch(self, article_id):
        args = article_update_args.parse_args()
        result = ArticleModel.query.filter_by(id=article_id).first()
        if not result:
            abort(404, message="Article doesn't exist, cannot update")

        if args['name']:
            result.name = args = ['name']
        if args['views']:
            result.views = args = ['views']
        if args['likes']:
            result.likes = args = ['likes']

        db.session.commit()

        return result

    def delete(self, article_id):
        abort_if_article_id_doesnt_exist(article_id)
        del articles[article_id]
        return '', 204


api.add_resource(Article, "/article/<int:article_id>")

if __name__ == "__main__":
    app.run(debug=True)
