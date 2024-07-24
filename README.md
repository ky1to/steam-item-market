# steam-item-market
This is a project written to parse the Steam Market website, save it to a database (SQLAlchemy + postgresql) and output it via a fast API with caching using Redis.
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