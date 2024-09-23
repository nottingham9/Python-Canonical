# simple curl test of 2 endpoints 

# Reset summary data
echo curl -i  http://127.0.0.6:5005/reset

curl -i  http://127.0.0.6:5005/reset

#load data
echo curl -i -X POST -H "Content-Type: multipart/form-data" -F "file=@$1" http://127.0.0.6:5005/transactions

curl -i -X POST -H "Content-Type: multipart/form-data" -F "file=@%1" http://127.0.0.6:5005/transactions

# check results
echo curl -i  http://127.0.0.6:5005/report

curl -i  http://127.0.0.6:5005/report

