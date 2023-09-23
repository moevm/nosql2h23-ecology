FROM osgeo/gdal:ubuntu-small-3.6.3

WORKDIR /worker

RUN apt-get update && apt install -y python3-pip && python -m pip install pip==22.0.2

ADD requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY app app
