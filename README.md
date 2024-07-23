# steam-item-market

This is a project written for parsing the steam market website with saving to a database (SQLAlchemy + postgresql) and output via fast api with caching using Redis

pg_dump -U username -h host dbname > backup.sql

docker cp backup.sql your_compose_project_db_1:/backup.sql

docker exec -it your_compose_project_db_1 bash

psql -U username -d your_db -f /backup.sql