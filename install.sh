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
print "written and maintained by: Sugar Ray Tenorio"
print "###################################"
echo ""
echo "Usage:"
echo ""
echo "'gae run' = run locally"
echo "'gae deploy [environment] [version]' = run locally"
echo "'gae update-libraries' = update application libraries"
echo "'gae activate' = activate virtual env again"
echo ""
echo "Please see README.md for more info ..."
echo "----------------------------------"
echo ""