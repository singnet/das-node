FROM python:3.10

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

ENV PYTHONPATH=/app

# Copy code
COPY . .

CMD ["python", "main.py"]

