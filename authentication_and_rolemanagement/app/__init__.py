from app import auth, routes
from datetime import timedelta

from flask import Flask
from flask_jwt_extended import JWTManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

# Initialize the app and config
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.config["SECRET_KEY"] = "super-secret"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=30)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)

# Initialize database, JWT, migrations, rate limiting
db = SQLAlchemy(app)
jwt = JWTManager(app)
migrate = Migrate(app, db)
limiter = Limiter(app, key_func=get_remote_address)

# Blacklist for revoked tokens
blacklist = set()


@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload):
    return jwt_payload["jti"] in blacklist


# Import routes
