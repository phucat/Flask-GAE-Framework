#Flask - GAE Boilerplate

The Goal is to quickly and easily implement a backend framework that contains all necessary structures configurations and automation designed for Google Appengine and Bitbucket pipelines for rapid development.

## Directory Structure
- root/
- - app/ (contains all project related codes)
- - - components/ (contains classes that is used across modules)
- - - modules/ (contains blueprint, model and module related services)
- - - services/ (contains services that are used across modules)
- - exceptions.py (should contain all custom exception used in the project)
- - util.py (contains snippets or methods that is used across classes)
- - configurations/ (configuration files for each environment)
- - tests/ (contains test files)
- - tools/ (contains scripts or tools to help on development)
- - app.yaml (appengine required files that defines your service)
- - appengine_config.py (tells appengine the path of libraries the project is using)
- - bitbucket-pipelines (for CI automation)
- - deploy.sh (a script to deploy your project easily)
- - local_requirements.txt (contains the required libraries to run your project locally)
- - main.py (the entry point of application used by Flask)
- - requirements.txt (contains only libraries that are needed when deploying to appengine)
- - run_local.sh (a script that will automate your local deployment)


## System Requirements
- python 2.7
- vitualenv 15.0.3 or higher
- pip 9.0.1 or higher
- setuptools

## How to run locally:
On your terminal:
```
virtualenv venv

. venv/bin/activate
pip install -r local_requirements.txt
pip install -r requirements.txt -t lib
./update-commons.sh

./run_local.sh
```
Note: run_local.sh will also run the nosetest
## How to deploy
> ./deploy [environment] [version]

The [environment] value will automatically map the files inside the 'configurations' folder and will load your environment settings
## How to import commons library

Create a **.pypirc** file and save it on your **root home directory**
On **.pypirc** file, paste the codes below:
```
[distutils]
index-servers =
  pypi
  dev-pypi

[pypi]
username:<your_pypi_username>
password:<your_pypi_passwd>

[dev-pypi]
repository: http://104.199.50.195:8080/
username: phucat
password: 111111
```

Restart your terminal
> exec restart

On the project's root directory, type:
> ./update-commons.sh

## Activating specific service account on you local machine
> gcloud auth activate-service-account [ACCOUNT] --key-file [path to json key file]

full example:
> gcloud auth activate-service-account cs-development-playground@appspot.gserviceaccount.com --key-file credentials/cs-development-playground.json

https://cloud.google.com/sdk/gcloud/reference/auth/activate-service-account

## To temporarily use your own user credentials, run:
> gcloud auth application-default login

https://cloud.google.com/sdk/gcloud/reference/auth/application-default/login

## TODOS|
- implement sample components
- implement sample service
- implement serving frontend files
- implement using Cloud SQL / Cloud Storage etc ..