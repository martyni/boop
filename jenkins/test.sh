source env/bin/activate
boop &
sleep 1
if [ "$(curl localhost:5000/test)" == "test" ]
  then  
     echo success
     export EXIT=0
  else
     echo failure
     export EXIT=1
fi
export PID=$(ps aux | grep -v awk |awk /boop/'{print $2}')
echo killing $PID
