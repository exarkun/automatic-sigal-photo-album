FROM ubuntu:14.04
MAINTAINER Jean-Paul Calderone <exarkun@twistedmatrix.com>

RUN apt-get update -qq
RUN apt-get install -y python-pip python-virtualenv s3cmd
RUN virtualenv /opt/sigal
RUN /opt/sigal/bin/pip install pexif characteristic python-twisted sigal

RUN mkdir /opt/lyra-sigal
ADD index.html /opt/lyra-sigal/index.html
ADD uploads.py /opt/lyra-sigal/uploads.py
ADD sigalthing.py /opt/lyra-sigal/sigalthing.py

EXPOSE 8080
VOLUME /photos

WORKDIR /opt/lyra-sigal
CMD /opt/sigal/bin/twistd -n web --resource lyra-sigal.rpy
