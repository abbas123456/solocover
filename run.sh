#/bin/bash
if [ $# -eq 0 ]
  then
    echo "USAGE: ./run.sh tag"
    exit 0
fi
docker rm -f appserver dbserver memcached mysql_data
docker run --name postgres_data -v ~/Documents/solocover_postgres:/var/lib/postgresql busybox true
docker run -d --name dbserver --volumes-from mysql_data abbas123456/solocover_db:$1
docker run -d -e DJANGO_SETTINGS_MODULE=conf.local -p 8000:8000 -p 8001:8001 --name appserver --link dbserver:dbserver -v ~/projects/solocover:/var/django-projects/solocover abbas123456/solocover_app:$1

