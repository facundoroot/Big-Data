FROM apache/airflow:2.2.2-python3.9

WORKDIR /requirements

# install dependencies
COPY requirements.txt /requirements
RUN pip install -r requirements.txt

