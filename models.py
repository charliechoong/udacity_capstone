from sqlalchemy import Column, String, Integer, Date, create_engine
from flask_sqlalchemy import SQLAlchemy
from datetime import date
import json
import os 

database_name = os.environ.get('DATABASE_NAME', 'cast')
database_path = os.environ.get('DATABASE_URL', "postgres://{}@{}/{}".format('postgres', 'localhost:5432', database_name))
if not database_path.startswith('postgresql'):
  database_path = database_path.replace("://", "ql://", 1)


db = SQLAlchemy()

def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()

def db_drop_and_create_all():
    db.drop_all()
    db.create_all()

    # populate with dummy data
    movie = Movie(
        title='The Cult of Shincheonji',
        release_date=date(2020, 1, 1)
    )
    movie.insert()

    movie = Movie(
        title='Up',
        release_date=date.today()
    )
    movie.insert()

    actor = Actor(
        name='Jynn Shen',
        age=22,
        gender='Female'
    )
    actor.insert()

    actor = Actor(
        name='Ethan Tam',
        age=27,
        gender='Male'
    )
    actor.insert()

    actor = Actor(
        name='Gloria Tan',
        age=22,
        gender='Female'
    )
    actor.insert()

'''
Movie
Have title and release date
'''
class Movie(db.Model):  
  __tablename__ = 'movies'

  id = Column(Integer, primary_key=True)
  title = Column(String)
  release_date = Column(Date)

  def __init__(self, title, release_date):
    self.title = title
    self.release_date = release_date

  def insert(self):
    db.session.add(self)
    db.session.commit()
  
  def update(self):
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

  def format(self):
    return {
      'id': self.id,
      'title': self.title,
      'release_date': self.release_date}

'''
Actor
Have name, age and gender
'''
class Actor(db.Model):  
  __tablename__ = 'actors'

  id = Column(Integer, primary_key=True)
  name = Column(String)
  age = Column(String)
  gender = Column(String)

  def __init__(self, name, age, gender):
    self.name = name
    self.age = age
    self.gender = gender

  def insert(self):
    db.session.add(self)
    db.session.commit()
  
  def update(self):
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

  def format(self):
    return {
      'id': self.id,
      'name': self.name,
      'age': self.age,
      'gender': self.gender}
