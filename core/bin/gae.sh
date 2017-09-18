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
*)
    echo "invalid gae argument."
esac