# Use an official Python runtime as a parent image
FROM python:3.6-slim

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt
RUN pip install gunicorn

# make entrypoint executable
RUN chmod +x boot.sh

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variables
ENV FLASK_APP flask_app.py
ENV GITHUB_CLIENT_ID 88b0968d095d8a22dad1

# entrypoint when container is run
ENTRYPOINT ["./boot.sh"]