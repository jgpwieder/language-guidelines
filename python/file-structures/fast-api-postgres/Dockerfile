

FROM python:3.10
WORKDIR /code
COPY . .
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
EXPOSE 8000
ENTRYPOINT python ./main.py
