FROM python:3.8
WORKDIR /app
COPY ./ /app
RUN pip install -r /app/requirements.txt
RUN python manage.py migrate
CMD ["python", "./manage.py", "runserver"]
# CMD ["gunicorn", "--bind", "0.0.0.0:8000", "stocks_products.wsgi"]