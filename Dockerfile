FROM python:3.9
COPY . /app1
WORKDIR /app1
RUN pip install -r requirements.txt
ENTRYPOINT [ "python" ]
CMD [ "app1.py" ]
