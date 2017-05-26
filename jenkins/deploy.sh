source env/bin/activate
zappa update $1 | tee build.log
awk -F "live!:" /amazonaws.com/'{print $2}' build.log > url
cat url
