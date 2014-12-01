Spycis
======

<*Spycis* http://github.com/marcwebbie/spycis>_ is a python console interface to stream websites. With spycis
we can *search*, *download*, *stream locally*, *watch* streaming site
videos with only one command

Installation
------------

Installer
~~~~~~~~~

.. code:: python

    pip install spycis

Update
~~~~~~~~~~~~

.. code:: python

    pip install -U spycis

Uninstall
~~~~~~~~~~~~

.. code:: python

    pip uninstall spycis

Options de ligne de commande de spycis
--------------------------------------

Options de spycis basiques
~~~~~~~~~~~~~~~~~~~~~~~~~~

Les options de Spycis sont active par des "switches" de terminal au
formats: ``-s value`` ou longue ``--switch value``

-  ``-r`` ou ``--raw-urls``: Retourne les raw urls pour le code ou
   specifie. ex: ``-r s02e31`` ou ``--raw-urls  s02e31``
-  ``-s`` ou ``--stream-urls``: Retourne les stream urls pour le code
   specifie. ex: ``-s s02e31`` ou ``--stream-urls  s02e31``
-  ``-p`` ou ``--position``: Options utilise avec ``-r`` ou ``-s`` pour
   specifie la positon[*]. ex: ``-p 2 -r s02e31``

Options bonus
~~~~~~~~~~~~~

Les options des bonus sont toujours utilisees avec ses noms longs pour
ne pas confondre avec les options basiques. Les bonus ne retournent pas
des urls, ils font des actions sur les ``raw urls`` trouvees. Donc, si
spycis n'a pas trouve des ``raw urls`` aucune action sera faite.

-  ``--download``: Telecharge le premier fichier au pattern[2] dans les
   ``raw urls`` extraites. ex: ``--download vostf``
-  ``--play``: Executer le premier fichier au pattern[2] specifie dans les
   ``raw urls`` extraites. ex: ``--play vostf``
-  ``--player``: Choisir le player pour l'option play ex:
   ``--player amarok``
-  ``--subtitles``: Ouvre les sous-titres pour streaming ex:
   ``--subtitles mes_sous_titres.srt``
-  ``--stream``: Ouvre streaming avec fichier choisi par pattern[2]
   specifie. ex: ``--stream video.flv``
-  ``--stream-port``: Change la port pour le streaming. ex:
   ``--stream-port 8080``

Options avancees
~~~~~~~~~~~~~~~~

-  ``--site-list``: Voir la liste de sites disponibles. ex:
   ``--site-lite``
-  ``--site``: Changer le site de recherche. ex: ``--site sitename``
-  ``-v``, ``-vv`` ou ``--verbose``: Activer le mode debogage. ex: -v,
   ``--verbose``, pour plus de debogage ``-vv``:
-  ``--workers``: Nombre des threads pour l'extraction des urls ex:
   ``--workers 20``
-  ``--version``: Voir la version de spycis. ex: ``--version``

    [*] La position est imprime au terminal dans les resultats de
    recherches avec les valeurs entre accolades carres ``[ ]``

    [2] Les patterns sont des expressions regulieres, ``.`` veut dire
    tout, alors que ``mp4$`` veut dire que doit se terminer par ``mp4``
    pour plus d'info lire ici: `tutoriel
    regex <http://lumadis.be/regex/tuto_pcre.php>`__

Tutoriel
--------

Le tutoriel est divise en parties:

1. Les recherches basiques par urls.
2. Les raccourcis de recherche par codes.
3. Les raccourcis de recherche par positions. (*ideal pour les films, ou
   les ambiguitees*)
4. Les recherches par sites.
5. Les options bonus.
6. Les options avancees.

1. Les recherches basiques par urls
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Recherche de serie ou film par titre[*]. Imprime: la position dans ``[...]``, la categorie, le titre, c'annee, le ``media url``:
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

.. code:: bash

    spycis mentalist

Exemple output:


