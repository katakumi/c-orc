# start C:\"Program Files"\Redis\redis-server.exe
for %%i in (*.py) do (

echo [LOG] Execute Agent : ：%%i
start python %%i

)