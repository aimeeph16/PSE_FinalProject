FROM python:3.8

RUN apt-get update && apt-get install -y \
        build-essential \
        cmake \
        gfortran \
        git \
        wget \
        curl \
        graphicsmagick \
        libgraphicsmagick1-dev \
        libatlas-base-dev \
        libavcodec-dev \
        libavformat-dev \
        libboost-all-dev \ 
        libgtk2.0-dev \
        libjpeg-dev \
        liblapack-dev \
        libswscale-dev \
        pkg-config \
        python3-dev \
        python3-numpy \
        python3-pip \
        zip \
    && apt-get clean \
    && apt-get install python3-picamera \
    && pip3 install --upgrade picamera[array] \
    && pip3 install dlib \
    && pip3 install numpy \
    && pip3 install scikit-image \
    && apt-get install python3-scipy \
    && apt-get install libatlas-base-dev \
    && apt-get install libjasper-dev \
    && apt-get install libqtgui4 \
    && apt-get install python3-pyqt5 \
    && apt install libqt4-test \
    && ip3 install opencv-python==3.4.6.27 \
    && pip3 install face_recognition 

WORKDIR /camera
COPY . .