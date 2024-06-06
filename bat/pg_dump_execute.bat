docker exec -i postgresql psql -U postgres -d postgres -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"
docker exec -i postgresql psql -U postgres -d postgres < test.sql
@REM cmd /k