####################################
Spycis: Get url from stream websites
####################################

`Spycis <http://github.com/marcwebbie/spycis>`_ is a python console interface to stream websites. With spycis can *search*, *download*, *stream locally*, *watch* streaming site videos with only one command.

************
Installing
************

Install
=========

.. code-block:: bash

    pip install spycis

Update
======

.. code-block:: bash

    pip install -U spycis

Uninstall
=========

.. code-block:: bash

    pip uninstall spycis

Quickstart
==========

.. code-block:: bash

   # searching for available streams
   spycis "Breaking Bad"

   # getting stream url for episode 6 from season 4 of Breaking Bad
   spycis "Breaking Bad" -s s04e06

   # getting download url for episode 6 from season 4 of Breaking Bad
   spycis "Breaking Bad" -r s04e06

   # downloading episode 6 from season 4 of Breaking Bad
   # requires: wget
   spycis "Breaking Bad" -r s04e06 --download

   # stream episode 6 from season 4 of Breaking Bad
   # requires: vlc
   spycis "Breaking Bad" -r s04e06 --stream

   # play episode 6 from season 4 of Breaking Bad
   # requires: vlc
   spycis "Breaking Bad" -r s04e06 --play

   # play episode 6 from season 4 of Breaking Bad with subtitles
   # requires: vlc
   spycis "Breaking Bad" -r s04e06 --play --subtitles /path/to/subtitles.srt

   # list available sites
   # spycis --site-list


***************
Writing plugins
***************

Wrappers
========

Wrappers are stream website scrapers. They find stream urls on the given site and return a list of Media objects representing them.

- Write a module with the name of the website wrapped
- Create a subclass `spycis.wrappers.common.BaseWrapper`
- Drop the module into `spycis.wrappers` package

Extractors
==========

Extractors find direct download url in stream urls found by Wrappers.

- Write a module with the name of the stream website from where you extract urls
- Create a subclass `spycis.wrappers.common.BaseExtractor`
- Drop the module into `spycis.extractors` package


***************
License (WTFPL)
***************

| DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
|                    Version 2, December 2004
|
| Copyright (C) 2013-2014 Marc Webbie `<https://github.com/marcwebbie>`_
|
| Everyone is permitted to copy and distribute verbatim or modified
| copies of this license document, and changing it is allowed as long
| as the name is changed.
|
| DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
| TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION
|
| 0. You just DO WHAT THE FUCK YOU WANT TO.
