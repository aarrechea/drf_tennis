FROM python:3.9-alpine3.13
LABEL maintainer="any.com"

# Ensures that Python output is sent straight to terminal without being buffered first
ENV PYTHONUNBUFFERED=1 

# Install dependencies. --no-cache to reduce image size.
# Copy requirements files and app code.
COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
COPY ./app /app
WORKDIR /app
EXPOSE 8000

# Create a virtual environment and install dependencies.
# rm to clean up temporary files.
# Use a non-root user to run our application
ARG DEV=false
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    if [ $DEV = "true" ] ; \
        then /py/bin/pip install -r /tmp/requirements.dev.txt ; \
    fi && \
    rm -rf /tmp && \
    adduser \
        --disabled-password \
        --no-create-home \
        django-user

# Set PATH to use the virtualenv
ENV PATH="/py/bin:$PATH"        

# Switch to a non-root user
USER django-user






