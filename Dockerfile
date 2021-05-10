# Use an official Python runtime as a parent image (image to start)
FROM python:3-slim-buster

ENV PYTHONUNBUFFERED=1

# Set the working directory to /app
WORKDIR /survey_project

RUN pip install --upgrade pip

COPY requirements.txt /survey_project/

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . .
# Make port 80 available to the world outside this container
#EXPOSE 8000

# CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]