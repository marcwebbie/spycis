Spycis
==========================

Spycis is a python console interface to stream websites


## Installation et MAJ

##### Installer

```python
pip install spycis
```

##### Mètre-à-jour

```python
pip install -U spycis
```

##### Désinstaller

```python
pip uninstall spycis
```

## Architecture de spycis

Spycis fournit trois types de urls

+ __media urls__: L’adresse de la page sur le site ou spycis a trouvé le media(série/film/musique)
+ __stream urls__: L’adresse de la page de streaming ou on peut regarder les vidéos en ligne.
+ __raw urls__: L’adresse du vrai fichier, avec cette url nous pouvons télécharger la vidéo sur l'ordinateur

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

+ `--workers`: Nombre des threads pour l'extraction des urls ex: `--workers 20`
+ `--verbose`: Activer le mode débogage. ex: `--verbose`
+ `--site`: Changer le site de recherche. ex: `--site sitename`

> ¹ La position est imprimé au terminal dans les résultats de recherches avec les valeurs entre accolades carrés `[ ]`



## Tutoriel

Le tutoriel est divisé en parties:
 
1. Les recherches basiques par urls
2. Les raccourcis de recherche par codes
3. Les raccourcis d'extractions par positions. (_idéal pour les films_)
3. Les bonus

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
spycis http://www.tubeplus.me/player/2086823/The_Mentalist/
```

###### Exemple output:

```bash
http://www.divxstage.eu/video/46b593256e86d
http://embed.nowvideo.sx/embed.php?v=3mlpxzgebdz0j
http://putlocker.com/embed/0A0E80DF1AD75BB8
http://embed.nowvideo.sx/embed.php?v=a4nrypw7ybimh
http://embed.nowvideo.sx/embed.php?v=09cc4321affc8
```

##### Obtenir les `raw urls` pour une stream url

```bash
spycis http://putlocker.com/embed/0A0E80DF1AD75BB8
```
###### Example output :
```bash
http://s62.coolcdn.ch/dl/1804cb30a73b505cc424800a4f819044/52c73947/ff51f6acabea45d2ab057ed55dd.flv
http://s63.coolcdn.ch/dl/59fb597996f8c5ba5fdc53d8/52c73795/ff51f6ad2ab057ed55dd.mp4
http://s63.coolcdn.ch/dl/59fd797996f8c5ba5fdc53d8/52c73795/ff51f65d2ab057ed55dd.mp4
```

### 2. Les raccourcis de recherche par code

Les raccourcis de recherche par code sans l'option position va toujours prendre le première position dans les recherches

##### Obtenir les `stream urls` pour la position `1` dans la recherche avec le code épisode 
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

##### Obtenir les `raw urls` pour la position `1` dans la recherche avec le code épisode `s02e03`
```bash
spycis -r s02e03 "Vampire Diaries"
```
###### Example output:
```bash
http://s62.coolcdn.ch/dl/1804cb30a73b505cc424800a4f819044/52c73947/ff51f6acabea45d2ab057ed55dd.flv
http://s63.coolcdn.ch/dl/59fb597996f8c5ba5fdc53d8/52c73795/ff51f6ad2ab057ed55dd.mp4
http://s63.coolcdn.ch/dl/59fd797996f8c5ba5fdc53d8/52c73795/ff51f65d2ab057ed55dd.mp4
```


##### Obtenir les `raw urls` pour la position de recherche `9` avec un code de `s03e07`.
```bash
spycis -p 9 -r s03e07 "Vampire Diaries"
```
###### Example output:

```bash
http://s62.coolcdn.ch/dl/1804800819044/52c73947/ff51f6acabefb1e855a45d2ab057ed55dd.flv
http://s63.coolcdn.ch/dl/330269fd69b0d0e/52c73933/ff51f6acabefb1e855a45d2a57ed55dd.flv
http://s63.coolcdn.ch/dl/59fd7597996f8c5ba5fdc53d8/52c73795/ff51f6acabefb1e855a45d2ab057ed55dd.mp4
http://s63.coolcdn.ch/dl/55a8b597996f8c5ba5fdc53d8/52c73795/ff51f6acabefb1e855a45d2ab057ed55dd.mp4
```


### 3. Les racourcis d'extractions par positions

##### Obtenir les `raw urls` pour la position de recherche `30`. Attention ça marche que pour les film, pour les series au moins un code episode doit être informé au format:`-p 30 -r s01e01`
```bash
spycis -p 30 "Lion King"
```
###### Example output:

```bash
http://s62.coolcdn.ch/dl/1804800819044/52c73947/ff51f6acabefb1e855a45d2ab057ed55dd.flv
http://s63.coolcdn.ch/dl/330269fd69b0d0e/52c73933/ff51f6acabefb1e855a45d2a57ed55dd.flv
http://s63.coolcdn.ch/dl/59fd7597996f8c5ba5fdc53d8/52c73795/ff51f6acabefb1e855a45d2ab057ed55dd.mp4
http://s63.coolcdn.ch/dl/55a8b597996f8c5ba5fdc53d8/52c73795/ff51f6acabefb1e855a45d2ab057ed55dd.mp4
```

### 4. Les bonus

Les bonus ne retournent pas des urls, ils font des actions sur les urls trouvées. les options des bonus sont toujours utilisées avec ses noms longs pour ne pas confondre avec les options basiques

#### Regarder une vidéo extrait

###### Regarder la vidéo en format mp4 sur vlc
```bash
spycis --play mp4 -p 2 "The Lion King" 
```

###### Regarder l’épisode 7 de saison 5 de "Vampire Diaries" en format mp4 sur mplayer
```bash
spycis --play mp4 --player mplayer -r s05e07 "vampire diaries" 
```

#### Télécharger une video extrait

###### Télecharge l'episode 7 de saison 5 de "Vampire Diaries" en format mp4
```bash
spycis --download mp4 -r s05e07 "vampire diaries" 
```

#### Streaming d'une video extrait

###### Fait du streaming de 'Roi Lion' sur la porte http 8080
```bash
spycis --stream 8080 -p 30 "lion king" 
```

###### Fait du streaming de l'episode 7 de saison 5 de "Vampire Diaries" sur la porte http 8080
```bash
spycis --stream 8080 -r s05e07 "vampire diaries" 
```
###### Fait du streaming de l'episode 7 de saison 5 de "Vampire Diaries" sur la porte http 8080 avec sous-titres
```bash
spycis --stream 8080 --subtitles vampire_soustitres.srt -r s05e07 "vampire diaries" 
```


## Cadeau


![je taime](http://images2.fanpop.com/image/photos/13800000/Key-to-my-Heart-speter-13806362-1280-800.jpg)