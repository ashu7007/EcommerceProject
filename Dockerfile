# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

WORKDIR /EcommerceProject/apps

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

ENV FLASK_APP=apps
ENV FLASK_ENV=development
ENV MAIL_USERNAME=avaish@deqode.com
ENV MAIL_PASSWORD=Ashutosh@007
ENV DATABASE_URL=postgresql://sdyfeipbuootgr:0a59a8ac47f990b0233279d18d1623d82120c449bb5e6f19cef3088d62e52427@ec2-44-193-178-122.compute-1.amazonaws.com:5432/da3043ab1s4rca

# CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
CMD gunicorn wsgi:app

