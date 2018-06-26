FROM python:3.7-rc

RUN apt-get -yq update \
  && apt-get -yq upgrade \
  && apt-get install -yq vim \
  && pip install --upgrade pip \
  && pip install google-auth google-cloud python-twitter requests_oauthlib \
  && apt-get -y autoremove \
  && apt-get -yq clean \
  && rm -rf /var/lib/apt/lists/* \
  && rm -rf /tmp/* \
  && rm -rf /var/tmp/*

WORKDIR /usr/src

CMD [ "/bin/bash" ]