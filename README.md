## Installation

1. clone the repository

2. Go to the root project

3. Set up virtualenv

```shell
python3 -m venv env
source env/bin/activate
pip3 install -r requirements.txt
```

4. create .env file in root project with value as follow:

SECRET_KEY=PUT_YOUR_SECRET_KEY_HERE
CALLBACK_URL="http://localhost:3001/callback"

## How to use
1. from root project, run local server with command (we need to use 127.0.0.1:3001 for callback):

```shell
python3 manage.py runserver 127.0.0.1:3001
```

2. To get authorise url, you can run curl as follow:

```shell
curl -X GET "http://127.0.0.1:3001"
```

3. You'll get response with key url & state. Then you can copy the value from key url and open it in your browser and follow instructions. After clicking on the "I Agree" button, you'll be redirected back to a callback URL like this: http://localhost:3001/callback?code=myinfo-com-NlZPurlLUH79euT2I0xT6dFnY0lbf5oNVAhNVo8U

4. To get person data you can copy value from key state at step 2 to auth_state in CURL and copy GET parameter "code" from step 3 to auth_code in CURL as request data body CURL to http://127.0.0.1:3001, with example as follow:

```shell
curl -X POST -H "Content-Type: application/json" -d '{"auth_code": "myinfo-com-cxVjud2BoquAZOuIXYh6wqaTTSXaUHONCn7jz1oK", "auth_state": "I9CGXZtZxuWN088e"}' http://127.0.0.1:3001
```

## Running unit test

1. To run for django app

```shell
python3 manage.py test
```

2. To run unit test for package myinfo. Go to myinfo folder then execute:

```shell
python3 -m pytest
```

## Reference

You may refer to the following screen recording of a Sample React Native app powered by Django REST Framework APIs
https://drive.google.com/file/d/1Lj6hFGjuC2R3AXSTDvVWBAnW4bNRLl1j/view?usp=sharing for reference.
