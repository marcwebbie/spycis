Spycis
==========================

_Spycis_ is a python console interface to stream websites. With spycis we can _search_, _download_, _stream locally_, _watch_ streaming site videos with only one command

## Installation

### Installer

```python
pip install https://bitbucket.org/marcwebbie/spycis/get/master.zip
```

### Mètre-à-jour

```python
pip install -U https://bitbucket.org/marcwebbie/spycis/get/master.zip
```

### Désinstaller

```python
pip uninstall https://bitbucket.org/marcwebbie/spycis/get/master.zip
```

## Options de ligne de commande de spycis

### Options de spycis basiques

les options de Spycis sont activé par des "switches" de terminal au formats: `-s value` ou longue `--switch value`

+ `-r` ou `--raw-urls`: Retourne les raw urls pour le code ou specifié. ex: `-r s02e31` ou `--raw-urls  s02e31`
+ `-s` ou `--stream-urls`: Retourne les stream urls pour le code specifié. ex: `-s s02e31` ou `--stream-urls  s02e31`
+ `-p` ou `--position`: Options utilisé avec `-r` ou `-s` pour specifié la positon¹. ex: `-p 2 -r s02e31`

### Options bonus

+ `--download`: Télécharge le premier fichier au pattern² dans les `raw urls` extraites. ex: `--download vostf`
+ `--play`: Executer le premier fichier au pattern² spécifié dans les `raw urls` extraites. ex: `--play vostf`
+ `--player`: Choisir le player pour l'option play ex: `--player amarok`
+ `--subtitles`: Ouvre les sous-titres pour streaming ex: `--subtitles mes_sous_titres.srt`
+ `--stream`: Ouvre streaming avec fichier choisi par pattern² specifié. ex: `--stream video.flv`
+ `--stream-port`: Change la port pour le streaming. ex: `--stream-port 8080`

### Options avancées

+ `-v`, `-vv` ou `--verbose`: Activer le mode débogage. ex: -v, `--verbose`, pour plus de debogage `-vv`: 
+ `--workers`: Nombre des threads pour l'extraction des urls ex: `--workers 20`
+ `--site`: Changer le site de recherche. ex: `--site sitename`
+ `--version`: Voir la version de spycis. ex: `--version`

> ¹ La position est imprimé au terminal dans les résultats de recherches avec les valeurs entre accolades carrés `[ ]`

> ² Les patterns sont des expressions regulières, `.` veut dire tout, alors que `mp4$` veut dire que doit se terminer par `mp4` pour plus d'info lire ici: [tutoriel regex](http://lumadis.be/regex/tuto_pcre.php)

## Tutoriel

Le tutoriel est divisé en parties:
 
1. Les recherches basiques par urls.
2. Les raccourcis de recherche par codes.
3. Les raccourcis de recherche par positions. (_idéal pour les films, ou les ambiguitées_)
4. Les bonus.
5. Les avancées.

### 1. Les recherches basiques par urls

##### Recherche de série ou film. Imprime: les positions dans `[...]`, les titres, les tags, et les `media urls`.

```bash
spycis "mentalist"
```

###### Exemple output:

```bash
[0] 'The Mentalist' ['film'] (http://www.tubeplus.me/player/558406/The_Mentalist/)
[1] 'The Mentalist' ['film'] (http://www.tubeplus.me/player/2086823/The_Mentalist/)
[2] 'The Mentalist' ['tv-show'] (http://www.tubeplus.me/player/1444106/The_Mentalist/)
```

##### Obtenir les `stream urls` pour une `media url`. Attention ça marche que pour les films. Pour les séries au moins un code episode doit être informé au format: _s01e01_

```bash
spycis http://www.tubeplus.me/player/553643/The_Lion_King/
```

###### Exemple output:

```bash
http://www.putlocker.com/embed/A17E6D66F6D1D44B
http://www.vidxden.com/embed-58jih9jyu06u.html
http://embed.nowvideo.sx/embed.php?v=d270847a4d88e
http://embed.nowvideo.sx/embed.php?v=84i2rp9p61v2f
http://www.vidxden.com/embed-0lp7jz069rfi.html
http://gorillavid.in/embed-zpkcdcd8e0hs-650x400.html
http://gorillavid.in/embed-arlo8rtqin7p-650x400.html
http://www.vidbux.com/embed-9p3igt5r8k36.html
```

