FROM node:8-alpine as builder

WORKDIR /frontend

COPY ./frontend/package*.json ./

RUN npm set progress=false && npm config set depth 0 && npm cache clean --force

RUN npm i && mkdir /ng-app && cp -R ./node_modules ./ng-app

COPY ./frontend/ .

RUN $(npm bin)/ng build --prod --build-optimizer --base-href /f/


FROM python:3.7-slim

EXPOSE 80

ENV MYSQL_PORT 3306
ENV CROSS_ORIGIN True
ENV DEBUG False

WORKDIR /app

ADD . /app/

COPY --from=builder /frontend/dist/frontend/ /app/frontend/dist/frontend

RUN apt-get update && apt-get install -y gcc build-essential libpq-dev libffi-dev wkhtmltopdf wget xfonts-75dpi

RUN wget https://github.com/wkhtmltopdf/wkhtmltopdf/releases/download/0.12.5/wkhtmltox_0.12.5-1.stretch_amd64.deb
RUN dpkg -i wkhtmltox_0.12.5-1.stretch_amd64.deb
RUN apt-get install -f
RUN cp /usr/local/bin/wkhtmlto* /usr/bin/

RUN pip install pipenv
RUN pipenv run pip install pip==18.0
RUN pipenv install

CMD pipenv run prod
