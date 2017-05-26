source env/bin/activate
boop &
sleep 1
url=$1
failed=0
if [ "$(curl $url/test)" == "OMG" ]
  then  
     echo success
  else
     echo failure
     failed=1
fi
if [ "$(curl $url/| grep folder)" ]
  then  
     echo success
  else
     echo failure
     failed=1
fi
if [ "$(curl $url/| grep ballface)" ]
  then  
     echo failure
     failed=1
  else
     echo success
fi
export PID=$(ps aux | grep -v awk |awk /boop/'{print $2}')
echo killing $PID
echo $PID >/tmp/PID
echo $failed >/tmp/EXIT