##### Obtenir les `raw urls` pour une stream url

```bash
spycis http://www.divxstage.eu/video/46b593256e86d
```

###### Exemple output :

```bash
http://s63.coolcdn.ch/dl/88fbb33139e52637640a5b282347a730/52caa6ef/ff51f6acabefb1e855a45d2ab057ed55dd.flv
```

### 2. Les raccourcis de recherche par code

Les raccourcis de recherche par code sans l'option position va toujours prendre le première position dans les recherches

##### Obtenir les `stream urls` pour la position par defaul(`0`) dans la recherche avec le code épisode `s02e03` 

```bash
spycis -s s02e03 "Vampire Diaries"
```

###### Exemple output:
```bash
http://www.divxstage.eu/video/46b593256e86d
http://embed.nowvideo.sx/embed.php?v=3mlpxzgebdz0j
http://embed.nowvideo.sx/embed.php?v=a4nrypw7ybimh
http://putlocker.com/embed/0A0E80DF1AD75BB8
http://embed.nowvideo.sx/embed.php?v=09cc4321affc8
```

##### Obtenir les `raw urls` pour la position par defaul(`0`) dans la recherche avec le code épisode `s02e03`

```bash
spycis -r s02e03 "Vampire Diaries"
```

###### Exemple output:
```bash
http://50.7.161.75:182/d/z5sj6h3iljrwuxim4y6sl4qu6gqlucqvfdxuelpkzxvacn37sxj6oc74/video.mp4
http://s32.coolcdn.ch/dl/dd361f0f4d8e911f31cb8c7f569828a5/52ca4a40/ff9ffca598779e196b4e5190f74f554189.flv
http://s82.coolcdn.ch/dl/f46549bc003bd0e5d04e3159ca264c6b/52ca4a40/ffec6671b8c36f0348ae0ef4e119f49d64.flv
http://fs16ssd.vidbull.com:182/d/zrshafliljrwuxim4y6wv3qu44s5xp5gx3mw22s7pvn6yqks7fgo27sn/video.mp4
http://s82.coolcdn.ch/dl/1b7bf3370a866aedf3a401a84c22e014/52ca4a79/ffec6671b8c36f0348ae0ef4e119f49d64.flv
http://fs16ssd.vidbull.com:182/d/zrsc2utiljrwuxim4y6wv3qu47ibh67chhnpui3v25wplfsy522ks6oe/video.mp4
http://s33.coolcdn.ch/dl/813c3b2938dec203a3e6769fb4f5549f/52ca4c1f/ff9ffca598779e196b4e5190f74f554189.flv
```

### 3. Les racourcis de recherche par positions

##### Obtenir les `stream urls` pour la position de recherche `1` avec le code épisode `s01e16`.

```bash
spycis -p 1 -s s01e16 house
```

###### Exemple output:

```bash
http://www.putlocker.com/embed/4EB13DEA60C9EF28
http://gorillavid.in/embed-kdk7i5r1p5ye-650x400.html
http://www.sockshare.com/embed/0830C86867F3EE66
http://gorillavid.in/embed-iabh7e6bchgq-650x400.html
http://gorillavid.in/embed-30y7ahav048u-650x400.html
```

##### Obtenir les `raw urls` pour la position de recherche `1` avec le code épisode `s01e16`.

```bash
spycis -p 1 -r s01e16 house
```
###### Exemple output:

```bash
http://50.7.161.75:182/d/z5sj6h3iljrwuxim4y6sl4qu6gqlucqvfdxuelpkzxvacn37sxj6oc74/video.mp4
http://s32.coolcdn.ch/dl/dd361f0f4d8e911f31cb8c7f569828a5/52ca4a40/ff9ffca598779e196b4e5190f74f554189.flv
http://s82.coolcdn.ch/dl/f46549bc003bd0e5d04e3159ca264c6b/52ca4a40/ffec6671b8c36f0348ae0ef4e119f49d64.flv
```

##### Obtenir les `raw urls` pour la position de recherche `30`. Attention ça marche que pour les film, pour les le code épisode doit être informé avec l'option --raw-url. ex: `-p 30 -r s01e01`

