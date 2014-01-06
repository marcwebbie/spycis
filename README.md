Spycis
==========================

Spycis is a python console interface to stream websites


## Installation et MAJ

##### Installer

```python
pip install spycis.zip
```

##### Mètre-à-jour

```python
pip install -U spycis.zip
```

##### Désinstaller

```python
pip uninstall spycis
```

## Architecture de spycis

Spycis fournit trois types de urls

+ __media urls__: L’adresse de la page sur le site ou spycis a trouvé le media(série/film/musique). Ces pages ont normalement l'information sur le media aussi comme plusieurs stream urls. exemple: `http://www.filmesonlinegratis.net/assistir-12-anos-de-escravidao-legendado-online.html`
+ __stream urls__: L’adresse de la page de streaming ou on peut regarder les vidéos en ligne. les sites(youtube, dailymotion...) de streaming sont les sites où on regarde les videos. exemple: `http://www.youtube.com/watch?v=VAJ8wZ97x94`
+ __raw urls__: L’adresse du vrai fichier, avec cette url nous pouvons télécharger la vidéo sur l'ordinateur, avec ce lien on peut telecharger la video sur l'ordinateur. exemple: `http://www.podtrac.com/pts/redirect.mp4/201312.jb-dl.cdn.scaleengine.net/las/2013/linuxactionshowep293-432p.mp4` 

### Options de spycis basiques

les options de Spycis sont activé par des "switches" de terminal au formats: `-s value` ou longue `--switch value`

+ `-r` ou `--raw-urls`: Retourne les raw urls pour le code ou specifié. ex: `-r s02e31` ou `--raw-urls  s02e31`
+ `-s` ou `--stream-urls`: Retourne les stream urls pour le code specifié. ex: `-s s02e31` ou `--stream-urls  s02e31`
+ `-p` ou `--position`: Options utilisé avec `-r` ou `-s` pour specifié la positon¹. ex: `-p 2 -r s02e31`

### Options bonus

+ `--play`: Executer le premier fichier au format spécifié dans les `raw urls` extraites. ex: `--play mp4`
+ `--player`: Choisir le player pour l'option play ex: `--player amarok`
+ `--download`: Télécharge le premier fichier en format dans les `raw urls` extraites. ex: `--download mp4`
+ `--subtitles`: Ouvre streaming pour les sous-titres ex: `--subtitles mes_sous_titres.srt`
+ `--stream`: Ouvre streaming sur la porte spécifié. ex: `--stream 8080`

### Options avancées

+ `-v`, `-vv` ou `--verbose`: Activer le mode débogage. ex: `--verbose`, pour plus de debogage `-vv`: 
+ `--workers`: Nombre des threads pour l'extraction des urls ex: `--workers 20`
+ `--site`: Changer le site de recherche. ex: `--site sitename`
+ `--version`: Voir la version de spycis. ex: `--version`

