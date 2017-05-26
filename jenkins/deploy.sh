source env/bin/activate
build=$(zappa update $1 2&>1 || zappa deploy $1 2&>1)
echo $build | tee build.log
awk -F "live!:" /amazonaws.com/'{print $2}' build.log > url
cat url
