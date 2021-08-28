# Use an existing docker image as a base
FROM python:3.8-slim-buster

# Set the working directory
WORKDIR /code

# Building the python environment
COPY requirements.txt requirements.txt
RUN  pip install -r requirements.txt

# Copying the python scripts for future execution
COPY ./*.py ./
COPY config.ini .

# Creating a directory for storing crawler logs
RUN mkdir logs

# Running the main crawler script
CMD [ "python", "main.py"]