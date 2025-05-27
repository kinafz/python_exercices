# Run the TP3 project

## Build

```bash
export MYSQL_ROOT_PASSWORD=myrootpassword
export MYSQL_USER=myuser
export MYSQL_PASSWORD=mypwd
export MYSQL_DATABASE=mydb
docker compose up --build
```

## Enter the application

```bash
docker logs tp3-runner && docker attach tp3-runner
```

## Cleanup

```bash
docker compose down
```