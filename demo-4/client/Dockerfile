FROM ghcr.io/maxotta/kiv-ds-docker:latest

RUN yum -q -y install python3

COPY . /opt/client

RUN pip3 install -r /opt/client/python/requirements.txt

CMD /usr/bin/python3 /opt/client/python/main.py

# EOF
