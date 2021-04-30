import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import date
from models import Movie, Actor, setup_db, db_drop_and_create_all
from auth import AuthError, requires_auth


def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  # Re-initialize database data
  db_drop_and_create_all()

  CORS(app)
  
  @app.after_request
  def after_request(response):
      response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
      response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
      return response
  
  @app.route('/')
  def get_greeting():
      greeting = "Welcome to the Casting Agency Management Site!" 
      return greeting

  @app.route('/actors', methods=['GET'])
  @requires_auth('get:actors')
  def get_actors(payload):
    actors = Actor.query.order_by(Actor.id).all()
    formatted_actors = [actor.format() for actor in actors]

    if len(formatted_actors) == 0:
      abort(404)

    return jsonify({
      'success': True,
      'actors': formatted_actors,
      'total_actors': len(formatted_actors)
    })

  @app.route('/actors/<int:actor_id>', methods=['DELETE'])
  @requires_auth('delete:actors')
  def delete_actor(payload, actor_id):
    try:
      actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
      if actor is None:
        abort(404)
      
      actor.delete()

      return jsonify({
        'success': True,
        'deleted': actor_id,
        'total_actors': len(Actor.query.all())
      })
    
    except:
      abort(422)

  @app.route('/actors', methods=['POST'])
  @requires_auth('post:actors')
  def create_actor(payload):
    body = request.get_json()
    if not body:
      abort(400, {'message': 'No data provided.'})
      
    new_name = body.get('name', None)
    new_age = body.get('age', None)
    new_gender = body.get('gender', None)

    if not (new_name and new_age and new_gender):
      abort(400, {'message': 'At least one of parameters is not specified.'})

    try:
      actor = Actor(
        name = new_name,
        age = new_age,
        gender = new_gender
      )

      actor.insert()

      return jsonify({
        'success': True,
        'created': actor.id,
        'total_actors': len(Actor.query.all())
      })

    except:
      abort(422)

  @app.route('/actors/<int:actor_id>', methods=['PATCH'])
  @requires_auth('patch:actors')
  def update_actor(payload, actor_id):
    body = request.get_json()
    if not body:
      abort(400)
    
    actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
    if actor is None:
      abort(404)
    
    name = body.get('name', None)
    age = body.get('age', None)
    gender = body.get('gender', None)

    if name:
      actor.name = name
    if age:
      actor.age = age
    if gender:
      actor.gender = gender
    
    actor.update()

    return jsonify({
      'success': True,
      'updated_actor': actor.id 
    })

  @app.route('/movies', methods=['GET'])
  @requires_auth('get:movies')
  def get_movies(payload):
    movies = Movie.query.order_by(Movie.id).all()
    formatted_movies = [movie.format() for movie in movies]

    if len(formatted_movies) == 0:
      abort(404)

    return jsonify({
      'success': True,
      'movies': formatted_movies,
      'total_movies': len(formatted_movies)
    })

  @app.route('/movies/<int:movie_id>', methods=['DELETE'])
  @requires_auth('delete:movies')
  def delete_movie(payload, movie_id):
    try:
      movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
      if movie is None:
        abort(404)
      
      movie.delete()

      return jsonify({
        'success': True,
        'deleted': movie_id,
        'total_movies': len(Movie.query.all())
      })
    
    except:
      abort(422)

  @app.route('/movies', methods=['POST'])
  @requires_auth('post:movies')
  def create_movie(payload):
    body = request.get_json()
    if not body:
      abort(400, {'message': 'No data provided.'})
      
    # For question creation
    new_title = body.get('title', None)
    new_release_date = body.get('release_date', None)

    if not (new_title and new_release_date):
      abort(400, {'message': 'At least one of parameters is not specified.'})

    # Process date
    try:
      split = new_release_date.split()
      year = int(split[0])
      month = int(split[1])
      day = int(split[2])
    except:
      abort(400, {'message': 'Inputted date has issues.'})

    try:
      movie = Movie(
        title = new_title,
        release_date = date(year, month, day)
      )

      movie.insert()

      return jsonify({
        'success': True,
        'created': movie.id,
        'total_movies': len(Movie.query.all())
      })

    except:
      abort(422)

  @app.route('/movies/<int:movie_id>', methods=['PATCH'])
  @requires_auth('patch:movies')
  def update_movie(payload, movie_id):
    body = request.get_json()
    if not body:
      abort(400)
    
    movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
    if movie is None:
      abort(404)
    
    title = body.get('title', None)
    release_date = body.get('release_date', None)

    if title:
      movie.title = title
    if release_date:
      try:
        split = release_date.split()
        year = int(split[0])
        month = int(split[1])
        day = int(split[2])
        movie.release_date = date(year, month, day)
      except:
        abort(400, {'message': 'Inputted date has issues.'})
    
    movie.update()

    return jsonify({
      'success': True,
      'updated_movie': movie.id 
    })

  # Error handling

  @app.errorhandler(422)
  def unprocessable(error):
      return jsonify({
          "success": False,
          "error": 422,
          "message": "unprocessable"
      }), 422

  @app.errorhandler(400)
  def bad_request(error):
      return jsonify({
        "success": False,
        "error": 400,
        "message": "bad request"
      }), 400

  @app.errorhandler(404)
  def not_found(error):
      return jsonify({
        "success": False,
        "error": 404,
        "message": "resource not found"
      }), 404
  
  @app.errorhandler(AuthError)
  def unauthorized(AuthError):
      return jsonify({
          "success": False,
          "error": AuthError.status_code,
          "message": "not authorized"
      }), AuthError.status_code
  

  return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)



