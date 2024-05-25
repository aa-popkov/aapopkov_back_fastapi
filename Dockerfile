FROM python:3.12.3-slim
LABEL authors="alexeypopkov"
EXPOSE 8000
WORKDIR /app

COPY requirements.txt .
RUN ["pip3", "install", "-r", "requirements.txt"]

COPY . .

ENV APP_MODE=dev
ENV APP_ADMIN_USERNAME=admin
ENV APP_ADMIN_PASSWORD=admin

RUN ["mkdir", "data"]
RUN ["chmod", "+x", "startup.sh"]

ENTRYPOINT ["/app/startup.sh"]