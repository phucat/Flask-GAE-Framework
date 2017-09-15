#Flask - GAE Boilerplate

The Goal is to quickly and easily implement a backend service that contains all necessary structures configurations and automation designed for Google Appengine and Bitbucket pipelines for rapid development.

It's the compilation of mostly used methods, approaches and techniques when developing backend in Appengine or Compute Engine.
This is not a Flask tutorial but takes advantages and leverages the features of Flask Framework.

## System Requirements
- python 2.7
- vitualenv 15.0.3 or higher
- pip 9.0.1 or higher
- setuptools

## Directory Structure
```
root/
 | - app/ (contains all project related codes)
 |   | - components/ (contains classes that is used across modules, ideally google api services)
 |   |   | - calendar.py
 |   |   | - directory.py
 |   |   | - cloud_storage.py
 |   |   | - ..... many more 
 |   | - modules/ (contains blueprint, model and module related services)
 |   |   | - home (home module)
 |   |   |    | - api.py
 |   |   |    | - model.py
 |   |   |    | - service.py 
 |   |   | - guestbook (guestbook module)
 |   |   |    | - api.py
 |   |   |    | - model.py
 |   |   |    | - service.py 
 |   | - services/ (contains services that are used across modules)
 |   | - exceptions.py (should contain all custom exception used in the project)
 |   | - util.py (contains snippets or methods that is used across classes)
 | - configurations/ (configuration files for each environment)
 |   | - local.yaml
 |   | - dev.yaml
 |   | - qa.yaml
 |   | - prod.yaml
 | - credentials/ (directory where service account credentials are located.)
 |   | - qa-encrypted.json
 |   | - dev-encrypted.json
 |   | - prod-encrypted.json
 | - core/ (this directory contains most of the core codes used on all application
 |   | - auth.py
 |   | - config.py
 |   | - ...... many more
 | - tests/ (contains test files)
 |   | - modules
 |   |   | - home
 |   |   |   | - api_tests.py
 |   |   |   | - model_tests.py
 |   |   |   | - service_tests.py
 |   |   | - guestbook
 |   |   |   | - api_tests.py
 |   |   |   | - model_tests.py
 |   |   |   | - service_tests.py
 | - tools/ (contains scripts or tools to help on development)
 | - app.yaml (appengine required files that defines your service)
 | - appengine_config.py (tells appengine the path of libraries the project is using)
 | - bitbucket-pipelines (for CI automation)
 | - deploy.sh (a script to deploy your project easily)
 | - local_requirements.txt (contains the required libraries to run your project locally)
 | - main.py (the entry point of application used by Flask)
 | - requirements.txt (contains only libraries that are needed when deploying to appengine)
 | - run_local.sh (a script that will automate your local deployment)
```


## How to run locally:
On your terminal:
```
virtualenv venv

. venv/bin/activate
pip install -r local_requirements.txt
pip install -r requirements.txt -t lib

./run_local.sh
```
Note: run_local.sh will also run the nosetest
## How to deploy
> ./deploy [environment] [version]

The [environment] value will automatically map the files inside the 'configurations' folder and will load your environment settings
## Core Functions
### Search (core.search.py)
To implement a search on datastore, use the following helper function
```
apply_search(
    blueprint=<BLUEPRINT>,
    model=<MODEL CLASS>,
    index_fields=['email', 'firstname', 'lastname'],
    paginate_limit=5,
    transformer=<ENTITY TRANSFORM FUNCTION if needed>
)

```
Full Example: 
```
user_accounts = Blueprint('user_accounts', __name__, url_prefix='/api/user_accounts')
apply_search(
    blueprint=user_accounts,
    model=UserAccountsRequestorModel,
    index_fields=['email', 'firstname', 'lastname'],
    index_only_if = ('active', True)
    paginate_limit=5,
    transformer=UserAccountsRequestorModel.search_output
)
```
#### what it does?
- This helper function will automagically create a "api/search" endpoint where you can query a search. eg: 
/api/search?query=<Search string>

- This helper listens to every put() on the specified model. once a put() is triggered, the entity will be added to the Search API given with what index_fields you want to be indexed or searchable field you wanted.
- This helper can only index a scenario that you want by using 'index_only_if'. On the example above, the indexing will only happen if User.active  == True.

## Auth (core.auth.py)
A general implementation for backend authentication that is fully integrated in Flask's apis.
See main.py and auth.py.

## NDB (core.ndb.py)
A simple NDB to BasicModel implementation that is applicable across any models you'll be using.
It just adds some usual fields like 'created_by', 'created_date', 'modified_by' etc. and also added the after_put, before_put, after_delete, before_delete events listeners.

## JSON UTILS (core.utils.py)
Basic utility tools on writing JSON response on your endpoints which also includes the standard HTTP response codes.

## Cross Domain (core.cross_domain.py)
Cross domain helper for your endpoints.

## Config (core.config.py)
The helper to organize your environment variables.

# Google Service Components Included
## Google Directory
basic implementation, needs improvement, TBC 
## Google Cloud Storage
basic implementation, needs improvement, TBC
## Google Pubsub
basic implementation, needs improvement, TBC
## Google Cloud KMS
Complete Interface when using Cloud KMS





## [OPTIONAL] How to import commons library

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