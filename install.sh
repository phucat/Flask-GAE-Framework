#!/usr/bin/env bash

deactivate
printf "\033c"
sudo rm /usr/bin/gae
sudo ln -s $PWD/core/bin/gae.sh /usr/bin/gae

if ! [ -x "$(command -v gcloud)" ]; then
  printf "Please install Google Cloud SDK first!"
  return ""
fi

virtualenv gae_environment

. gae_environment/bin/activate

pip install -r requirements.txt -t lib
pip install -r local_requirements.txt

printf "\033c"
print ""
print "###################################"
print "Flask GAE Framework Installed!"
print "###################################"
printf ""