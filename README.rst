######
Spycis
######

<*Spycis* http://github.com/marcwebbie/spycis>_ is a python console interface to stream websites. With spycis
we can *search*, *download*, *stream locally*, *watch* streaming site
videos with only one command

************
Installing
************

Installer
=========

.. code:: bash

    pip install spycis

Update
======

.. code:: bash

    pip install -U spycis

Uninstall
=========

.. code:: bash

    pip uninstall spycis


Quickstart
==========

.. code:: bash

   # searching for available streams
   spycis "Breaking Bad"

   # getting stream url for episode 6 from season 4 of Breaking Bad
   spycis "Breaking Bad" -s s04e06

   # getting download url for episode 6 from season 4 of Breaking Bad
   spycis "Breaking Bad" -r s04e06

   # downloading episode 6 from season 4 of Breaking Bad
   # requires: wget
   spycis "Breaking Bad" -s s04e06 --download

   # stream episode 6 from season 4 of Breaking Bad
   # requires: vlc
   spycis "Breaking Bad" -s s04e06 --stream

   # play episode 6 from season 4 of Breaking Bad
   # requires: vlc
   spycis "Breaking Bad" -s s04e06 --play

   # play episode 6 from season 4 of Breaking Bad with subtitles
   # requires: vlc
   spycis "Breaking Bad" -s s04e06 --play --subtitles /path/to/subtitles.srt


*************
License (MIT)
*************

| DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
|                    Version 2, December 2004
|
| Copyright (C) 2013 Marc Webbie <https://github.com>
|
| Everyone is permitted to copy and distribute verbatim or modified
| copies of this license document, and changing it is allowed as long
| as the name is changed.
|
| DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
| TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION
|
| 0. You just DO WHAT THE FUCK YOU WANT TO.
