source env/bin/activate
if [ "$(poop)" == "I'm an app" ]
  then  
     echo success
     exit 0
  else
     echo failure
     exit 1
fi