> ¹ La position est imprimé au terminal dans les résultats de recherches avec les valeurs entre accolades carrés `[ ]`


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
spycis http://www.putlocker.com/embed/A17E6D66F6D1D44B
```
###### Example output :
```bash
http://s62.coolcdn.ch/dl/1804cb30a73b505cc424800a4f819044/52c73947/ff51f6acabea45d2ab057ed55dd.flv
http://s63.coolcdn.ch/dl/59fb597996f8c5ba5fdc53d8/52c73795/ff51f6ad2ab057ed55dd.mp4
http://s63.coolcdn.ch/dl/59fd797996f8c5ba5fdc53d8/52c73795/ff51f65d2ab057ed55dd.mp4
```

### 2. Les raccourcis de recherche par code

Les raccourcis de recherche par code sans l'option position va toujours prendre le première position dans les recherches

##### Obtenir les `stream urls` pour la position par defaul(`0`) dans la recherche avec le code épisode 
```bash
spycis -s s02e03 "Vampire Diaries"
```
###### Example output:
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
###### Example output:
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

##### Obtenir les `stream urls` pour la position de recherche `2` avec un code de `s01e01`.
```bash
spycis -p 2 -s s01e01 dead
```
###### Example output:

```bash
http://www.putlocker.com/embed/064AB1FB4E109807
http://www.putlocker.com/embed/CBE069654BC5EA7E
http://www.sockshare.com/embed/54191E3B7033E7D2
```

##### Obtenir les `raw urls` pour la position de recherche `2` avec un code de `s01e01`.
```bash
spycis -p 2 -r s01e01 dead
```
###### Example output:

```bash
http://50.7.161.75:182/d/z5sj6h3iljrwuxim4y6sl4qu6gqlucqvfdxuelpkzxvacn37sxj6oc74/video.mp4
http://s32.coolcdn.ch/dl/dd361f0f4d8e911f31cb8c7f569828a5/52ca4a40/ff9ffca598779e196b4e5190f74f554189.flv
http://s82.coolcdn.ch/dl/f46549bc003bd0e5d04e3159ca264c6b/52ca4a40/ffec6671b8c36f0348ae0ef4e119f49d64.flv
```

##### Obtenir les `raw urls` pour la position de recherche `30`. Attention ça marche que pour les film, pour les series au moins un code episode doit être informé au format:`-p 30 -r s01e01`
```bash
spycis -p 30 "Lion King"
```
###### Example output:

```bash
http://s93.coolcdn.ch/dl/460eaf292dde58e88cc20dd85e3089b0/52ca4d78/ff8f8516069d4a60080318ff20932c4572.flv
http://s63.coolcdn.ch/dl/aee95feb62c17d6e52ba373b692e7bb8/52ca4bd3/ff7a1a561530c5f727d23577fcd250828e.flv
```

### 4. Les bonus

Les bonus ne retournent pas des urls, ils font des actions sur les urls trouvées. les options des bonus sont toujours utilisées avec ses noms longs pour ne pas confondre avec les options basiques

#### Regarder une vidéo extrait

###### Regarder la vidéo en format mp4 sur vlc
```bash
spycis --play mp4 -p 30 "The Lion King" 
```

###### Regarder l’épisode 7 de saison 5 de "Vampire Diaries" en format mp4 sur mplayer
```bash
spycis --play mp4 --player mplayer -r s05e07 "vampire diaries" 
```

#### Télécharger une vidéo

###### Télecharge l'episode 7 de saison 5 de "Vampire Diaries" en format mp4
```bash
spycis --download mp4 -r s05e07 "vampire diaries" 
```

#### Streaming d'une video

###### Faire streaming du film 'Roi Lion' sur la porte http 8080
```bash
spycis --stream 8080 -p 30 "lion king" 
```

###### Faire streaming de l'episode 7 de saison 5 de "Vampire Diaries" sur la porte http 8080
```bash
spycis --stream 8080 -r s05e07 "vampire diaries" 
```

###### Fait du streaming de l'episode 7 de saison 5 de "Vampire Diaries" sur la porte http 8080 avec sous-titres
```bash
spycis --stream 8080 --subtitles vampire_soustitres.srt -r s05e07 "vampire diaries" 
```

###### Fait du streaming d'une `raw url` sur la porte http 8080
```bash
spycis --stream 8080 http://s63.coolcdn.ch/dl/59fd759b1e855a45d2ab057ed55dd.mp4
```

###### Fait du streaming d'une raw url sur la porte http 8080 avec sous-titres
```bash
spycis --stream 8080 --subtitles vampire_soustitres.srt http://s63.coolcdn.ch/dl/59fd759b1e855a45d2ab057ed55dd.mp4
```

###### Fait du streaming d'un fichier local sur la porte http 8080 avec sous-titres
```bash
spycis --stream 8080 --subtitles messoustitres.srt /home/user/Videos/ma_video_local.mp4
```

### 5. Avancée

##### Obtenir version de spycis installée

```bash
spycis --version
```

###### Example output:


##### Executer spycis en mode verbose avec `-v` ou `--verbose`

```bash
spycis --verbose 'lion king'

# Pour avoir plus d'information de debogage
spycis --vv 'lion king'
```

##### Changer le nombre de threads utilisé par `3`

```bash
spycis --workers 3 'lion king'
```

```bash
Spycis v0.0.1

License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>.
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.
```

### Cadeau

Image bonus pour toi

![je taime](http://images2.fanpop.com/image/photos/13800000/Key-to-my-Heart-speter-13806362-1280-800.jpg)