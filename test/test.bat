@echo off

REM simple curl test of 2 endpoints 

REM Reset summary data
echo C:\Windows\System32\curl -i  http://127.0.0.6:5005/reset

C:\Windows\System32\curl -i  http://127.0.0.6:5005/reset

REM load data
echo C:\Windows\System32\curl -i -X POST -H "Content-Type: multipart/form-data" -F "file=@%1" http://127.0.0.6:5005/transactions

C:\Windows\System32\curl -i -X POST -H "Content-Type: multipart/form-data" -F "file=@%1" http://127.0.0.6:5005/transactions

REM check results
echo C:\Windows\System32\curl -i  http://127.0.0.6:5005/report

C:\Windows\System32\curl -i  http://127.0.0.6:5005/report

