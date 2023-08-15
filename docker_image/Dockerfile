FROM ubuntu:22.04
MAINTAINER Minsu Chae

ADD download.py /download.py
ADD chromedriver /chromedriver
ADD localtime /etc/localtime
ADD info.json /info.json
ADD account.json /account.json
ADD google-chrome-stable_current_amd64.deb /google-chrome-stable_current_amd64.deb
RUN chmod +x /chromedriver
RUN apt update
RUN apt install -y python3 python3-pip wget ffmpeg
RUN pip3 install selenium-wire requests
RUN apt install -y /google-chrome-stable_current_amd64.deb
RUN mkdir -p /Download
CMD python3 /download.py $USER
