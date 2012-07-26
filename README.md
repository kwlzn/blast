blast
=====

overview
--------

blast is a simple web-based, multi-platform music player written in python, HTML/CSS and javascript.


installation
------------

the easiest way to install blast is by using python setuptools "easy_install" command:

    $ easy_install blast

you can also install using ez_setup, pip or installing the package directly from pypi. 


usage
-----

    $ cd ~/Music
    $ blast

then you can connect to the blast frontend at <http://localhost:5000> (or via IP if you're binding externally with -x).

blast is primarily keystroke driven. here's a list of the available key commands:

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

when in doubt, you can hit the "?" key to see this same list in the UI.

you can also click on tracks to play/pause and seek around in tracks by clicking on the duration bar.


open source
-----------

blast currently leverages the following open source components to speed development:

 - Flask (http://flask.pocoo.org/)
 - SoundManager2 (http://www.schillmania.com/projects/soundmanager2/)
 - SoundManager2 Page Player (http://www.schillmania.com/projects/soundmanager2/demo/page-player/)
 - jQuery (http://jquery.com/)
 - jQuery Shuffle Plugin (http://yelotofu.com/labs/jquery/snippets/shuffle/)
 - Bootstrap (http://twitter.github.com/bootstrap/)
 - Sticky (http://thrivingkings.com/sticky)


contributing
------------

blast is open sourced under a simple BSD license. you can find the source code on github:

 - <https://github.com/kwlzn/blast>
