FROM python:3.8.12-slim-buster

# YOUR COMMANDS HERE
# ....
# ....
WORKDIR /usr/src/app

# copy all the files to the container
COPY . .
RUN apt-get -y update && \
    apt-get -y instal python3.11
RUN pip3 install --no-cache-dir -r requirements.txt

CMD ["python3", "bot.py"]