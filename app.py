from flask import Flask
import os
from dotenv import load_dotenv
from database import db
import models
from flask_graphql import GraphQLView
import graphene
from schema import Query, Mutation

load_dotenv()
DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://root:{DATABASE_PASSWORD}@localhost/dashboard_db'
db.init_app(app)

schema = graphene.Schema(query=Query,mutation=Mutation)

app.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view('graphql',schema=schema, graphiql=True)
)

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)