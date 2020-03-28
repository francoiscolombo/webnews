# WebNews

![build-backend](https://github.com/francoiscolombo/webnews/workflows/build-backend/badge.svg) ![build-frontend](https://github.com/francoiscolombo/webnews/workflows/build-frontend/badge.svg)

## What is this?

it is not a fake project like a voting application or something similar.

it does provide a nice looking application with the following features:

- geo location by IP
- retrieving the current weather regarding your location
- collecting news from several sources
- storing the news in a database
- display the news and the weather with a material design

## Why?

to have a full *realistic* project with complex components (backend, jobs, frontend) to test K8S deployments

and also having a template for Python API, Angular Frontend and Celery jobs.

## Design

the project contains 3 different components:

- `backend API` to store and retrieve the news, and the weather
- `jobs scheduler` because we want to retrieve the news in the background every 15mn
- `frontend` to display the news, with a material look and feel

### backend API

the backend API is written in Python and uses [Flask](https://flask.palletsprojects.com/en/1.1.x/) framework to expose the endpoints.

we are using [Flask-SQLAchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) and [Flask-Migrate](https://flask-migrate.readthedocs.io/en/latest/) for dealing with the database layer.

in order to be able to run the backend, you will have to create a `.env` file that contains your own [Rapid Api key](https://rapidapi.com/) because we need it for the weather API, and the geo location API.

the backend can be run in 2 modes: `development mode` which is the default one, and `production mode` that you can activate by setting the environment variable `PRODUCTION_MODE` to `yes`
in *production mode* the access to the API requires a *token* and an *app name* that you will have to register manually from the backend container with the following command:

```
$ flask auth add 'application name'
```

of course the backend must be running when you issue this command, or if you are running as docker container you have to connect to the container to run the command.

the token issued is valid for one year. after it ends, you will have to renews the token with this command:

```
$ flask auth renew 'application name'
```

by default the backend used a SQLlite database, but of course it is not what you have to use on a production environment.
to use a mysql database instead, you will have to set the variable `DATABASE_URL` in your .env file. see the [docker compose](docker-compose.yml) file for an example.
once you update the variable, you will have to tell Flask to migrate the database to the newly defined database with this command:

```
$ flask db upgrade
```

for the remaining, the code is self explanatory enough.

### the jobs scheduler

this part is also written in Python but this time we are using [Celery](http://www.celeryproject.org/) as the scheduler, with [Flower](https://flower.readthedocs.io/en/latest/) as the dashboard.

we select RabbitMQ as the broker support, but we could as well use Redis.

if you are running under windows as your dev platform, and using Windows containers instead of docker containers, this is a sample Dockerfile for building a RabbitMQ container easily:

```dockerfile
FROM mcr.microsoft.com/windows/servercore:1909 

ENV ERLANG_HOME="c:\\erlang"
ENV RABBITMQ_VERSION=3.6.15
ENV RABBITMQ_SERVER=C:\\rabbitmq_server-3.6.15

SHELL [ "powershell", "-command"]

COPY otp_win64_20.2.exe c:\\erlang_install.exe
COPY rabbitmq-server-windows-3.6.15.zip c:\\rabbitmq.zip

RUN Start-Process -Wait -FilePath "c:\\erlang_install.exe" -ArgumentList /S, /D=$env:ERLANG_HOME ; Remove-Item -Force -Path "C:\\erlang_install.exe" ;
RUN Expand-Archive -Path "c:\\rabbitmq.zip" -DestinationPath "c:\\" ; Remove-Item -Force -Path "c:\\rabbitmq.zip" ;
RUN $path = [Environment]::GetEnvironmentVariable('Path', 'Machine'); [Environment]::SetEnvironmentVariable('Path', $path + ';C:\rabbitmq_server-3.6.15\sbin', 'Machine')
RUN rabbitmq-plugins enable rabbitmq_management --offline

COPY rabbitmq.config C:\\Users\\ContainerAdministrator\\AppData\\Roaming\\RabbitMQ\\rabbitmq.config

ENTRYPOINT rabbitmq-server

EXPOSE 5672 15672
```

and you will need the binary packages from the RabbitMQ website, plus a (*rabbitmq.config*) file with this content:

```
[{rabbit, [{loopback_users, []}]}].
```

then build the container. once built you can run it with a command like:

```
C:\> docker run --rm --name rabbitmqtest rabbitmq -p 15672:15672 -p 5672:5672 -t rabbitmq
```

please note that you will have to retrieve the IP from the container with a docker inspect, and set the proper value for the environment variable `CELERY_BROKER_URL` in the `.env` file of the project.

otherwise, if you are using Linux, just use the docker-compose provided.

for running the scheduler without docker-compose you will have to use a `.env` file for hosting your environment variables, like for the backend.

however this time the environment variables that you will need are the following:

| variable | description | sample value |
| --- | --- | --- |
| NEWS_API_KEY | your [News API key](https://newsapi.org/) since it's our source for retrieving the news... | - | 
| JOBS_APP_NAME | your app name if the backend API does run on production mode | webnews.jobs |
| JOBS_APP_TOKEN | the associated token generated on the backend side | - |
| WEBNEWS_API_BASE_URL | the URL where you can find the backend API | http://127.0.0.1:5000/api/v1.0 |
| CELERY_BROKER_URL | the broker url for Celery (see the doc) | amqp://guest:guest@127.0.0.1:5672// |
| CELERY_BACKEND_URL | this must be the value `rpc://` | rpc:// |

then for running the scheduler you have to start a worker with the following command:

```
$ python scheduler.py start-worker
```

and if you want to use flower (which is advised) then run the following command:

```
$ python scheduler.py start-flower
```

you can now start a synchronize job with the command:

```
$ python scheduler.py synchronize
```

for now, it must be triggered manually, but this task is the only way to refresh the news database, so it should be executed periodically, like every 30mn for example.

### the frontend

the frontend is written in [Angular](https://angular.io/) and it uses [Angular material](https://material.angular.io/).

it is composed of 6 components and 2 stores:

- **the application by itself**, of course, will do the layout and import the other components
- **a category component**, display the news by categories (fixed for now) with a tab for each different category
- **a top stories component**, display a list of top stories on the left of the page
- **a latest news component**, uses a carousel to display the news, 10 by 10, with a button to load the next batch of news
- **a IP wan component**, uses an API to retrieve the WAN IP of the user, this IP is then used for geo location and retrieving the current weather for this location
- **a weather component**, simply query an API to retrieve the weather for the current location. this is done only when we load the page or refresh it.

then we are using 2 stores:

- **one for sharing the IP** between the IP WAN and weather component
- **one for storing the current page** for the latest news component

this is how it looks:

![screencap.png](screencap.png)

we also have something a little special for this project: the way we are implementing environment variables.

since we are going to build a docker container for this project, I needed a way to pass some environment variables to the container.
of course I'm not going to pass the values hardcoded. I need to pass some secret values, like API keys, and some values that will changes regarding the environment that we are deploying, like the backend API URL.

so I used this method to be able to uses OS environment variables from Angular...

1. install custom-webpack as dev dependency: `npm install -D @angular-builders/custom-webpack`. this allow to customize build configuration while staying inside the context of the Angular project.
2. the next step is to tell Angular to use the new builder. so we need to to modify `angular.json` and do this change:
```json
{
  "$schema": "./node_modules/@angular/cli/lib/config/schema.json",
  "version": 1,
  "newProjectRoot": "projects",
  "projects": {
    "webnews": {
...
      "architect": {
        "build": {
          "builder": "@angular-builders/custom-webpack:browser",
          "options": {
            "customWebpackConfig": {
              "path":"custom-webpack.config.js"
            },
...
```
3. and we add at the same level than the `angular.json` file a new file to describe the new configuration: [custom-webpack.config.js](frontend/webnews/custom-webpack.config.js).
actually, I'm creating a webpack plugin. and in this plugin, I'm reading the OS environment variables in order to be able to pass them to Angular, via webpack.
the environment variables are part of a map named *$ENV*, because it makes sense, correct?
4. then I need to type the variables. this is done in the [typing.d.ts](frontend/webnews/src/typing.d.ts) file.
5. then I just need to use the environment variables in my [environment.prod.ts](frontend/webnews/src/environments/environment.prod.ts)

that's all I need to register and use real environment variables inside Angular. smart, isn't it?

except this part, everything is quite straight forward in the code. just check, it is self explanatory.

to run the frontend locally on your dev workstation, simply use:

```
$ ng serve -o
```

### the docker compose stack

of course, every component have a Docker file, which allows to build a Docker image. you can find the docker file at the root of every component folder.

we also have a [docker compose](docker-compose.yml) file. as you can see if you open the file, this docker-compose file uses environment variables that you will have to set in a `.env` file, like for the backend and the scheduler.

this is the list of the variables you will need to provide:

- SECRET_KEY, a secret key used by the backend to generate the JWT token
- MYSQL_PASSWORD, well, you know
- NEWS_API_KEY, see the scheduler part
- X_RAPID_API_KEY, see the backend part
- JOBS_APP_NAME, id of the job application, most likely webnews.jobs
- JOBS_APP_TOKEN, the token generated by the backend
- FRONTEND_APP_NAME, id of the frontend application, most likely webnews.frontend
- FRONTEND_APP_TOKEN, then token generated by the backend

once you have it, just use:

```
$ docker-compose up -d
```

and it will run the services stack.
