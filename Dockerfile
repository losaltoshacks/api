# Start from the official Python base image.
FROM python:3.11

# Setup env
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1

# Set the current working directory to /code.
WORKDIR /code

# Install pipenv
RUN pip install pipenv

# Install python dependencies in /.venv
COPY ./Pipfile /code/Pipfile
COPY ./Pipfile.lock /code/Pipfile.lock
RUN python -m pip install --upgrade pip
RUN pip install pipenv && pipenv install --system --deploy

# 
COPY ./app /code/app

# 
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]