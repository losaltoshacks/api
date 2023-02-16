# Start from the official Python base image.
FROM python:3.11

# Setup env
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1

# Allow statements and log messages to immediately appear in the Knative logs
ENV PYTHONUNBUFFERED 1

# Set the current working directory to /code.
WORKDIR /code

# Install pipenv
RUN pip install pipenv

# Install python dependencies in /.venv
COPY ./Pipfile /code/Pipfile
COPY ./Pipfile.lock /code/Pipfile.lock
RUN python -m pip install --upgrade pip
RUN pip install pipenv && pipenv install --dev --system --deploy

# 
COPY ./app /code/app

# Timeout is set to 0 to disable the timeouts of the workers to allow Cloud Run to handle instance scaling.
CMD ["uvicorn", "app.main:app", "--proxy-headers", "--port", $PORT, "--timeout", "0", "--workers", "1", "--threads", "8"]