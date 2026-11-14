FROM python:3.11-slim

LABEL maintainer="Khanhtnq <218711032+Khanhtnq@users.noreply.github.com>"
LABEL ugreen.skill.id="com.ugreen.skill.vaultsense"
LABEL ugreen.skill.version="1.0.0"

WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8443

HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8443/api/v1/status')" || exit 1

CMD ["uvicorn", "vaultsense.api:app", "--host", "0.0.0.0", "--port", "8443"]
