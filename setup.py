import os, sys, subprocess
from setuptools import setup, find_packages

def read(f):
    return open(os.path.join(os.path.dirname(__file__), f)).read()

os.environ['COPYFILE_DISABLE'] = 'true'    ## turn off annoying dot files on OSX

if len(sys.argv) > 1 and sys.argv[1] == '--release':
    print('[ Releasing! ]')
    cmd = '%s setup.py sdist upload' % sys.executable
    subprocess.call(cmd, shell=True)

elif len(sys.argv) > 1 and sys.argv[1] == '--clean':
    print('[ Cleaning up ]')
    files = ['blast.egg-info', 'dist']
    cmd = 'rm -rvf ' + ' '.join(files)
    print('Running command: %s' % cmd)
    subprocess.call(cmd, shell=True)

else:
    setup(
           name='blast',
           version=read('VERSION').strip(),
           description='a simple web-based, multi-platform music/mp3 player written in python, HTML/CSS and javascript',
           long_description=read('README.rst'),
           keywords='python wsgi web mp3 player javascript html music audio',
           author='kw',
           author_email='pypi@onoku.com',
           url='http://github.com/kwlzn/blast',
           license='BSD',
           zip_safe=False,
           packages=['blast'],
           package_data={ '': [ 'templates/*.html',
                                'static/*.js',
                                'static/*.css',
                                'static/*.ico',
                                'static/*.png',
                                'static/swf/*.swf',
                                'static/swf/*.zip' ] },
           install_requires=['flask'],
           entry_points={ 'console_scripts': [ 'blast = blast.main:main' ] },
           classifiers=[
                         'Development Status :: 4 - Beta',
                         'License :: OSI Approved :: BSD License',
                         'Environment :: Console',
                         'Environment :: Web Environment',
                         'Operating System :: OS Independent',
                         'Programming Language :: Python',
                         'Programming Language :: JavaScript',
                         'Topic :: Multimedia :: Sound/Audio :: Players :: MP3',
                         'Topic :: Internet :: WWW/HTTP :: WSGI',
                         'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
                         'Topic :: Internet :: WWW/HTTP',
                         'Topic :: Software Development :: Libraries :: Python Modules',
                       ]
         )
