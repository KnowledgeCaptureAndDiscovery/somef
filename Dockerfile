from python:3.6

RUN git clone https://github.com/KnowledgeCaptureAndDiscovery/somef

RUN cd somef && pip install . 

RUN somef configure -a 
