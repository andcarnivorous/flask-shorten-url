FROM alpine:latest

RUN apk update && apk upgrade
RUN yes | apk add python3 py3-setuptools

COPY . /workspace

RUN pip3 install -r /workspace/requirements.txt
RUN python3 /workspace/db.py

ENTRYPOINT [ "python3" ]
CMD [ "/workspace/service.py" ]

