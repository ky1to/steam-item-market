docker cp  $1:./backup.sql backup.sql
docker exec -it $1 pg_dump -U $2 -d $3 > backup.sql