FROM ubuntu:20.04

# Set an environment variable for python to look up if it is in a container or not
ENV WITHIN_DOCKER_CONTAINER=True

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Disable prompts from apt
ENV DEBIAN_FRONTEND=noninteractive

# Install Python 3.8 and pip
RUN apt-get update && apt-get install -y \
    python3.8 python3-pip

# Install dependencies and some useful tools
RUN apt-get update && apt-get install -y \
    nano curl sudo git bzip2 ca-certificates build-essential wget

# Add Google Chrome repository and install Google Chrome
RUN apt -f install -y
RUN wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN apt-get install ./google-chrome-stable_current_amd64.deb -y

# Set environment variables
ENV CHROME_BIN=/usr/bin/google-chrome
ENV CHROMEDRIVER_PATH=/usr/bin/chromedriver

# Install dependencies:
COPY requirements.txt .
RUN python3 -m pip install --upgrade pip
RUN pip install --upgrade setuptools
RUN pip install --default-timeout=240 -r requirements.txt

# Copy the app from local machine to the container
WORKDIR /app
COPY . /app

# Expose port 7000
EXPOSE 7000

# Run the app
CMD ["python3", "main.py", "--api"]