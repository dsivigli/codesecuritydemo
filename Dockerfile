FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# VULNERABILITY: Running as root
# Should use a non-privileged user

# VULNERABILITY: Exposing unnecessary ports
EXPOSE 5001 22 80 443

# VULNERABILITY: Environment variables with secrets
ENV AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE
ENV AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
ENV DB_PASSWORD=insecure_password

CMD ["python", "app.py"]
