FROM balenalib/raspberrypi3-python:3.7-latest-build as build

COPY ./requirements.txt .

RUN pip install --no-cache-dir --target=./pip-packages -r requirements.txt

FROM balenalib/raspberrypi3-python:3.7-latest-run

RUN install_packages bluez bluetooth

COPY --from=build ./pip-packages /home/pip-packages

ENV PYTHONPATH="/home/pip-packages:${PYTHONPATH}"

COPY src/main.py home/main.py
COPY src/docker_entrypoint.sh .
COPY ./.env home/.env

ENTRYPOINT sh docker_entrypoint.sh
