import requests
import sys

print "url: " + sys.argv[1]
base_url = sys.argv[1]

def test_path(path):
    if requests.get(base_url + path):
        print "success: {}".format(base_url + path) 
        return 1
    else:
        print "fail: {}".format(base_url + path)
        return 0

def serializable(path):
    try:
        requests.get(base_url + path).json
        print "success: {}".format(base_url + path)
        return 1
    except:
        print "fail: {}".format(base_url + path)
        return 0

for path in "/", "/test", "/series/folder", "/api":
    if not test_path(path):
       sys.exit(1)

for path in ["/api"]:
    if not serializable(path):
       sys.exit(1)

for path in ["/"]:
    if serializable(path):
       sys.exit(1)

for path in ["/no_endpoint"]:
    if test_path(path):
       sys.exit(1)
