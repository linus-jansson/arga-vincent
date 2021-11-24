#!/bin/bash
FROM python:3.8-buster
# FROM node:10

# Setting workdir to /bot
WORKDIR /bot

# Copying everything into workdir
COPY . .

RUN python -m pip install -r requirements.txt

# DEBUG
RUN ls

# Starting script

CMD ["python", "bot.py"]