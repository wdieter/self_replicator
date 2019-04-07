## Introduction

This repository contains a web application that will copy it's source code to your github profile.
The application triggers an [OAuth authentication flow](https://stackoverflow.com/questions/4727226/on-a-high-level-how-does-oauth-2-work)
to get access to the user's github.
This means the user will never provide their password to the application, and only needs to sign in to github.

## Software requirements 

To run application locally, download docker for desktop here: https://www.docker.com/products/docker-desktop

You can test that your installation is working by running the following in the terminal:

``docker run hello-world``

## Running the application on local machine

Only two commands are needed to run the application: 
````
docker build --tag=self_rep .
````
followed by
````
self_generating_repo wolf$ docker run -e GITHUB_CLIENT_SECRET='30183c211388ce8f58ab296e32437c498ffe481f' -e APP_SECRET_KEY='secretkey123' -p 4000:80 self_rep
````
To test if the application is running open http://localhost:4000/.
You should see a message and a link to copy the repository to your github
