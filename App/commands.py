import click
from flask.cli import with_appcontext
from flask_sqlalchemy import SQLAlchemy
from flask import Blueprint

from models import Hotels, Brief_explanations, Aspects_hotels, Comments, Preferences, Feature_category, Reviews, \
    Actions

db = SQLAlchemy()

bp = Blueprint('create_tables', __name__)


@click.command(name='create_tables')
#@bp.cli.command(name='create_tables')
@with_appcontext
def create_tables():
    print("i will create tables")
    db.create_all()
    print("i created tables")
