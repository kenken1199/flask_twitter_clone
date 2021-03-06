from flask import Flask
from flask_sqlalchemy  import SQLAlchemy
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config.from_object('project.config')
bcrypt = Bcrypt(app)
db = SQLAlchemy(app)

from project.users.views import users_blueprint
from project.tweets.views import tweets_blueprint

app.register_blueprint(users_blueprint)
app.register_blueprint(tweets_blueprint)

