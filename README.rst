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

| Copyright © 2013-2014 Marcwebbie, http://github.com/marcwebbie
|
| Permission is hereby granted, free of charge, to any person obtaining
| a copy of this software and associated documentation files (the
| "Software"), to deal in the Software without restriction, including
| without limitation the rights to use, copy, modify, merge, publish,
| distribute, sublicense, and/or sell copies of the Software, and to
| permit persons to whom the Software is furnished to do so, subject to
| the following conditions:
|
| The above copyright notice and this permission notice shall be
| included in all copies or substantial portions of the Software.
|
| THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
| EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
| MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
| NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
| LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
| OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
| WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
