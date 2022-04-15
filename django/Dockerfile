# Pull base image
FROM python:3.9

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /code

# Install dependencies
COPY requirements.txt /code/
RUN python3 -m pip install -r  --system /code/requirements.txt

# Copy project
COPY . /code/

# Run migration just in case
RUN python3 /code/manage.py makemigrations 
RUN python3 /code/manage.py migrate

# # Serve
# CMD python3 /code/manage.py run_server