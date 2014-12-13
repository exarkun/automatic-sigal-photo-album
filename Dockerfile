FROM ubuntu:14.04
MAINTAINER Jean-Paul Calderone <exarkun@twistedmatrix.com>

RUN apt-get update -qq
RUN apt-get install -y python-pip python-virtualenv s3cmd
RUN apt-get build-dep -y python-twisted
RUN apt-get build-dep -y python-imaging
RUN apt-get install -y libopenjpeg-dev
RUN virtualenv /opt/sigal
RUN /opt/sigal/bin/pip install pexif characteristic twisted sigal==0.7.0

RUN mkdir /opt/lyra-sigal
ADD index.html /opt/lyra-sigal/index.html
ADD uploads.py /opt/lyra-sigal/uploads.py
ADD sigalthing.py /opt/lyra-sigal/sigalthing.py
ADD lyra-sigal.rpy /opt/lyra-sigal/lyra-sigal.rpy

EXPOSE 8080
VOLUME /photos

ENV PATH /usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/opt/sigal/bin

WORKDIR /opt/lyra-sigal
CMD /opt/sigal/bin/twistd -n web --resource lyra-sigal.rpy
