MAINTAINER Jean-Paul Calderone <exarkun@twistedmatrix.com>
FROM ubuntu:14.04

RUN apt-get update
RUN apt-get install -y python-pip python-virtualenv
RUN virtualenv /opt/sigal
RUN /opt/sigal/bin/pip install python-twisted sigal

EXPOSE 8080

CMD /opt/sigal/bin/twistd -n web --resource lyra-sigal.rpy
