FROM python:slim

COPY . /app

RUN apt-get update && apt-get install -y git build-essential yasm cmake libtool libc6 libc6-dev unzip wget libnuma1 libnuma-dev
RUN mkdir /build
WORKDIR /build
RUN git clone https://git.videolan.org/git/ffmpeg/nv-codec-headers.git
RUN cd nv-codec-headers && make install
WORKDIR /build
RUN git clone https://git.ffmpeg.org/ffmpeg.git ffmpeg/
RUN  apt install build-essential yasm cmake libtool libc6 libc6-dev unzip wget libnuma1 libnuma-dev
WORKDIR /build/ffmpeg
RUN ./configure --enable-nonfree --enable-cuda-nvcc --enable-libnpp --extra-cflags=-I/usr/local/cuda/include --extra-ldflags=-L/usr/local/cuda/lib64 --disable-static --enable-shared
RUN make -j 8
RUN make install

RUN pip install --upgrade pip && pip install --upgrade setuptools
WORKDIR /app
RUN pip install -r requirements.txt
RUN apt-get remove -y git gcc build-essential yasm cmake libtool libc6 libc6-dev unzip wget libnuma1 libnuma-dev \
&& apt-get -y autoremove
EXPOSE 5000
CMD ["/app/start.sh"]