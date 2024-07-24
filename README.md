# steam-item-market
This is a project written to scrape the Steam Market website, store it in a database (SQLAlchemy + postgresql) and output it through a fast API with caching using Redis. Also uses nginx to send html file and static content.

## To-Do list
- make a service for updating the database (update.py does not work now)
- Authorization + personal account
- email notification (report)

## Backup
Download a backup copy of the database in which the element table is located. If you want to create your own database backup, use the following command:
``` sh
    pg_dump -U username -h hostname > backup.sql
```
To host a backup database in Docker:
``` sh
docker cp backup.sql your_compose_project_db_1:/backup.sql
```
To log into a container from the database:
``` sh
docker exec -it your_compose_project_db_1 bash
```
When you are ready in the Docker container, upload the backup to the PostGreSQL database.
``` sh
psql -U username -d your_db -f /backup.sql
```
## Launch
To run you need to create a .env file with content and fill it with your data:
```  
POSTGRES_USER=
POSTGRES_PASSWORD=
POSTGRES_DB=
PGADMIN_DEFAULT_EMAIL=
PGADMIN_DEFAULT_PASSWORD=
```
after this you can run docker compose:
``` sh
sudo docker-compose up --build
```