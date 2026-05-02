import os

SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
SQLALCHEMY_TRACK_MODIFICATIONS = False


# here we are using environment variables to store our database URI,
# this is a good practice because it allows us to keep sensitive information out of our codebase and makes it easier to change the database URI without having to modify our code,
# we can set the environment variable in our terminal before running the app, for example: export SQLALCHEMY_DATABASE_URI="sqlite:///db.sqlite3" on Linux/Mac or set SQLALCHEMY_DATABASE_URI="sqlite:///db.sqlite3" on Windows