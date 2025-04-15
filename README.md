# Sych-assessment FasAPI server + RabbitMQ

## Overview
This project is a FastAPI server that works with a RabbitMQ container to handle ansychronous tasks. The server exposes an endpoint to receive messages, which are then sent to a RabbitMQ queue for processing.

## Installation
Ensure you have Docker and Docker Compose installed on your machine.

To start the application and its dependencies, simply run:

```bash
docker-compose up --build -d
```
### Routes
The routes for interacting with the server are as specified in the document.

### Queue technology
I initially implemented the server using a simple python queue, and then switched to RabbitMQ.


### Storage of scheduled tasks
For the storage of the scheduled tasks, I used a simple in-memory dictionary. This is not suitable for production, but it was allowed for the assessment. I did have to take care to make sure the dictionary was not recreated on each import from its file, as I thought the file would run on every import but I was wrong, so the Singleton pattern was not needed.

### Background task handler 
For the background task handler I simple used a separate thread, done as so:

### Type hints and Classes
I utilizes Pydantic in most of the classes, it helped greatly in validating the data and ensuring that the data being passed around was of the correct type. I used the typing library in a few places, as it helped me define a dictionary's key, although this could definitely have been done through Pydantic, not the best practice.

All the class models are defined in the `models.py` file.

### Docker
The project is containerized using Docker. The `docker-compose.yml` file defines the services required to run the application, including the FastAPI server and RabbitMQ.

The FastAPI server is built using the `Dockerfile` provided in the project root. The server is exposed on port 8080, and RabbitMQ is exposed on port 5672.

## Project Structure
```plaintext
.
├── app
│   ├── main.py 
│   ├── models.py
│   ├── predict.py
│   ├── rabbbit.py
│   └── prediction_results.py
│   └── background_task_runner.py
├── docker-compose.yml
├── Dockerfile
├── pyproject.toml
├── README.md
├── uv.lock
├── .gitignore
├── .python-version
└── .venv/

```
- `app/main.py`: The main entry point for the FastAPI server.
- `app/models.py`: Contains the Pydantic models/classes.
- `app/predict.py`: Contains the `mock_model_predict` function.
- `app/rabbit.py`: Contains the logic for connecting to RabbitMQ and sending messages to the queue.
- `app/prediction_results.py`: Makes the results dictionary.
- `app/background_task_runner.py`: Contains the logic related to the background task runner.

### Disclaimers
Plagirasm was strictly forbidden and so I did not use any help from any other persons. I obviously did use Google and LLM help on bugs and errors and finding out how to setup and use RabbitMQ as this was my first time using it.

Very minimal snippets of code were copied from LLMs, to the best of my knowledge these were:
-  The threading API function in python, I'm used this but didn't remember it exactly:
```python
# Starting the worker that handles the tasks in the backgroung
threading.Thread(target=predict_task_runner, daemon=True).start()
```
- The RabbitMQ/pika connection **retry** logic. This was because I only found out I needed this when I ran the app and rabbitMQ containers together and realized the rabbitMQ container took a few seconds to start up and the FastAPI server was trying to connect to it before it was ready..
- The initial connection code to RabbitMQ: 
```python
connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host))
channel = connection.channel()
channel.queue_declare(queue='sych-app-tasks')
```
- A large part of both the `docker-compose.yml` and `Dockerfile` were generated using LLM help, but the I faced numerous errors with them and had to fix them and change them to get them to work.
- Parts of this `README.md`, like the folder structure and project overview. This was simply done to save time and for aesthetics.

### Notes
- The project is designed to be run in a Docker container. Ensure you have Docker and Docker Compose installed on your machine.
- You can rum the FastAPI server locally by running (as long as you have uv, pip, and python installed):
```bash
PYTHONPATH=app/src uvicorn app.src.main:app --reload --host 0.0.0.0 --port 8080
# This assumes you are have a rabbitMQ server running on localhost:5672
```
- **The pika libarry is not thread safe**, it took me a while to realize that I had to use a separate channel connection for the background task thread and for the main app thread. 
