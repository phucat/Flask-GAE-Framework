#!/usr/bin/env bash
function usage {
    cat << EOF

<Usage>: deploy.sh <environment> [version]

Deploys this appengine application to the designated environment (dev/qa/prod).

EOF
   exit 1
}

environment=$1

if [ $# -gt 2 ] || [ $# -lt 1 ]; then
    usage;
fi

gitHash=`git rev-parse --short HEAD`
version=$2

if [ "$environment" = "dev" ]; then
    projectId="cs-development-playground"
    nopromote=""
fi

if [ "$environment" = "qa" ]; then
    projectId="acn-morri-jml-qa"
    nopromote=""
    version="$version-$gitHash"
fi

if [ "$environment" = "staging" ]; then
    projectId="acn-morri-jml-staging"
    nopromote=""
    version="$version-$gitHash"
fi

if [ "$environment" = "pre" ]; then
    projectId="morrisons-jml-pre"
    nopromote=""
    version="$version-$gitHash"
fi

if [ "$environment" = "prod" ]; then
    projectId="morrisons-jml"
    nopromote=" --no-promote"
    version="$version-$gitHash"
fi

cp configurations/${environment}.yaml env_variables.yaml
(gcloud app deploy app.yaml --project=$projectId --version=$version $nopromote --verbosity=info)
