docker cp backup.sql $1:/backup.sql
docker exec -it $1 psql -U $2 -d $3 -f /backup.sql