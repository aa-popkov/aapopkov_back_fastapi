# AAPopkov Backend API

## Run this project

Pull this repo:

```shell
git pull https://github.com/aa-popkov/aapopkov_back_fastapi.git
```

### Docker

Go into repo folder

```shell
cd ./aapopkov_back_fastapi
docker build -t backend_api .
docker run -d -p 8080:8000 \
  -e APP_MODE=dev \
  -e APP_ADMIN_USERNAME=admin \
  -e APP_ADMIN_PASSWORD=admin \
  -v $(pwd)/data:/app/data \
  --name backend_api \
  backend_api
```

>
> | Env                  | Type                  | Example |
> |----------------------|-----------------------|---------|
> | `APP_MODE`           | `enum`_(dev \| prod)_ | prod    |
> | `APP_ADMIN_USERNAME` | `string`_(max=50)_    | admin   |
> | `APP_ADMIN_PASSWORD` | `string`              | admin   |

## API Helpers

### Issue RSA private key + public key pair

> **Generate an `RSA private key`, of size `2048`**
> ```shell
> openssl genrsa -out jwt-private.pem 2048
> ```

> **Extract the `public key` from the key pair, which can be used in a certificate**
> ```shell
> openssl rsa -in jwt-private.pem -outform PEM -pubout -out jwt-public.pem
> ```

### Alembic

> **Initialization**
> ```shell
> cd /*path_to_project*
> alembic init -t async alembic
> ```

> **Make migration**
> ```shell
> alembic revision --autogenerate -m "Init"
> ```

> **Update DB**
> ```shell
> alembic upgrade head
> ```
