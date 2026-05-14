FROM python:3.11

WORKDIR /somef
COPY . /somef
# RUN git clone https://github.com/KnowledgeCaptureAndDiscovery/somef

RUN curl -sSL https://install.python-poetry.org | python3 -

ENV PATH="/root/.local/bin:$PATH"

RUN pip install poetry-plugin-shell

RUN poetry install 

ENV PATH="/somef/.venv/bin:$PATH"
RUN poetry config virtualenvs.in-project true && poetry install

RUN poetry run somef configure -a

RUN echo 'source $(poetry env info --path)/bin/activate' >> ~/.bashrc

CMD ["bash", "--login"]


