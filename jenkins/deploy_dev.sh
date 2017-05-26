source env/bin/activate
zappa update dev >build.log
awk -F "live!:"/amazonaws.com/'{print $2}' build.log > url
cat url
