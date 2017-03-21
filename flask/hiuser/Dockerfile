FROM python:3.4

COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["hiuser.py"]
#RUN export FLASK_APP=hiuser.py
#RUN export FLASK_DEBUG=1
