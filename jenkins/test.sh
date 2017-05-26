source env/bin/activate
boop &
sleep 1
failed = 0
if [ "$(curl localhost:5000/test)" == "OMG" ]
  then  
     echo success
  else
     echo failure
     failed = 1
fi
if [ "$(curl localhost:5000/)" == "file" ]
  then  
     echo success
  else
     echo failure
     failed = 1
fi
export PID=$(ps aux | grep -v awk |awk /boop/'{print $2}')
echo killing $PID
echo $PID >/tmp/PID
echo $failed >/tmp/EXIT
