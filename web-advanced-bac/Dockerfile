FROM python:3.11-slim
WORKDIR /app
# Install Flask sekaligus Requests untuk keperluan exfiltration
RUN pip install --no-cache-dir flask requests
COPY ./app /app
EXPOSE 5000
CMD ["python", "app.py"]