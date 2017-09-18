environment="local"
cp $PWD/configurations/${environment}.yaml $PWD/env_variables.yaml

nosetests $PWD/tests/ --with-coverage --with-ferris --gae-sdk-path=$HOME/google-cloud-sdk/platform/google_appengine
(dev_appserver.py app.yaml --port=8081 --log_level debug)