source env/bin/activate
zappa update dev >build.log
grep amazonaws.com build.log
