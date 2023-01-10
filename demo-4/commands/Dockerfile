FROM ghcr.io/maxotta/kiv-ds-docker:latest

RUN yum -q -y install python3

COPY . /opt/commands

RUN pip3 install -r /opt/commands/python/requirements.txt

# EOF