#!/bin/bash

echo "Check certs file"

PRIVATE_KEY="$(pwd)/data/jwt-private.pem"
PUBLIC_KEY="$(pwd)/data/jwt-public.pem"

if [ -e "$PRIVATE_KEY" ]; then
    echo "Private certs is exist"
else
  echo "Private certs is not exist, try to create"
  openssl genrsa -out "$PRIVATE_KEY" 2048 || (echo "Private key generation is failed" && exit 1)
  echo "Private is successful generated"
fi

if [ -e "$PUBLIC_KEY" ]; then
    echo "Public certs is exist"
else
  echo "Public certs is not exist, try to create"
  openssl rsa -in "$PRIVATE_KEY" -outform PEM -pubout -out "$PUBLIC_KEY" || (echo "Public key generation is failed" && exit 1)
  echo "Public is successful generated"
fi

echo "Certs check is successful"

echo "Start alembic database upgrade"
alembic upgrade head || (echo "Alembic database upgrade is failed" && exit 1)
echo "Alembic database upgrade is successful"

echo "Start application"
python3 main.py