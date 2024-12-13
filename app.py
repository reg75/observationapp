from flask import Flask
from app.routes import register_routes
from app.models import db, create_initial_data
from flasgger import Swagger

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///obsapp.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'very_secret_hidden_key'

db.init_app(app)
swagger = Swagger(app)


def create_tables():
   with app.app_context():
      db.create_all()
      create_initial_data()

create_tables()

register_routes(app)

if __name__ == "__main__":
   app.run(debug=True)