```bash
spycis -p 30 "Lion King"
```

###### Exemple output:

```bash
http://s93.coolcdn.ch/dl/460eaf292dde58e88cc20dd85e3089b0/52ca4d78/ff8f8516069d4a60080318ff20932c4572.flv
http://s63.coolcdn.ch/dl/aee95feb62c17d6e52ba373b692e7bb8/52ca4bd3/ff7a1a561530c5f727d23577fcd250828e.flv
```

### 4. Les bonus

Les bonus ne retournent pas des urls, ils font des actions sur les `raw urls` trouvées. Les options des bonus sont toujours utilisées avec ses noms longs pour ne pas confondre avec les options basiques.

#### Option `--play`: Regarder une vidéo

###### Regarder "Le Roi Lion" avec pattern `flv` sur vlc

```bash
spycis --play flv -p 30 "The Lion King" 
```

###### Example output:
```bash
http://50.7.164.218:8182/46or2vr77su4tqukwyq3nbzwllazlxk4tcokrqmk6bg3q3nlbivff237mi/video.flv
http://50.7.164.218:8182/46or2vj77su4tqukwyq3nbzwlkn5arxroclhufzikh4jpmzwrld5psxz4u/video.flv
 * Playing url: http://50.7.164.218:8182/46or2vr77su4tqukwyq3nbzwllazlxk4tcokrqmk6bg3q3nlbivff237mi/video.flv
VLC media player 2.1.2 Rincewind (revision 2.1.2-0-ga4c4876)
[0x2273048] main libvlc: Running vlc with the default interface. Use 'cvlc' to use vlc without interface.
```

###### Regarder l’épisode 7 de saison 5 de "Vampire Diaries" que contient le pattern mp4 sur mplayer

```bash
spycis --play mp4 --player mplayer -r s05e07 "vampire diaries" 
```

#### Option `--download`: Télécharger une vidéo

###### Télecharge l'episode 7 de saison 5 de "Vampire Diaries" que contient le pattern mp4

```bash
spycis --download mp4 -r s05e07 "vampire diaries" 
```

#### Option `--stream`: Streaming d'une video

###### Faire streaming du film 'Roi Lion'

```bash
spycis --stream . -p 30 "lion king" 
```

###### Faire streaming de l'episode 7 de saison 5 de "Vampire Diaries"

```bash
spycis --stream . -r s05e07 "vampire diaries" 
```

###### Fait du streaming d'une `raw url`

```bash
spycis --stream . http://s63.coolcdn.ch/dl/59fd759b1e855a45d2ab057ed55dd.mp4
```

###### Fait du streaming d'une `stream url`

```bash
spycis --stream . http://embed.nowvideo.sx/embed.php?v=5fd0e2c91f94f
```

###### Exemple output:

```bash
http://s32.coolcdn.ch/dl/e4ed66cb4caee3a4d66a46e524d9c133/52cdcc05/ff9ffca598779e196b4e5190f74f554189.flv
Glissez les sous-titres pour 'the.vampire.diaries.s02e03.dvdrip.xvidreward' ici : 
 * Chosen file: http://s32.coolcdn.ch/dl/e4ed66cb4caee3a4d66a46e524d9c133/52cdcc05/ff9ffca598779e196b4e5190f74f554189.flv
 * Streaming from: 192.168.25.8:8080
VLC media player 2.1.2 Rincewind (revision 2.1.2-0-ga4c4876)
[0x10ab9a8] dummy interface: using the dummy interface module...
```

###### Utiliser pattern pour stream de la version francaise de under the dome s01e01 sur le site `loveserie`

```bash
spycis --site loveserie --stream FRENCH -r s01e01 "under the dome"
```

###### Exemple output:

```bash
# le pattern choisi le fichier que a le mot 'FRENCH'
http://fs2.youwatch.org:8777/ytv7tqhdekoax3ptx2bindnq66k2ymiojy67sa4je2zd7y3gi7nxelb2ai/video.mp4
http://fs15.youwatch.org:8777/exv75i7dh6oax3ptx25ynrp5uq77jyflkxa5n5qs3imzxtasd2mn4szdua/video.mp4
Glissez les sous-titres pour 'Download.Under.The.Dome.S01E01.FRENCH.BDRip.XviD.MiND.avi' ici :
```

