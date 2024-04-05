cd ../../
docker compose down
docker container prune -f
docker image prune -a -f
docker volume prune -f
@REM cmd /k