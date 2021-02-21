# social-network-api
## Table of contents
* [General info](#general-info)
* [Functionality](#functionality)
* [Setup](#setup)
* [Tests](#tests)

## General info
The app is a simple REST API for Social Network

## Functionality
- user signup
- user login
- post creation
- post like/unlike
- analytics about how many likes was made
- user activity

## Setup
To run this project locally, make the following:

```
$ git clone https://github.com/vladikkuzn/social-network-api
$ cd social-network-api
$ python3.8 -m venv env
$ source env/bin/activate
$ (env)$ pip install -r requirements.txt
$ (env)$ python manage.py migrate


## Tests
To run the tests ```python manage.py test ./api/tests/```