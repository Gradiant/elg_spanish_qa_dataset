FROM python:3.8


COPY scripts /app/

RUN pip3 install --upgrade pip && pip3 install -r /app/requirements.txt

WORKDIR /app/

ENV LANG="C.UTF-8" \
    LC_ALL="C.UTF-8"


EXPOSE 8866


CMD ["python3", "serve.py"]
