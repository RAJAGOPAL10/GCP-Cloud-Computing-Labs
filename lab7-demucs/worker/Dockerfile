FROM xserrat/facebook-demucs:latest

ADD worker-server.py /

RUN pip3 install --upgrade minio redis jsonpickle requests
RUN pip3 install --upgrade ffmpeg-python

COPY . /worker

CMD cd /worker && \
python3 worker-server.py