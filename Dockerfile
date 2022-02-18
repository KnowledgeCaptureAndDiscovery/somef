from python:3.9

RUN git clone https://github.com/KnowledgeCaptureAndDiscovery/somef

RUN cd somef && pip install -e . 

RUN somef configure -a
