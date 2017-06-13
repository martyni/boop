from flask import Flask, Response, request, url_for, redirect, jsonify, render_template, make_response, request, current_app
from feedgen.feed import FeedGenerator
import boto3
from datetime import datetime, timedelta
from functools import update_wrapper
import re
from requests import get

app = Flask(__name__)
client = boto3.client("s3")

cache = {}
time_format = "%Y-%M-%d %H:%M:%s"
author = "Martyn Pratt"
email = "martynjamespratt@gmail.com"
s3_link = "https://s3-eu-west-1.amazonaws.com/{}/"


def url_sanitizer(raw_path):
    if ".amazonaws.com" not in request.url:
        return raw_path.replace('/prod', '').replace('/stge', '').replace('/dev', '')
    else:
        return raw_path


def path_sanitizer(raw_path):
    return raw_path.lower().replace("_", " ")


def url_4(*args, **qwargs):
    raw_path = url_for(*args, **qwargs)
    return url_sanitizer(raw_path)


def time_dump():
    return datetime.utcnow().strftime(time_format)


def time_load(time_string):
    return datetime.strptime(time_string, time_format)


def time_diff(time_1, time_2):
    if type(time_1) == str:
        time_1 = datetime.strptime(time_1,  time_format)
    if type(time_2) == str:
        time_2 = datetime.strptime(time_2,  time_format)
    return time_1 - time_2

def crossdomain(origin=None, methods=None, headers=None,
                max_age=21600, attach_to_all=True,
                automatic_options=True):
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, basestring):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, basestring):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers

            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator


def parse_series_and_episodes(s3_list, path=None, s3_link=""):
    series = {}
    if not path:
        path = '[a-z\s]*'
    for _ in s3_list:
        m = re.match('({})/$'.format(path), _)
        if m:
            series[m.group(1)] = {}

        m = re.search('({})/([0-9]*)/$'.format(path), _)
        if m:
            series[m.group(1)][m.group(2)] = {}

        m = re.search('({})/description.txt$'.format(path), _)
        if m:
            series[m.group(1)]["description"] = get(
                s3_link.format(path) + m.group(1) + '/description.txt').text

        m = re.search('({})/([a-z_]*)\.png$'.format(path), _)
        if m:
            series[m.group(1)]["image"] = s3_link.format(path) + m.group(0) 
            series[m.group(1)]["image_title"] = path_sanitizer(m.group(2)).title() 

        m = re.search('({})/([0-9]*)/(.*).mp3$'.format(path), _)
        if m:
            series[m.group(1)][m.group(2)][m.group(3)] = {
                "mp3": s3_link + m.group(0)}

        m = re.search('({})/([0-9]*)/(.*).txt$'.format(path), _)
        if m:
            series[m.group(1)][m.group(2)][m.group(
                3)]["txt"] = s3_link + m.group(0)
    return series


def get_series(Bucket="martyni-boop", path="", series=False, old=False):
    if cache.get(path):
        blob = cache.get(path)
    else:
        blob = client.list_objects_v2(
            Bucket="martyni-boop", Prefix=path_sanitizer(path))
        cache[path] = blob
        cache[path]["date"] = time_dump()
    contents = blob.get('Contents', None)
    if contents is not None:
        s3_list = [f['Key'] for f in contents]
        return parse_series_and_episodes(s3_list, path, s3_link=s3_link.format(Bucket))
    else:
        blob["error"] = "No Contents found in S3"
        return blob


def api(path="", error=None, meta={}):
    error_status_code = 400
    path = path_sanitizer(path)
    payload = {
        "error": error,
        "path": path,
        "response": {},
        "meta": meta
    }
    payload["meta"]["date"] = time_dump()
    payload["meta"]["url"] = url_sanitizer(request.url)
    payload["meta"]["remote_addr"] = request.remote_addr
    payload["meta"]["user_agent"] = str(request.user_agent)
    payload["meta"]["status"] = 200
    payload["response"] = get_series(path=path)
    if payload["response"].get("error"):
        payload["error"] = payload["response"]["error"]
    if not payload["response"]:
        payload["error"] = "Series {} not found".format(path)
    if not payload["error"]:
        return jsonify(payload)
    else:
        payload["meta"]["status"] = error_status_code
        response = jsonify(payload)
        response.status_code = error_status_code
        return response


@app.route('/test')
def test():
    return 'OMG'


@app.route('/error_test')
def error_test():
    return api(path="error_test", error="here is an error")


@app.route('/')
def list_files():
    request_path = url_4("list_files")
    request_path = request_path + "/" if request_path[-1] != "/" else request_path
    print request_path
    return render_template("base.html", request_path=request_path, links={"api_root": url_4("api_root")})


@app.route('/rss/<path>')
def rss_creation(path):
    path        = path_sanitizer(path)
    title       = path.title()
    url         = url_sanitizer(request.url)
    raw_series  = get_series(path=path)
    series      = raw_series.get(path)
    if not series:
        return api(path=request.path, error="No Series found", meta={"s3_response": raw_series})
    description = series.get("description", "generic podcast")
    fg          = FeedGenerator()
    fg.load_extension('podcast')
    fg.id(url)
    fg.title(title)
    fg.podcast.itunes_category('Technology', 'Podcasting')
    fg.author({'name': author, 'email': email})
    fg.link(href=url, rel='self')
    fg.description(description)
    fg.image(url=series.get("image", "https://s3-eu-west-1.amazonaws.com/martyni-boop/default.png"),
             title=series.get("image_title", "Default"),
             link="http://blah.com/image",
             width='123',
             height='123',
             description=description)
    series = {s: series[s] for s in series if type(series[s]) == dict}
    for season in series:
        for episode in series[season]:
            fe = fg.add_entry()
            fe.id(series[season][episode]["mp3"])
            fe.title(path_sanitizer(episode).title())
            fe.description(get(series[season][episode]["txt"]).text)
            fe.enclosure(series[season][episode]["mp3"], 0, 'audio/mpeg')
            fe.link(href=request.url, rel='alternate')
            fe.author(name=author, email=email)
    return Response(fg.rss_str(), mimetype='text/xml')


@app.route('/api')
@crossdomain("*")
def api_root():
    return api()


@app.route('/api/<path>')
@crossdomain("*")
def api_path(path):
    return api(path=path)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
