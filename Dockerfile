FROM python:3.10

ENV PYTHONUNBUFFERED 1

WORKDIR /restapi

COPY restapi/ ./

ENV PYTHONPATH "${PYTHONPATH}:/restapi"

EXPOSE 5050
CMD uvicorn main:app --host 0.0.0.0 --port 5050

