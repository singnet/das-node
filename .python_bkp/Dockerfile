FROM python:3.10

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

ENV PYTHONPATH=/app

# Copy code
ADD ./hyperon_das_node /app/

CMD ["python", "main.py"]