.. code:: bash

    [0]    ['tv-show']   'The Mentalist'                                [2008] (http://www.tubeplus.me/player/1444106/)
    [1]    ['film']      'The Mentalist'                                [2004] (http://www.tubeplus.me/player/558406/)
    [2]    ['film']      'The Mentalist'                                [2011] (http://www.tubeplus.me/player/2086823/)

    [*] Attention: Pour les titres avec des spaces utilises des guillement
    ou doubles guillements. ex: ``spycis "the mentalist"``

Obtenir les ``stream urls`` pour une ``media url``:
'''''''''''''''''''''''''''''''''''''''''''''''''''

.. code:: bash

    spycis http://www.tubeplus.me/player/553643/

Exemple output:


.. code:: bash

    http://www.sockshare.com/embed/F3154F8EADC345F4
    http://gorillavid.in/embed-zpkcdcd8e0hs-650x400.html
    http://gorillavid.in/embed-arlo8rtqin7p-650x400.html
    http://www.vidbux.com/embed-9p3igt5r8k36.html

    \*: **Attention** Cette commande ne marche que pour les films, pour
    obtenir des ``raw urls`` pour les series, le code episode doit etre
    informe avec l'option --raw-url. ex: ``-p 30 -r s01e01``.

Obtenir les ``raw urls`` pour une ``stream url``:
'''''''''''''''''''''''''''''''''''''''''''''''''

.. code:: bash

    spycis http://www.divxstage.eu/video/46b593256e86d

Exemple output :


.. code:: bash

    http://s63.coolcdn.ch/dl/88fbb33139e52637640a5b282347a730/52caa6ef/ff51f6acabefb1e855a45d2ab057ed55dd.flv

2. Les raccourcis de recherche par code.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Les raccourcis de recherche par code sans l'option position va toujours
prendre le premiere position dans les recherches.

Obtenir les ``stream urls`` pour la position par defaul(\ ``0``) dans la recherche avec le code episode ``s02e03``:
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

.. code:: bash

    spycis -s s02e03 "Vampire Diaries"

Exemple output:


.. code:: bash

    http://embed.nowvideo.sx/embed.php?v=5fd0e2c91f94f           [English]       subtitles=[]
    http://vidbull.com/embed-7i1xh24afy1c-650x328.html           [English]       subtitles=[]
    http://embed.nowvideo.sx/embed.php?v=7uf38f5ub01j3           [English]       subtitles=[]
    http://vidbull.com/embed-xu1nnexz2ers-650x328.html           [English]       subtitles=[]
    http://embed.novamov.com/embed.php?v=j9dyd2h9bnvn0           [English]       subtitles=[]
    http://www.divxstage.eu/video/25aadbe169644                  [English]       subtitles=[]
    http://vidbull.com/embed-37iq0bewngk5-650x328.html           [English]       subtitles=[]
    http://vidbull.com/embed-pxm4uio4fe9a-650x328.html           [English]       subtitles=[]

Obtenir les ``raw urls`` pour la position par defaul(\ ``0``) dans la recherche avec le code episode ``s02e03``:
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

.. code:: bash

    spycis -r s02e03 "Vampire Diaries"

Exemple output:


.. code:: bash

    http://50.7.161.75:182/d/z5sj6h3iljrwuxim4y6sl4qu6gqlucqvfdxuelpkzxvacn37sxj6oc74/video.mp4
    http://s32.coolcdn.ch/dl/dd361f0f4d8e911f31cb8c7f569828a5/52ca4a40/ff9ffca598779e196b4e5190f74f554189.flv
    http://s82.coolcdn.ch/dl/f46549bc003bd0e5d04e3159ca264c6b/52ca4a40/ffec6671b8c36f0348ae0ef4e119f49d64.flv
    http://fs16ssd.vidbull.com:182/d/zrshafliljrwuxim4y6wv3qu44s5xp5gx3mw22s7pvn6yqks7fgo27sn/video.mp4
    http://s82.coolcdn.ch/dl/1b7bf3370a866aedf3a401a84c22e014/52ca4a79/ffec6671b8c36f0348ae0ef4e119f49d64.flv
    http://fs16ssd.vidbull.com:182/d/zrsc2utiljrwuxim4y6wv3qu47ibh67chhnpui3v25wplfsy522ks6oe/video.mp4
    http://s33.coolcdn.ch/dl/813c3b2938dec203a3e6769fb4f5549f/52ca4c1f/ff9ffca598779e196b4e5190f74f554189.flv

3. Les racourcis de recherche par positions.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Obtenir les ``stream urls`` pour la position de recherche ``1`` avec le code episode ``s01e16``:
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

.. code:: bash

    spycis -p 1 -s s01e16 house

Exemple output:


.. code:: bash

    http://www.putlocker.com/embed/4EB13DEA60C9EF28              [English]       subtitles=[]
    http://gorillavid.in/embed-kdk7i5r1p5ye-650x400.html         [English]       subtitles=[]
    http://www.sockshare.com/embed/0830C86867F3EE66              [English]       subtitles=[]
    http://gorillavid.in/embed-iabh7e6bchgq-650x400.html         [English]       subtitles=[]
    http://gorillavid.in/embed-30y7ahav048u-650x400.html         [English]       subtitles=[]

Obtenir les ``raw urls`` pour la position de recherche ``1`` avec le code episode ``s01e16``.
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

.. code:: bash

    spycis -p 1 -r s01e16 house

Exemple output:


.. code:: bash

    http://50.7.164.186:8182/kworoewk46u4tqukwzalnftgklqs2kbmdlytomyiaeprqqbbp3wz2kacjm/video.flv
    http://50.7.164.186:8182/kworpnaf56u4tqukwzalnftgkir5zdscugtrcngs4yvpqhozx6axvbhhve/video.flv
    http://50.7.164.186:8182/kworpnqf56u4tqukwzalnftgkkeynchx4tkfeod7o7gdaoyus5e47r6xlq/video.flv

Obtenir les ``raw urls`` pour la position de recherche ``30``: [\*]
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

.. code:: bash

    spycis -p 30 "Lion King"

Exemple output:


.. code:: bash

    http://50.7.164.218:8182/46or2vj77su4tqukwyq3nbzwlkn5arxroclhufzikh4jpmzwrldtpm7z4u/video.flv
    http://50.7.164.218:8182/46or2vr77su4tqukwyq3nbzwllazlxk4tcokrqmk6bg3q3nlbivlfet7mi/video.flv

    \*: **Attention** Cette commande ne marche que pour les films, pour
    obtenir des ``raw urls`` pour les series, le code episode doit etre
    informe avec l'option --raw-url. ex: ``-p 30 -r s01e01``.

4. Les recherches par site
~~~~~~~~~~~~~~~~~~~~~~~~~~

Lister les sites disponibles:
'''''''''''''''''''''''''''''

.. code:: bash

    spycis --site-list

Exemple output:


.. code:: bash

    List of available sites:
      loveserie
      example
      tubeplus

Faire recherche sur un site alternatif:
'''''''''''''''''''''''''''''''''''''''

.. code:: bash

    # Rechercher sur le site "loveserie" les stream urls pour le episode `s01e08` de deadwood au
    spycis --site loveserie -s s01e08 deadwood

Exemple output:


.. code:: bash

    http://youwatch.org/l0lqxt7w5t25                             [English]       subtitles=['French']
    http://youwatch.org/cd49rhqmpbps                             [French]        subtitles=[]
    http://www.duckstreaming.com/lm0fhyxsrhxj                    [French]        subtitles=[]

5. Les options bonus
~~~~~~~~~~~~~~~~~~~~

Option ``--play``: Regarder une video
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Regarder "Le Roi Lion" sur vlc:
'''''''''''''''''''''''''''''''

.. code:: bash

    spycis --play -p 30 "The Lion King"

Example output:


.. code:: bash

    http://50.7.164.218:8182/46or2vr77su4tqukwyq3nbzwllazlxk4tcokrqmk6bg3q3nlbivff237mi/video.flv
    http://50.7.164.218:8182/46or2vj77su4tqukwyq3nbzwlkn5arxroclhufzikh4jpmzwrld5psxz4u/video.flv
     * Playing url: http://50.7.164.218:8182/46or2vr77su4tqukwyq3nbzwllazlxk4tcokrqmk6bg3q3nlbivff237mi/video.flv
    VLC media player 2.1.2 Rincewind (revision 2.1.2-0-ga4c4876)
    [0x2273048] main libvlc: Running vlc with the default interface. Use 'cvlc' to use vlc without interface.

Option ``--player``: Changer le lecteur video
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Regarder l'episode 7 de saison 5 de "Vampire Diaries" sur mplayer:
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

.. code:: bash

    spycis --play --player mplayer -r s05e07 "vampire diaries"

Option ``--download``: Telecharger une video
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Telecharge l'episode 7 de saison 5 de "Vampire Diaries":
''''''''''''''''''''''''''''''''''''''''''''''''''''''''

.. code:: bash

    spycis --download -r s05e07 "vampire diaries"

Option ``--stream``: Streaming d'une video
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Faire streaming du film 'Roi Lion':
'''''''''''''''''''''''''''''''''''

.. code:: bash

    spycis --stream -p 30 "lion king"

Faire streaming de l'episode 7 de saison 5 de "Vampire Diaries":
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

.. code:: bash

    spycis --stream -r s05e07 "vampire diaries"

Faire du streaming d'une ``raw url``:


.. code:: bash

    spycis --stream http://s63.coolcdn.ch/dl/59fd759b1e855a45d2ab057ed55dd.mp4

Faire du streaming d'une ``stream url``:
''''''''''''''''''''''''''''''''''''''''

.. code:: bash

    spycis --stream http://embed.nowvideo.sx/embed.php?v=5fd0e2c91f94f

Exemple output:


.. code:: bash

    http://s32.coolcdn.ch/dl/e4ed66cb4caee3a4d66a46e524d9c133/52cdcc05/ff9ffca598779e196b4e5190f74f554189.flv
    Glissez les sous-titres pour 'the.vampire.diaries.s02e03.dvdrip.xvidreward' ici :
     * Chosen file: http://s32.coolcdn.ch/dl/e4ed66cb4caee3a4d66a46e524d9c133/52cdcc05/ff9ffca598779e196b4e5190f74f554189.flv
     * Streaming from: 192.168.25.8:8080
    VLC media player 2.1.2 Rincewind (revision 2.1.2-0-ga4c4876)
    [0x10ab9a8] dummy interface: using the dummy interface module...

Utiliser pattern pour stream de la version francaise de under the dome s01e01 sur le site ``loveserie``:
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

.. code:: bash

    spycis --site loveserie --stream --pattern FRENCH -r s01e01 "under the dome"

Exemple output:


.. code:: bash

    # le pattern choisi le fichier que a le mot 'FRENCH'
    http://fs2.youwatch.org:8777/ytv7tqhdekoax3ptx2bindnq66k2ymiojy67sa4je2zd7y3gi7nxelb2ai/video.mp4
    http://fs15.youwatch.org:8777/exv75i7dh6oax3ptx25ynrp5uq77jyflkxa5n5qs3imzxtasd2mn4szdua/video.mp4
    Glissez les sous-titres pour 'Download.Under.The.Dome.S01E01.FRENCH.BDRip.XviD.MiND.avi' ici :

Option ``--subtitles``: Streaming d'une video avec sous-titres
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Fait du streaming de l'episode 7 de saison 5 de "Vampire Diaries" avec sous-titres:
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

.. code:: bash

    spycis --stream --subtitles vampire_soustitres.srt -r s05e07 "vampire diaries"

Fait du streaming d'une raw url avec sous-titres:
'''''''''''''''''''''''''''''''''''''''''''''''''

.. code:: bash

    spycis --stream --subtitles vampire_soustitres.srt http://s63.coolcdn.ch/dl/59fd759b1e855a45d2ab057ed55dd.mp4

Fait du streaming d'un fichier local avec sous-titres:
''''''''''''''''''''''''''''''''''''''''''''''''''''''

.. code:: bash

    spycis --stream --subtitles messoustitres.srt /home/user/Videos/ma_video_local.mp4

Option ``--stream-port``: Streaming d'une video sur une port specifie
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Faire streaming du film 'Roi Lion' sur la porte ``9000``. **note**: La porte par default c'est la 8080:
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

.. code:: bash

    spycis --stream --stream-port 9000 -p 30 "lion king"

Exemple output:


.. code:: bash

    http://50.7.164.218:8182/46or2vj77su4tqukwyq3nbzwlkn5arxroclhufzikh4jpmzwrld7dspz4u/video.flv
    http://50.7.164.218:8182/46or2vr77su4tqukwyq3nbzwllazlxk4tcokrqmk6bg3q3nlbivhj2d7mi/video.flv
    Glissez les sous-titres pour 'zpkcdcd8e0hs.flv' ici :
     * Chosen file: http://50.7.164.218:8182/46or2vj77su4tqukwyq3nbzwlkn5arxroclhufzikh4jpmzwrld7dspz4u/video.flv
     * Streaming from: 192.168.25.8:9000
    VLC media player 2.1.2 Rincewind (revision 2.1.2-0-ga4c4876)
    [0x937938] dummy interface: using the dummy interface module...

6. Les options avancees
~~~~~~~~~~~~~~~~~~~~~~~

Voir la version de spycis installe:
'''''''''''''''''''''''''''''''''''

.. code:: bash

    spycis --version

Exemple output:


.. code:: bash

    Spycis v0.0.1

Executer spycis en mode verbose avec ``-v`` ou ``--verbose``:
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

.. code:: bash

    spycis -vv 'lion king'

Executer spycis en mode verbose avec information de debogage plus approfondie avec ``-vv``:
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

.. code:: bash

    spycis -vv 'lion king'

Changer le nombre de threads utilise par ``3``:
'''''''''''''''''''''''''''''''''''''''''''''''

.. code:: bash

    spycis --workers 3 'lion king'

Architecture de spycis
----------------------

Spycis fournit trois types de urls

-  **media urls**: L'adresse de la page sur le site ou spycis a trouve
   le media(serie/film/musique). Ces pages ont normalement l'information
   sur le media aussi comme plusieurs stream urls. exemple:
   ``http://www.filmesonlinegratis.net/assistir-12-anos-de-escravidao-legendado-online.html``
-  **stream urls**: L'adresse de la page d'un site de streaming. Sur ces
   pages nous pouvons regarder les videos en ligne sans avoir besoin de
   telecharger la video. les sites 'youtube', 'dailymotion', 'vimeo'
   sont des sites de streaming. example de stream url :
   ``http://www.youtube.com/watch?v=VAJ8wZ97x94``
-  **raw urls**: L'adresse du vrai fichier, avec cette url nous pouvons
   telecharger la video sur l'ordinateur. Ces liens sont normalement
   caches du publique(pour faire les utilisateur regarder les videos sur
   leur stream urls). exemple de une raw url:
   ``http://50.7.161.75:182/d/z5sj6h3iljrwuxim4y6sl4qu6gqlucqvfdxuelpkzxvacn37sxj6oc74/video.mp4``
