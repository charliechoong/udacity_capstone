## Backend - Full Stack Casting Agency API 

### Motivation

This application allows managers and directors to manage movies and actors, with differing permissions. It also grants casting assistants the ability to view the movies and actors.

### Installing Dependencies

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)


2. **Virtual Enviornment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)


3. **PIP Dependencies** - Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:
```bash
pip install -r requirements.txt
```
This will install all of the required packages we selected within the `requirements.txt` file.


4. **Key Dependencies**
 - [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

 - [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

 - [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 


### Running the server

From within the `./starter` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.


## API Documentation

This section documents all the endpoints. For each endpoint, it explains the methods used, request arguments and sample response.

1. GET '/actors'
- Fetches actors.
- Request Arguments: `None`
- Returns: 
    - Success State: `bool`
    - Actors: `list of dictionaries`
    - Total number of actors: `int`

**Sample Response:**
```
response = {
    "actors": [
        {
            "age": "22",
            "gender": "Female",
            "id": 1,
            "name": "Jynn Shen"
        },
        {
            "age": "27",
            "gender": "Male",
            "id": 2,
            "name": "Ethan Tam"
        },
        {
            "age": "22",
            "gender": "Female",
            "id": 3,
            "name": "Gloria Tan"
        }
    ],
    "success": true,
    "total_actors": 3
}
    
```

2. POST '/actors'
- Create a new actor.
- Request Arguments: `name` (type: `string`), `age` (type: `int`), `gender` (type: `string`)

**Sample Request:**
```
{
    "name": "James teo",
    "age": 35,
    "gender": "Male"
}
```
- Returns: 
    - Success status: `bool`
    - ID of actor created: `int`
    - Total number of actors: `int`

**Sample Response:**
```
response = {
    "created": 4,
    "success": true,
    "total_actors": 4
}
```

3. DELETE '/actors/<int:actor_id>'
- Deletes a specific actor using `actor_id`.
- Request Arguments: `None`
- Returns:
    - Success status: `bool`
    - ID of deleted actor: `int`
    - Total number of actors: `int`

**Sample Response:**
```
response = {
    "deleted": 4,
    "success": true,
    "total_actors": 3
}
```

4. PATCH '/actors/<int:actor_id>'
- Updates an existing actor.
- Request Arguments: `name` (type: `string`, optional), `age` (type: `int`, optional), `gender` (type: `string`, optional)

**Sample Request:**
```
{
    "age": 100
}
```
- Returns:
    - Success status: `bool`
    - ID of updated actor: `int`

**Sample Response:**
```
response = {
    "success": true,
    "updated_actor": 2
}
```

5. GET '/movies'
- Fetches movies.
- Request Arguments: `None`
- Returns: 
    - Success State: `bool`
    - Movies: `list of dictionaries`
    - Total number of movies: `int`

**Sample Response:**
```
response = {
    "movies": [
        {
            "id": 1,
            "release_date": "Wed, 01 Jan 2020 00:00:00 GMT",
            "title": "The Cult of Shincheonji"
        },
        {
            "id": 2,
            "release_date": "Fri, 30 Apr 2021 00:00:00 GMT",
            "title": "Up"
        }
    ],
    "success": true,
    "total_movies": 2
}
    
```

6. POST '/movies'
- Create a new movie.
- Request Arguments: `title` (type: `string`), `release_date` (type: `string`)

**Note:** `release_date` must be of format `"Y M D"` where `Y` is year, `M` is month and `D` is day.

**Sample Request:**
```
{
    "title": "Mobile Legends",
    "release_date": "1859 2 15" 
}
```
- Returns: 
    - Success status: `bool`
    - ID of movie created: `int`
    - Total number of movies: `int`

**Sample Response:**
```
response = {
    "created": 3,
    "success": true,
    "total_movies": 3
}
```

7. DELETE '/movies/<int:movie_id>'
- Deletes a specific movie using `movie_id`.
- Request Arguments: `None`
- Returns:
    - Success status: `bool`
    - ID of deleted movie: `int`
    - Total number of movies: `int`

**Sample Response:**
```
response = {
    "deleted": 3,
    "success": true,
    "total_movies": 2
}
```

8. PATCH '/movies/<int:movie_id>'
- Updates an existing movie.
- Request Arguments: `title` (type: `string`, optional), `release_date` (type: `int`, optional)

**Sample Request:**
```
{
    "release_date": "2025 6 16"
}
```
- Returns:
    - Success status: `bool`
    - ID of updated movie: `int`

**Sample Response:**
```
response = {
    "success": true,
    "updated_movie": 2
}
```


## Testing
Tests have been created to test each endpoint and role.

To run the tests, run
```
dropdb -U postgres cast
createdb -U postgres cast
python test_app.py
```

## JWT Tokens

There are 3 roles, which hold different permissions:

1. Casting Assistant
    - Permissions:
        - `get:actors`
        - `get:movies`

2. Casting Director
    - Permissions:
        - `get:actors`
        - `post:actors`
        - `delete:actors`
        - `patch:actors`
        - `get:movies`
        - `patch:movies`

3. Executive Producer
    - Permissions:
        - `get:actors`
        - `post:actors`
        - `delete:actors`
        - `patch:actors`
        - `get:movies`
        - `post:movies`
        - `delete:movies`
        - `patch:movies`

**Secret (Shhh...):** The tokens for each role can be found under `tokens.py`.

## Testing API (only with provided JWT tokens)

**APP is delopyed at** https://charliecastagency.herokuapp.com/

With the provided tokens in `tokens.py`, you may test using Postman by inserting the tokens into Authorization tab and manually testing out the various API using the sample requests documented above, or any valid requests.

Also, the auth0 information can be found in `auth.py`.
