FROM python:3.11
# YOUR COMMANDS HERE
# ....
# ....
WORKDIR /usr/src/app

# copy all the files to the container
COPY . .
RUN apt-get -y update && \
    apt-get -y install python3.11
RUN pip3 install --no-cache-dir -r requirements.txt

CMD ["python3", "bot.py"]