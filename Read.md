create virtual environment
```bash
python -m venv .venv
```

activate virtual environment
```bash
source .venv/bin/activate
```

access virtual environment on windows
```bash
source .venv/bin/activate
``` 

deactivate virtual environment
```bash
deactivate
```

install dependencies
```bashbash
pip install -r requirements.txt
```

install flask
```bashbash
pip install flask
```

install python-dotenv
```bash
pip install python-dotenv
```



run flask app
```bashbash
export FLASK_APP=app.py
export FLASK_ENV=development
flask run
```

run flask app on windows
```bashbash
set FLASK_APP=app.py
set FLASK_ENV=development
flask run
```

create database table
```bashbash
flask shell
from app import db
db.create_all()
exit()
```

create database table on windows
```bash
flask shell
from app import db
db.create_all()
exit()
```

create table with flask-migrate
```bash
flask db init
flask db migrate -m "Initial migration."
flask db upgrade
```

create table using 
```bash
flask create_tables
```

run flask app with gunicorn
```bash
gunicorn -w 4 app:app
``` 