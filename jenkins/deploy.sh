source env/bin/activate
build=$(zappa deploy $1)
echo $build >build.log
awk -F "live!:" /amazonaws.com/'{print $2}' build.log > url
cat url
