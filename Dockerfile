FROM python:3.9

ENV APP_ROOT /app

RUN mkdir ${APP_ROOT}
WORKDIR ${APP_ROOT}

EXPOSE 8182

COPY entrypoint.sh requirements.txt ${APP_ROOT}/
RUN pip install -r ${APP_ROOT}/requirements.txt

ADD hashi/ ${APP_ROOT}

CMD ["gunicorn", "--bind", "0.0.0.0:8182", "hashi.wsgi"]
