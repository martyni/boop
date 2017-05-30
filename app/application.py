from flask import Flask, request, url_for, redirect
import boto3
from pprint import pprint

app = Flask(__name__)
client = boto3.client("s3")

def url_4(*args, **qwargs):
   raw_path = url_for(*args, **qwargs)
   if ".amazonaws.com" not in request.url:
      return raw_path.replace('/prod', '').replace('/stge', '').replace('/dev', '')
   else:
      return raw_path

def get_files(Bucket="martyni-boop", path="", folders=False):
    blob = client.list_objects_v2(Bucket="martyni-boop")
    contents = blob['Contents']
    if not folders:
       return '\n'.join(f['Key'] for f in contents if "/" not in f['Key'])
    elif folders:
        return [f['Key'][:-1:] for f in contents if "/" in f['Key']]

@app.route('/test')
def test():
   return 'OMG'

@app.route('/')
def list_files():
    return request.url + ''.join(['<a href="{url}">{series}</a>'.format(url=url_4('series', name=folder), series=folder) for folder in get_files(folders=True)])

@app.route('/series/<name>')
def series(name):
   return get_files(path="/{}".format(name))

if __name__ == '__main__':
   app.run(host='0.0.0.0')
