FROM  gcr.io/google-appengine/python

RUN apt-get -qq update && apt-get -y install nano curl

ENV CLOUDSDK_CORE_DISABLE_PROMPTS=1
RUN curl -O -J https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-sdk-127.0.0-linux-x86_64.tar.gz
RUN tar -zxvf google-cloud-sdk-127.0.0-linux-x86_64.tar.gz --directory ${HOME}
ENV PATH=${PATH}:/root/google-cloud-sdk/bin

ENV GAE_PYTHONPATH=/root/google_appengine
ENV PYTHONPATH=${PYTHONPATH}:${GAE_PYTHONPATH}
ADD lib/fetch_gae.py /fetch_gae.py
RUN python /fetch_gae.py $(dirname "${GAE_PYTHONPATH}")
RUN echo "${PYTHONPATH}" && ls ${GAE_PYTHONPATH}