FROM python:3.11.0
WORKDIR /fampay_assignment
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY /fampay_assignment .
EXPOSE 8080
CMD ["sh","-c","python manage.py migrate && python manage.py runserver 0.0.0.0:8080"]