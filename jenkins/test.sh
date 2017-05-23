source env/bin/activate
boop &
sleep 1
if [ "$(curl localhost:5000/test)" == "test" ]
  then  
     echo success
     EXIT=0
  else
     echo failure
     EXIT=1
fi
PID=$(ps aux | grep -v awk |awk /boop/'{print $2}')
echo killing $PID
kill $PID
echo exit $EXIT
exit $EXIT
