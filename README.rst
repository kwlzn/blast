=====
blast
=====

overview
--------

blast is a simple web-based, multi-platform music/mp3 player written in python, HTML/CSS and javascript.


installation
------------

the easiest way to install blast is by using python setuptools "easy_install" command:

::

    $ easy_install blast

you can also install using ez_setup, pip or installing the package directly using setup.py:

::

    $ python setup.py install


usage
-----

::

    $ cd ~/Music
    $ blast

then you can connect to the blast frontend at http://localhost:5000 (or via IP if you're binding externally with -x).

NOTE: if you use flashblock, make sure to whitelist your blast server (otherwise the URLs will simply open as if you clicked them)


blast is primarily keystroke driven. here's a list of the available key commands:

::

      v         Play
      c         Toggle Pause
      x         Stop
      j k       Next / Previous Track (Google Reader style)
      n         Next Track (same as j, Google Reader style)
      b z       Next / Previous Track (Winamp Style)  
      , .       Reverse or Skip Ahead 1 second
      { }       Reverse or Skip Ahead 5 seconds
      [ ]       Reverse or Skip Ahead 30 seconds
      0         Reset to 0 position
      s         Toggle Shuffle
      m         Toggle Mute
      ?         Toggle Help
      r         Randomize List
      d         Debug Mode

when in doubt, you can also hit the "?" key in the UI to see this same help information.

in addition to key commands, you can click on tracks to play/pause and seek around in tracks by clicking on the duration bar.

platform support
----------------

blast is written with portability in mind. currently the server (the blast CLI) should run anywhere that python can be installed (pretty much everywhere) and the UI should run in most browsers. the UI is also known to work under iOS (e.g. for iPhone/iPad playback) - which means you can stream your large computer-based library to your iOS device over wifi.

tested/verified platforms
~~~~~~~~~~~~~~~~~~~~~~~~~

- blast server
    - OSX python
    - Cygwin (Windows) python
    - Linux python

- front-end/UI
    - OSX chrome
    - OSX safari 
    - OSX firefox
    - iOS safari (iPhone/iPad)
    - Windows chrome
    - Windows firefox

untested, but might work on
~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Windows python (non-cygwin) and/or ActiveState python
- Other UNIXs (BSD, Solaris etc) python
- Windows Internet Explorer
- Opera
- Android

open source
-----------

blast currently leverages the following open source components to speed development:

- Flask (http://flask.pocoo.org/)
- SoundManager2 (http://www.schillmania.com/projects/soundmanager2/)
- SoundManager2 Page Player (http://www.schillmania.com/projects/soundmanager2/demo/page-player/)
- jQuery / jQueryUI (http://jquery.com/, http://jqueryui.com)
- jQuery Shuffle Plugin (http://yelotofu.com/labs/jquery/snippets/shuffle/)
- Bootstrap (http://twitter.github.com/bootstrap/)
- Sticky (http://thrivingkings.com/sticky)


contributing
------------

blast is open sourced under a simple BSD license. you can find the source code on github:

- https://github.com/kwlzn/blast
