@echo off
chcp 65001 >nul
set /p CONTINUE=本当に実行しますか？ (y/n):

if /i "%CONTINUE%" NEQ "y" (
    echo 操作はキャンセルされました。
    goto :EOF
)

docker exec -i postgresql psql -U postgres -d postgres -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"
docker exec -i postgresql psql -U postgres -d postgres < test.sql

@REM cmd /k
