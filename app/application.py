from flask import Flask
import boto3

app = Flask(__name__)
client = boto3.client("s3")
@app.route('/test')
def test():
   return 'OMG'

@app.route('/')
def list_files():
    blob = client.list_objects_v2(Bucket="martyni-boop")
    contents = blob['Contents']
    print contents
    return [f['Key'] for f in contents][0]

if __name__ == '__main__':
   app.run(host='0.0.0.0')
