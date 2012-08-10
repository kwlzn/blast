#!/usr/bin/env python
#
# blast
#

import os, sys, urllib, re
from flask import Flask, Response, render_template, url_for, send_from_directory, stream_with_context
from blast.scanner import DirScanner

ALLOWED_TYPES = ['.mp3', '.m4a']

## Initialize flask
app = Flask(__name__)
app.config['DEBUG']      = True
app.config['SECRET_KEY'] = 'blast'
app.config['USERNAME']   = 'admin'
app.config['PASSWORD']   = 'blastadmin'

@app.errorhandler(401)
def page_not_authorized(error): return render_template('401.html'), 401

@app.errorhandler(404)
def page_not_found(error): return render_template('404.html'), 404

@app.errorhandler(500)
def ise(error): return render_template('500.html'), 500

@app.route('/favicon.ico')
def favicon():
    return app.send_static_file('favicon.ico')

## courtesy of http://flask.pocoo.org/docs/patterns/streaming/
def stream_template(template_name, **context):
    ''' allow streaming of jinja templates for reduced page load start latency (e.g. for large lists) '''
    app.update_template_context(context)
    t = app.jinja_env.get_template(template_name)
    rv = t.stream(context)
    rv.enable_buffering(5)
    return rv

def unescape_utf8(msg):
    ''' convert escaped unicode web entities to unicode '''
    def sub(m):
        text = m.group(0)
        if text[:3] == "&#x": return unichr(int(text[3:-1], 16))
        else:                 return unichr(int(text[2:-1]))
    return re.sub("&#?\w+;", sub, urllib.unquote(msg))

def escape_utf8(msg):
    ''' convert unicode strings to web safe escaped text entities '''
    return urllib.quote(msg.decode('utf-8').encode('ascii', 'xmlcharrefreplace'))

def iterplayables():
    ''' fast iterator of playable file object/dicts found on disk '''
    ls = DirScanner(stripdot=True)
    ## filter out just mp3 files (and dirs to support recursion)
    filt = lambda x: ( os.path.isdir(x) or x[-4:].lower() in ALLOWED_TYPES )
    ## take the last two segments of the path as the label
    func = lambda x: '/'.join(x.split('/')[-2:])
    ## iterate over all the files (excluding dirs), filtering for .mp3 and .m4a
    for x,y in ls.iteritems(want_files=True, want_dirs=False, func=func, filt=filt):
        yield {      'name': x.decode('utf-8'),
                'file_name': escape_utf8(y)     }

@app.route('/')
def playh():
    return Response( stream_template('play.html', entries=stream_with_context(iterplayables())) )

@app.route('/viz')
def vizh():
    return render_template('viz.html')

@app.route('/play/json')
def jsonh():
    return Response( stream_template('files.json', entries=stream_with_context(iterplayables())) )

@app.route('/play/<path:file_str>')
def play_fileh(file_str):
    file_str = unescape_utf8(file_str)
    ## block serving of all other file types (and subdirs via ..) for security reasons
    if ( os.path.splitext(file_str)[1].lower() not in ALLOWED_TYPES or '../' in file_str ):
        return render_template('401.html'), 401
    
    base_dir  = os.path.abspath(os.getcwd())
    file_name = os.path.join(base_dir, file_str)
    if not os.path.exists(file_name):
        print 'ERROR: file "%s" doesnt exist' % file_name
        return render_template('404.html'), 404
    
    dirname, basename = os.path.dirname(file_name), os.path.basename(file_name)
    ## one more validation that the file we're serving is coming from cwd
    if not dirname[:len(base_dir)] == base_dir: return render_template('401.html'), 401
    return send_from_directory(dirname, basename)

#@app.route('/dupes')
#def dupes():
#    #searchword = request.args.get('key', '')
#    ls = DirScanner(os.getcwd())
#    entries = []
#    for x in ls.iterdupes():
#        entries.append( {'title': x[0], 'text': x[1]} )
#    return render_template('dupes.html', entries=entries)

def usage(bail=False):
    print ''' usage: cd /path/to/some/mp3s && blast
    
              options
              -------
                -h        Print this help screen
                -x        Run externally (otherwise binds only to localhost)
                -d        Daemonize (run in background)
          '''
    if bail: sys.exit(0)

def run_as_daemon(func, *args, **kwargs):
    ## retain cwd (our basedir)
    cwd = os.getcwd()
    ## double fork
    pid = os.fork()
    if (pid == 0):
        os.setsid()
        pid = os.fork()
        if (pid == 0):
            ## forked twice and ready to run
            print 'pid: %s, cwd: %s' % (os.getpid(), cwd)
            os.chdir(cwd)
            os.umask(0)
            sys.stdout.flush(), sys.stderr.flush(), sys.stdin.close()
            ## TODO: take log name argument to -d and write stdout/err to log
            func(*args, **kwargs)
        else:
            os._exit(0)
    else:
        os._exit(0)
    return

def main():
    if '-h' in sys.argv or '--help' in sys.argv: usage(bail=True)
    host = '0.0.0.0' if ('-x' in sys.argv) else '127.0.0.1'
    
    if '-d' in sys.argv: run_as_daemon(app.run, **{'host': host})
    else:                app.run(host=host)

if __name__ == '__main__':
    main()
