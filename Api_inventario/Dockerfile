FROM python:3

COPY . /app/api_inventario

EXPOSE 5002

RUN pip install flask && pip install mysql.connector && pip install flask_sqlalchemy && \
pip install datetime && pip install flask_httpauth && pip install Response && pip install requests

WORKDIR /app/api_inventario

CMD python Execução.py