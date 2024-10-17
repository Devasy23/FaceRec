from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Initialize SQLAlchemy and Migrate
db = SQLAlchemy()
migrate = Migrate()

def init_db(app):
    """Initialize the database with the Flask app."""
    db.init_app(app)
    migrate.init_app(app, db)
