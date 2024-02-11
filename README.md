# datapains-whiskey-el


![example workflow](https://github.com/Thelin90/datapains-whiskey-el/actions/workflows/merge.yaml/badge.svg)
![example workflow](https://github.com/Thelin90/datapains-whiskey-el/actions/workflows/pr.yaml/badge.svg)


Data Pains Training Session Part 1 Of End To End Data Product.

## Application guide

*

## Requirements

* ^python3.10
* poetry 1.7.1
* make

### Setup

```bash
make setup-environment
```

Update package
```bash
make update
```

### Local

Please set

```bash
export AWS_ALLOW_HTTP=true
```

If running from local machine

```bash
make run config-file-name=config/local/example-config.ini
```

### Test

`TODO`

```bash
export PYTHONPATH="${PYTHONPATH}:src"
make test type=unit
```

### Docker

The reason `docker` is used in the source code here, is to be able to build up an encapsulated
environment of the codebase, and do `unit/integration and load tests`.

```bash
make build-container-image DOCKER_BUILD="buildx build --platform linux/amd64" CONTEXT=.
```

```bash
make run-container-tests type=unit
```

### K8S

#### Local

```bash
make apply-k8s LAYER=base
make apply-k8s LAYER=storage
```

Verify this is up and running and bucket is created via:

* http://localhost:30001/login

```bash
user: accountadmin123
pass: accountadminsecret123
```

```bash
make apply-k8s LAYER=app
```
