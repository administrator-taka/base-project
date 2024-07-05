@echo off

REM SchemaSpyを実行してスキーマ情報を出力
docker run -v "%cd%/../schema:/output" --net="host" schemaspy/schemaspy:6.1.0 -t pgsql -host localhost:5432 -db postgres -u postgres -p postgres -connprops useSSL\=false -all

cmd /k
