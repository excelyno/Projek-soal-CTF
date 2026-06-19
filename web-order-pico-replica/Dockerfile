FROM python:3.11-slim
RUN useradd -m ctf
WORKDIR /app
RUN pip install --no-cache-dir flask
COPY ./app /app
RUN chown -R ctf:ctf /app
USER ctf
EXPOSE 5000
CMD ["python", "app.py"]