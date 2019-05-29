FROM python:3.7
RUN mkdir /app/
WORKDIR /app/
RUN adduser --disabled-password --gecos '' app
USER app
ENV PATH "/home/app/.local/bin:$PATH"
ADD python/requirements.txt /app/
RUN pip install -r requirements.txt --user
ADD python/* /app/
ENTRYPOINT ["python setup_data.py"]
