source env/bin/activate
if [ "$(boop)" == "I'm an app" ]
  then  
     echo success
     exit 0
  else
     echo failure
     exit 1
fi