import argparse
import csv
import glob
import os
import requests
from pathlib import Path

def gestion_date(date:str, chemin:str) -> str:
    s_time = "T00:00:00"
    ret = "1900-01-01" + s_time
    if date == "":
        if chemin.find('/'):
            dossier_date = chemin.split('/')[-3]
            if dossier_date.startswith('20') and len(dossier_date) == 4:
                ret = dossier_date + "-01-01" + s_time
            elif dossier_date.startswith('20') and len(dossier_date) == 7:
                ret = dossier_date + "-01" + s_time
            elif dossier_date.startswith('20') and len(dossier_date) == 10:
                ret = dossier_date + s_time
    elif date.find('/'):
        ret = date.split('/')[2] + "-" + date.split('/')[1] + "-" + date.split('/')[0] + s_time

    return ret

##### dossiers ######
s_stockage = "files"
s_dossier_ign = "IGN"
s_dossier_osm = "OSM"
#####################

if __name__ == "__main__":
    # on commence par récupérer les arguments :
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", help="Indique le fichier d'import des photos de wikimaginot.eu (obligatoire)", type=str, required=True)
    args = parser.parse_args()

    s_root = os.getcwd () + "/"
    print(f"dossier courant  : {s_root}")
    s_local_files = s_root + s_stockage + "/"

    s_fichier_csv = s_root + args.file
    print(f"fichier d'import : {s_fichier_csv}")
    print(f"dossier d'import : {s_local_files}")
    print()

    with open(s_fichier_csv, newline='') as csvfile:
        o_reader = csv.DictReader(csvfile, delimiter=';', quotechar='"')

        for row in o_reader:
            # Num_photo;Lat;Lon;Titre;Sujet;Auteur;Licence;Date_photo;Url_photo;Url_site
            # 93407;48.932294;7.951462;"HOFFEN - (Abri)";;"wikimaginot - Gregory Fuchs";CC-BY-SA;07/06/2019;https://files-wikimaginot.eu/_documents/2021-03/_wiki_photos_redim/63-1616490496.jpg;https://wikimaginot.eu/V70_construction_detail.php?id=10961
            #print("-")

            # num photo
            s_num = row['Num_photo']
            # vérif licence
            if row['Licence'] not in ['Domaine public','CC-O','CC-BY','CC-BY-SA']:
                print(f"erreur, Licence vide pour photo {s_num} !")
                continue
            if row['Licence'] in ['Domaine public','CC-O']:
                s_dossier = s_dossier_ign
            else:
                s_dossier = s_dossier_osm
            # vérif id
            s_id_seq = ""
            if "?id=" in row['Url_site']:
                s_id_seq = row['Url_site'][row['Url_site'].find("?id=")+4:]
            if s_id_seq == "":
                print(f"erreur, id vide pour photo {s_num} !")
                continue
            # vérif lat,lon,titre,url_photo
            if row['Lat'] == "":
                print(f"erreur, Lat vide pour photo {s_num} !")
                continue
            if row['Lon'] == "":
                print(f"erreur, Lon vide pour photo {s_num} !")
                continue
            if row['Titre'] == "":
                print(f"erreur, Titre vide pour photo {s_num} !")
                continue
            if row['Url_photo'] == "":
                print(f"erreur, Url_photo vide pour photo {s_num} !")
                continue
            s_url = row['Url_photo']
            s_name_photo = ""
            if s_url.find('/'):
                s_name_photo = s_url.split('/')[-1]
            if s_name_photo == "":
                print(f"erreur, nom de photo vide pour photo {s_num} !")
                continue
            # auteur
            s_auteur = ""
            if len(row['Auteur']) > 14:
                s_auteur = row['Auteur'][14:]
            else:
                s_auteur = row['Auteur']
            # vérif date
            s_raw_date = row['Date_photo']
            s_date = gestion_date(s_raw_date, s_url)

            # photo
            s_local_dossier = s_local_files + s_dossier + "/" + s_id_seq + "/"
            p_local_photo = Path(s_local_dossier)
            if not p_local_photo.exists():
                p_local_photo.mkdir(parents = True)
            s_local_photo = s_local_dossier + s_name_photo

            # récapitulatif :
            #print(f"{row['Licence']}, {s_dossier}, {s_id_seq}, {s_name_photo}, {s_local_photo}")
            #print(f"titre : {row['Titre']}")
            ## file;lat;lon;capture_time;Exif.Image.Artist;Xmp.xmp.BaseURL
            print(f"{s_dossier} {s_id_seq} : csv : {s_name_photo}, {row['Lat']}, {row['Lon']}, {s_date}, {s_auteur}, {row['Url_site']}")

            # téléchargement de la photo
            if not Path(s_local_photo).exists():
                print(f"download {s_url} ...")
                headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'}
                with requests.get(url=s_url, headers=headers, verify=True, allow_redirects=True, stream=True) as request:
                    if request.status_code == 200:
                        # On ouvre le fichier de sortie
                        with open(s_local_photo, 'wb') as file:
                            # On écrit le contenu dedans
                            file.write(request.content)
                    else:
                        print(f"erreur http pour {s_dossier} {s_id_seq}, code retour = {request.status_code}")
                        continue
            else:
                print(f"photo présente {s_local_photo}")
                continue

            # écriture du titre.txt
            s_fichier_titre = s_local_dossier + 'titre.txt'
            if not Path(s_fichier_titre).exists():
                with open(s_fichier_titre, 'w', encoding='utf-8') as titre_file:
                    titre_file.write(row['Titre'])
                    #print(f"écriture terminée pour {s_fichier_titre}")

            # écriture du _geovisio.csv
            b_write_first_ligne = True
            if Path(s_local_dossier + '_geovisio.csv').exists():
                b_write_first_ligne = False
            with open(s_local_dossier + '_geovisio.csv', 'a', newline='') as csvfile:
                o_writer = csv.writer(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                if b_write_first_ligne:
                    o_writer.writerow(["file","lat","lon","capture_time","Exif.Image.Artist","Xmp.xmp.BaseURL"])
                o_writer.writerow([s_name_photo, row['Lat'], row['Lon'], s_date, s_auteur, row['Url_site']])


    # on va parcourir les dossiers pour envoyer les séquences à la CLI
    liste_id_seq = []
    for instance in (s_dossier_ign, s_dossier_osm):
        liste_id_seq.extend(glob.glob(os.path.join(s_local_files, f"{instance}/*")))
    if len(liste_id_seq) > 0:
        liste_id_seq.sort()
        for i_id in liste_id_seq:
            print(f" geovisio upload --api-url http://localhost:5000/ {i_id }")
