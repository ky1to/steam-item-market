# steam-item-market

This is a project written to scrape the Steam Market website, store it in a database (SQLAlchemy + postgresql) and output it through a fast API with caching using Redis. Also uses nginx to send html file and static content.

## To-Do list

- add a service for logs

- Authorization + personal account

- email notification (report)

## Backup
### Uploading beсkup to the server
To upload a backup to the server, there is a script upload_backup.sh in the repository. To run it you need to pass arguments to it:

``` sh
sh upload_backup.sh name_your_db_container username name_db
```
### Creating a backup and downloading it from a docker container
As in the past, the script named install_backup.sh must be run with certain arguments:

``` sh 
sh install_backup.sh name_your_db_container username name_db
```

## Launch

To run you need to create a .env file with content and fill it with your data:

```
POSTGRES_USER=
POSTGRES_PASSWORD=
POSTGRES_DB=
AUTH_POSTGRES_USER=
AUTH_POSTGRES_PASSWORD=
AUTH_POSTGRES_DB=
PGADMIN_DEFAULT_EMAIL=
PGADMIN_DEFAULT_PASSWORD=
SECRET_KEY = 
ALGORITHM = 
```

after this you can run docker compose:

``` sh

sudo docker-compose up --build

```