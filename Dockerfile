FROM ubuntu:16.04

# Ensure that Python outputs everything that's printed inside
# the application rather than buffering it.
ENV PYTHONUNBUFFERED 1
ENV APP_ROOT /code
ENV DEBUG False

RUN apt-get update && apt-get install -y \
  build-essential \
  python3 \
  python3-pip \
  python3-dev \
  python3-venv \
  libpq-dev \
  libjpeg-dev \
  binutils \
  libproj-dev \
  gdal-bin \
  libxml2-dev \
  libxslt1-dev \
  zlib1g-dev \
  libffi-dev \
  libssl-dev \
  language-pack-pt \
  python3-gdal \
  curl \
  wget\
  libgconf2-4 libnss3-1d libxss1 \
  fonts-liberation libappindicator1 xdg-utils \
  software-properties-common \
  unzip \
  xvfb




# install geckodriver and firefox

RUN GECKODRIVER_VERSION=`curl https://github.com/mozilla/geckodriver/releases/latest | grep -Po 'v[0-9]+.[0-9]+.[0-9]+'` && \
    wget https://github.com/mozilla/geckodriver/releases/download/$GECKODRIVER_VERSION/geckodriver-$GECKODRIVER_VERSION-linux64.tar.gz && \
    tar -zxf geckodriver-$GECKODRIVER_VERSION-linux64.tar.gz -C /usr/local/bin && \
    chmod +x /usr/local/bin/geckodriver

RUN add-apt-repository -y ppa:ubuntu-mozilla-daily/ppa
RUN apt-get update && apt-get install -y firefox


## Copy in your requirements file
ADD requirements.txt /requirements.txt
## Install build deps, then run `pip install`, then remove unneeded build deps all in a single step. Correct the path to your production requirements file, if needed.
RUN python3 -m venv /venv
RUN /venv/bin/pip install -U pip==18.1
RUN /venv/bin/pip install --no-cache-dir -r /requirements.txt


RUN mkdir ${APP_ROOT}
WORKDIR ${APP_ROOT}
ADD . ${APP_ROOT}
COPY mime.types /etc/mime.types

# uWSGI will listen on this port
EXPOSE 8030

# Call collectstatic (customize the following line with the minimal environment variables needed for manage.py to run):
# RUN if [ -f manage.py ]; then /venv/bin/python manage.py collectstatic --noinput; fi

# Start uWSGI
CMD [ "/venv/bin/uwsgi", "--ini", "/code/uwsgi.ini"]
