cd ../../
docker compose down --volumes
docker image prune -a -f
@REM cmd /k