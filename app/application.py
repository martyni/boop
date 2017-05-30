from flask import Flask, request, url_for, redirect, jsonify
import boto3
import datetime
import re
from pprint import pprint

app = Flask(__name__)
client = boto3.client("s3")

cache = {}

def url_sanitizer(raw_path):
    if ".amazonaws.com" not in request.url:
       return raw_path.replace('/prod', '').replace('/stge', '').replace('/dev', '')
    else:
       return raw_path

def url_4(*args, **qwargs):
   raw_path = url_for(*args, **qwargs)
   return url_sanitizer(raw_path)

def parse_series_and_episodes(s3_list, path=None):
   series = {}
   c = 0
   for _ in s3_list:
       m = re.match(r'([a-z]*)/$', _)
       if m:
          series[m.group(1)] = {}
          s3_list.pop(c)
       c += 1
   c = 0    
   for _ in s3_list:
       m = re.search(r'([a-z]*)/([0-9]*)/$', _)
       if m:
           series[m.group(1)][m.group(2)] = {}
           s3_list.pop(c)
       c += 1
   c = 0     
   for _ in s3_list:
       m = re.search(r'([a-z]*)/([0-9]*)/(.*).mp3$', _)
       if m:
           series[m.group(1)][m.group(2)][m.group(3)] = {"mp3":m.group(0)} 
           s3_list.pop(c)
       c += 1

   c = 0     
   for _ in s3_list:
       m = re.search(r'([a-z]*)/([0-9]*)/(.*).txt$', _)
       if m:
           series[m.group(1)][m.group(2)][m.group(3)]["txt"] = m.group(0) 
           s3_list.pop(c)
       c += 1
   c = 0     
   pprint(series)
   return series   

def get_series(Bucket="martyni-boop", path="", series=False, old=False):
    if cache.get(path):
        blob = cache.get(path)
    else:
        blob = client.list_objects_v2(Bucket="martyni-boop")
        cache[path] = blob
    contents = blob['Contents']
    s3_list = [f['Key'] for f in contents]
    if not old:
       return  parse_series_and_episodes( s3_list )
    elif not series:
        return [f for f in s3_list if "/" not in f ]
    elif series:
        return [f[:-1:] for f in s3_list if "/" in f ]



def api(path="/", error=None, meta={}):
    payload = {
            "error": error,
            "path": path,
            "data": {},
            "meta": meta
            }
    payload["meta"]["date"] = str(datetime.datetime.utcnow())
    payload["meta"]["url"]  = url_sanitizer(request.url)
    payload["meta"]["remote_addr"]   = request.remote_addr
    payload["meta"]["user_agent"]   = str(request.user_agent)
    payload["data"]["series"] = get_series(path=path)
    
    if not payload["error"]:
       return jsonify(payload)
    else:
       response = jsonify(payload)
       response.status_code = 400
       return response 

@app.route('/test')
def test():
   return 'OMG'


@app.route('/error_test')
def error_test():
   return api(path="error_test", error="here is an error")

@app.route('/')
def list_files():
    return request.url + ''.join(['<a href="{url}">{series}</a>'.format(url=url_4('series', name=folder), series=folder) for folder in get_series(series=True,old=True)])

@app.route('/series/<name>')
def series(name):
   return str(get_series(path="/{}".format(name), old=True))

@app.route('/api')
def api_root():
    return api()

@app.route('/api/<path>')
def api_path(path):
    return api(path=path)

if __name__ == '__main__':
   app.run(host='0.0.0.0')
