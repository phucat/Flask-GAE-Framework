#!/usr/bin/env bash

ACTION=$1
ENVIRONMENT=$2
VERSION=$3

case $ACTION  in
run)
    echo "Running application locally ..."
    ./core/bin/run_local.sh
    ;;
deploy)
    echo -n "Deploying application ..."
    ./core/bin/deploy.sh $ENVIRONMENT $VERSION
    ;;
activate)
    . gae_environment/bin/activate
    ;;
tests)
    . gae_environment/bin/activate
    nosetests $PWD/tests/ --with-coverage --with-ferris --gae-sdk-path=$HOME/google-cloud-sdk/platform/google_appengine
    ;;
update-libraries)
    echo -n "Updating libraries ..."
    pip install -r requirements.txt -t lib --upgrade
    pip install -r local_requirements.txt --upgrade
    ;;
*)
    echo "invalid gae argument."
esac