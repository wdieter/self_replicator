## Project goals: 

_The result of your work should be an URL to an application. 
The application behind the URL should request access to the user's GitHub profile and create a repository
 with its own (application's) code._
_The application should not ask for the users's password or require access to  user's private repositories._

_Technical document: Technical specification document describing what the application does and how._


## Overview of application: 
#### Functionality:
The application consists of a flask application running inside a Docker container. 
The flask application guides the user through an OAuth authentication flow. 
Once the user has granted the application access to the user's github, the application forks a repository from github
to the authenticated user's github profile. 


#### Rationale behind choices of tools: 
- Flask: simple lightweight web app service that can serve as a quick prototype and also work in production.
- Docker: Allows for a consistent running environment and access to the correct library versions. 
This is advantageous for running locally for many users, and also for running in production. 
- Gunicorn: a simple WSGI HTTP Server that is ready for production use.
- OAuth was chosen so that the application would not require the password of the user in order to access their github. 


#### Notes / TODOs for moving to production: 
- Callback url needs to match the url given in the app settings on github. This url would need to change when moving to
production as the domain name will not be 'localhost'.
- Environment variables are currently stored as plaintext in the repository readme, namely `GITHUB_CLIENT_SECRET` and 
`APP_SECRET_KEY`. With regards to environment variables, no changes should be required to the app when moving to
 production setting, environment variables just need to be passed in at runtime. 
- https needs to be enabled, currently serving http, which could be a security risk. 
- Unit testing for both the endpoints and the api functions.