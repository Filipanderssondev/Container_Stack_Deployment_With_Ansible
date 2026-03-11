FROM private-registry.com/our-repo/rockylinux:10-ubi-init

# Copying the package repos
COPY dnf-repos/yum.repos.d /etc/yum.repos.d

RUN dnf install -y \
    python3 \
    python3-flask \
    python3-psycopg2 \
    python3-dotenv \
    && dnf clean all

WORKDIR /app

COPY . .

EXPOSE 5000

CMD ["python3", "app.py"]
