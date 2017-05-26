source env/bin/activate
zappa update $1 || zappa deploy $1>build.log
awk -F "live!:" /amazonaws.com/'{print $2}' build.log > url
cat url
