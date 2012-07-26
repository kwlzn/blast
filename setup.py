import os
from setuptools import setup, find_packages

setup(
       name='blast',
       version='0.3.0',
       description='blast',
       keywords='python wsgi web mp3 player javascript html music audio',
       author='kw',
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
                     'Environment :: Web Environment',
                     'Operating System :: OS Independent',
                     'Programming Language :: Python',
                     'Programming Language :: Javascript',
                     'Programming Language :: HTML',
                     'Topic :: Multimedia :: Sound/Audio :: Players :: MP3'
                   ]
     )