FROM python:3.9-slim-bullseye

ENV APP_ROOT /app

RUN mkdir ${APP_ROOT}
WORKDIR ${APP_ROOT}

EXPOSE 8182

COPY rqworker.entrypoint.sh entrypoint.sh requirements.txt ${APP_ROOT}/
RUN pip install -r ${APP_ROOT}/requirements.txt

ADD hashi/ ${APP_ROOT}
