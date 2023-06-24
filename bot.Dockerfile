FROM python:3.11
# YOUR COMMANDS HERE
# ....
# ....
WORKDIR /usr/src/app

# copy all the files to the container
COPY . .
RUN apt-get update && apt-get install awscli vim -y
ENV AWS_ACCESS_KEY_ID=AKIAQI7GRHZBX72Y72ME
ENV AWS_SECRET_ACCESS_KEY=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
ENV AWS_DEFAULT_REGION=us-west-1


RUN pip3 install --no-cache-dir -r requirements.txt

CMD ["python3", "bot.py"]