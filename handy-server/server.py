#!/usr/bin/env python3

from flask import Flask, render_template, redirect, request
from subprocess import CalledProcessError, Popen, check_output
from base64 import b64decode, urlsafe_b64encode


app = Flask(__name__, template_folder='./')


@app.route('/youtube-dl', methods=['GET'])
def youtube_dl():
    """Show output from youtube-dl utility as list of URLs. If there is
    only one URL redirect to vlc route.
    """
    urls = []
    if 'url' in request.args:
        url = b64decode(request.args['url'])
        app.logger.info(f"decoded url is '{url}'")
        try:
            urls = check_output(
                ['youtube-dl', '-f', 'best', '-g', url],
                encoding='utf-8',
            ).split()
        except CalledProcessError:
            pass

    urls = [build_url(url.encode('utf-8')) for url in urls]
    if len(urls) == 1:
        return redirect(f"/vlc?url={urls[0]['base64']}")
    else:
        return render_template("youtube-dl.html", urls=urls)


@app.route('/vlc', methods=['GET'])
def vlc():
    """Open vlc with requested url
    """
    if 'url' not in request.args:
        return 'url not found'

    url = b64decode(request.args['url'])
    process = Popen(['vlc', url])
    app.logger.info(f"running video {url} in vlc (PID = {process.pid})")
    return f'running video in vlc (PID = {process.pid})'


def build_url(url):
    return {
        'base64': str(urlsafe_b64encode(url), 'utf-8'),
        'encoded': str(url, 'utf-8')
    }


if __name__ == "__main__":
    app.run()
