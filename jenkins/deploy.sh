source env/bin/activate
yes | zappa undeploy $1
zappa deploy $1 2>&1 | tee build.log
awk -F "live!:" /amazonaws.com/'{print $2}' build.log > url
cat url
