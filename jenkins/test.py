import requests
import sys

print "url: " + sys.argv[1]

def test_path(path, base_url=sys.argv[1]):
    if requests.get(base_url + path):
        print "success: {}".format(base_url + path) 
        return 1
    else:
        print "fail: {}".format(base_url + path)
        return 0

for path in "/", "/test", "/series/folder":
    if not test_path(path):
       sys.exit(1)

for path in ["/no_endpoint"]:
    if test_path(path):
       sys.exit(1)
