FROM python:3.8.2

COPY ./ /back_end/

RUN pip3.8 install -r /back_end/requirements.txt

ENV PYTHONPATH="${PYTHONPATH}:/back_end/"
WORKDIR /back_end

EXPOSE 5555

CMD [ "python", "./app/api/server.py", "--config=./app/api/config.txt"]