#### Option `--subtitles`: Streaming d'une video avec sous-titres

###### Fait du streaming de l'episode 7 de saison 5 de "Vampire Diaries" avec sous-titres

```bash
spycis --stream . --subtitles vampire_soustitres.srt -r s05e07 "vampire diaries" 
```

###### Fait du streaming d'une raw url avec sous-titres

```bash
spycis --stream . --subtitles vampire_soustitres.srt http://s63.coolcdn.ch/dl/59fd759b1e855a45d2ab057ed55dd.mp4
```

###### Fait du streaming d'un fichier local avec sous-titres

```bash
spycis --stream . --subtitles messoustitres.srt /home/user/Videos/ma_video_local.mp4
```

#### Option `--stream-port`: Streaming d'une video sur une port specifié

###### Faire streaming du film 'Roi Lion' sur la porte `9000`. __note__: La porte par default c'est la 8080

```bash
spycis --stream . --stream-port 9000 -p 30 "lion king" 
```

###### Exemple output:

```
http://50.7.164.218:8182/46or2vj77su4tqukwyq3nbzwlkn5arxroclhufzikh4jpmzwrld7dspz4u/video.flv
http://50.7.164.218:8182/46or2vr77su4tqukwyq3nbzwllazlxk4tcokrqmk6bg3q3nlbivhj2d7mi/video.flv
Glissez les sous-titres pour 'zpkcdcd8e0hs.flv' ici : 
 * Chosen file: http://50.7.164.218:8182/46or2vj77su4tqukwyq3nbzwlkn5arxroclhufzikh4jpmzwrld7dspz4u/video.flv
 * Streaming from: 192.168.25.8:9000
VLC media player 2.1.2 Rincewind (revision 2.1.2-0-ga4c4876)
[0x937938] dummy interface: using the dummy interface module...
```

### 5. Avancée

###### Lister les sites disponibles

```bash
spycis --site-list all
```

###### Faire recherche sur un site alternatif

```bash
# Rechercher au avec le site "loveserie" les stream urls pour deadwood
spycis --site loveserie -s s01e08 deadwood
```

###### Exemple output:

```bash
# Sur le site loveserie, les urls se terminent par version, VO, VF ou VOST
http://youwatch.org/l0lqxt7w5t25
http://youwatch.org/cd49rhqmpbps
http://www.duckstreaming.com/lm0fhyxsrhxj
```

###### Voir la version de spycis installé

```bash
spycis --version
```

###### Exemple output:

```bash
Spycis v0.0.1
```

##### Executer spycis en mode verbose avec `-v` ou `--verbose`. Plus 

```bash
spycis -vv 'lion king'
```

##### Executer spycis en mode verbose avec information de debogage plus approfondie avec `-vv`

```bash
spycis -vv 'lion king'
```

##### Changer le nombre de threads utilisé par `3`

```bash
spycis --workers 3 'lion king'
```

## Architecture de spycis

Spycis fournit trois types de urls

+ __media urls__: L’adresse de la page sur le site ou spycis a trouvé le media(série/film/musique). Ces pages ont normalement l'information sur le media aussi comme plusieurs stream urls. exemple: `http://www.filmesonlinegratis.net/assistir-12-anos-de-escravidao-legendado-online.html`
+ __stream urls__: L’adresse de la page d'un site de streaming. Sur ces pages nous pouvons regarder les vidéos en ligne sans avoir besoin de télécharger la vidéo. les sites 'youtube', 'dailymotion', 'vimeo' sont des sites de streaming. example de stream url : `http://www.youtube.com/watch?v=VAJ8wZ97x94`
+ __raw urls__: L’adresse du vrai fichier, avec cette url nous pouvons télécharger la vidéo sur l'ordinateur. Ces liens sont normalement cachés du publique(pour faire les utilisateur régarder les videos sur leur stream urls). exemple de une raw url: `http://50.7.161.75:182/d/z5sj6h3iljrwuxim4y6sl4qu6gqlucqvfdxuelpkzxvacn37sxj6oc74/video.mp4` 


## Cadeau

Image bonus pour toi

![je taime](http://images2.fanpop.com/image/photos/13800000/Key-to-my-Heart-speter-13806362-1280-800.jpg)