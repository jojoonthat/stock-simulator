# Stock Simulator

## Setup
```sh
$ cd server

# Python virtual env
$ python -m venv venv
$ source ./venv/bin/activate

# Install flask stuff and pytest
$ pip install -r requirements.txt

# Run dev server, start simulation
$ FLASK_APP=server flask run
```

```sh
$ cd client

# React deps
$ npm ci

# Run dev server
$ npm start
```

Go to localhost:3000, adjust market sentiment, and watch the market react!
