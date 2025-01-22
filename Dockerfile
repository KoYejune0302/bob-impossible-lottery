FROM python:3.12
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 8080
CMD ["flask", "run", "--port=8080", "--host=0.0.0.0"]
