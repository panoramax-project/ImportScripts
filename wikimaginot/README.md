# WikiMaginot

Ce dépôt porte sur l'import de photos et de métadonnées de https://wikimaginot.eu vers les instances IGN et OSM de panoramax.

## Fichier cvs exporté de wikimaginot.eu

Le fichier csv comprend 10 colonnes :
```
Num_photo;Lat;Lon;Titre;Sujet;Auteur;Licence;Date_photo;Url_photo;Url_site
10828;49.021719;7.252502;"R602 (Chambre de coupure) ";;"wikimaginot - Christatus";CC-BY;;https://files-wikimaginot.eu/_documents/2011/_wiki_photos_redim/30-1321810396.JPG;https://wikimaginot.eu/V70_construction_detail.php?id=11631
10827;49.021719;7.252502;"R602 (Chambre de coupure) ";;"wikimaginot - Christatus";CC-BY;05/04/2009;https://files-wikimaginot.eu/_documents/2021-06/_wiki_photos_redim/63-1623253016.jpg;https://wikimaginot.eu/V70_construction_detail.php?id=11631
11091;49.054370;7.353364;"B - (Chambre de coupure)";;"wikimaginot - Christatus";CC-BY;18/02/2011;https://files-wikimaginot.eu/_documents/2021-07/_wiki_photos_redim/63-1626528361.jpg;https://wikimaginot.eu/V70_construction_detail.php?id=11902
11090;49.054370;7.353364;"B - (Chambre de coupure)";;"wikimaginot - Christatus";CC-BY;18/02/2011;https://files-wikimaginot.eu/_documents/2021-07/_wiki_photos_redim/63-1626528390.jpg;https://wikimaginot.eu/V70_construction_detail.php?id=11902
29796;50.371584;3.601278;"B461 - RESERVOIR D'ONNAING - (Blockhaus pour canon)";;"wikimaginot - Google Streetview";CC-O;02/04/2015;https://files-wikimaginot.eu/_documents/2021-10/_wiki_photos_redim/63-1633348951.jpg;https://wikimaginot.eu/V70_construction_detail.php?id=18934
```

## Import des photos dans panoramax

Les photos ayant pour licence "Domaine public" et CC-O seront importées dans l'instance IGN.

Celles de licence CC-BY et CC-BY-SA seront importées dans l'instance OSM.

_Volumétrie :_

CC-BY          : 7074 photos

CC-BY-SA       : 6286 photos

CC-O           : 1786 photos

Domaine public : 1319 photos


## Arborescence

Les photos seront regroupées par séquence **"instance/id de Url_site"** comme ceci :
```
/racine/OSM/11631/30-1321810396.JPG
/racine/OSM/11631/63-1623253016.jpg
/racine/OSM/11902/63-1626528361.jpg
/racine/OSM/11902/63-1626528390.jpg
/racine/IGN/18934/63-1633348951.jpg
```


Dans chaque sous-dossier "id", en plus des photos, on aura 2 fichiers supplémentaires :

- **titre.txt** : contient le champ "Titre" : "R602 (Chambre de coupure)"

- **_geovisio.csv** : un mini fichier cvs compatible avec la CLI ([format attendu](https://gitlab.com/geovisio/cli/-/blob/main/README.md?ref_type=heads#external-metadata)) qui contiendra les champs suivants :

```
file;lat;lon;capture_time;Exif.Image.Artist;Xmp.xmp.BaseURL
30-1321810396.JPG;49.021719;7.252502;"2011-01-01T00:00:00";"Christatus";https://wikimaginot.eu/V70_construction_detail.php?id=11631
63-1623253016.jpg;49.021719;7.252502;"2009-04-05T00:00:00";"Christatus";https://wikimaginot.eu/V70_construction_detail.php?id=11631
```

NB: pour Date_photo, si vide alors prendre la date dans le nom du dossier parent de Url_photo; compléter un mois vide avec "01", un jour vide avec "01", et le time avec "T00:00:00".

NB: pour Exif.Image.Artist, on enlève les lettres "wikimaginot - " qui précèdent chaque champ "Auteur".
