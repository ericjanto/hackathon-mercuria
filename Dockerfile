FROM python:3.9

USER root
EXPOSE 8000

COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt
COPY --chown=nobody:nobody src /pythonapp/

WORKDIR /pythonapp/mock_api
USER nobody

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "mock_api.wsgi"]
