import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from tokens import assistant, director, executive

from app import create_app
from models import setup_db, Movie, Actor, db_drop_and_create_all

# Initializes headers based on roles

assistant_header = {
    'Authorization': assistant
}
director_header = {
    "Authorization": director
}
executive_header = {
    "Authorization": executive
}

class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        #os.environ['DATABASE_NAME'] = "cast_test"
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "cast"
        self.database_path = "postgresql://{}@{}/{}".format('postgres', 'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)
        db_drop_and_create_all()

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    
    def tearDown(self):
        """Executed after reach test"""
        pass

    # ------ TEST Actor ------ #

    # GET /actors , assistant 
    def test_get_actors_assistant(self):
        res = self.client().get('/actors', headers=assistant_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_actors'])
        self.assertTrue(len(data['actors']))

    # GET /actors, director
    def test_get_actors_director(self):
        res = self.client().get('/actors', headers=director_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_actors'])
        self.assertTrue(len(data['actors']))
    
    # GET /actors, unauthorized
    def test_401_get_actors(self):
        res = self.client().get('/actors')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'not authorized')

    # POST /actors, executive
    def test_create_actors_executive(self):
        self.new_actor = {
            'name': 'Bean',
            'age' : 50,
            'gender' : 'Male'
        }

        res = self.client().post('/actors', json=self.new_actor, headers=executive_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])
        self.assertTrue(data['total_actors'])

    # POST /actors, director, empty
    def test_400_create_invalid_actor(self):
        self.invalid_actor = {}

        res = self.client().post('/actors', json=self.invalid_actor, headers=director_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)

    # DELETE /actors, director
    def test_delete_actor_director(self):

        res = self.client().delete('/actors/1', headers=director_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 1)

    # DELETE /actors, assistant
    def test_403_delete_actor_assistant(self):

        res = self.client().delete('/actors/2', headers=assistant_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'not authorized')
    
    # PATCH /actors, executive
    def test_patch_actor_executive(self):
        self.updated_actor = {
            'name': 'Updated Person',
            'age' : 60,
            'gender' : 'Female'
        }
        res = self.client().patch('/actors/3', json=self.updated_actor, headers=executive_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['updated_actor'], 3)

    # PATCH /actors, director
    def test_404_update_non_existent_question(self):
        self.updated_actor = {
            'name': 'Updated Person',
            'age' : 60,
            'gender' : 'Female'
        }
        res = self.client().patch('/actors/10000', json=self.updated_actor, headers=director_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')


    # ------ TEST Movie ------ #

    # GET /movies , assistant 
    def test_get_movies_assistant(self):
        res = self.client().get('/movies', headers=assistant_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_movies'])
        self.assertTrue(len(data['movies']))
    
    # GET /movies, unauthorized
    def test_401_get_movies(self):
        res = self.client().get('/movies')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'not authorized')

    # POST /movies, executive
    def test_create_movie_executive(self):
        self.new_movie = {
            'title': 'Bean Goes Holiday',
            'release_date' : '1996 1 2'
        }

        res = self.client().post('/movies', json=self.new_movie, headers=executive_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])
        self.assertTrue(data['total_movies'])

    # POST /movies, director
    def test_403_create_movie(self):
        self.new_movie = {
            'title': 'Sad',
            'release_date': '1995 2 8'
        }
        res = self.client().post('/movies', json=self.new_movie, headers=director_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)

    # DELETE /movies, executive
    def test_delete_movie_executive(self):

        res = self.client().delete('/movies/1', headers=executive_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 1)

    # DELETE /movies, assistant
    def test_403_delete_movie_assistant(self):

        res = self.client().delete('/movies/2', headers=assistant_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'not authorized')
    
    # PATCH /movies, director
    def test_patch_movie_director(self):
        self.updated_movie = {
            'title': 'Up v2',
            'release_date' : '2999 1 2'
        }
        res = self.client().patch('/movies/1', json=self.updated_movie, headers=director_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['updated_movie'], 1)

    # PATCH /movies, executive
    def test_400_update_invalid_release_date(self):
        self.updated_movie = {
            'title': 'Updated Person',
            'release_date' : '2021/12/15'
        }
        res = self.client().patch('/movies/1', json=self.updated_movie, headers=executive_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request')

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()