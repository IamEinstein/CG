FROM python:3.9
WORKDIR /
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
RUN apk add --no-cache gcc musl-dev linux-headers
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN pip install poetry
RUN poetry config virtualenvs.create false

EXPOSE 5000
COPY . .
CMD ["python3", "launcher.py"]
