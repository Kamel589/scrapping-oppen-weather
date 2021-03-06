from IPython.core.display import HTML
import csv
from termcolor import colored, cprint
import time
import urllib.request
import pandas as pd
import json 

#Récupération des données de http://openweathermap.org/ à l'aide du User key
def url_builder(city_id,city_name,country):
    user_api = '5974b0c12e0fc15309884061f3af3402'  
    unit = 'metric'  
    if(city_name!=""):
        api = 'http://api.openweathermap.org/data/2.5/weather?q=' 
        full_api_url = api + str(city_name) +','+ str(country)+ '&mode=json&units=' + unit + '&APPID=' + user_api
    else:
        api = 'http://api.openweathermap.org/data/2.5/weather?id='     
        full_api_url = api + str(city_id) + '&mode=json&units=' + unit + '&APPID=' + user_api
    return full_api_url


def data_fetch(full_api_url):
    url = urllib.request.urlopen(full_api_url)
    output = url.read().decode('utf-8')
    raw_api_dict = json.loads(output)
    url.close()
    return raw_api_dict


# Organisation des données
def data_organizer(raw_api_dict):
    data = dict(
        city=raw_api_dict.get('name'),
        country=raw_api_dict.get('sys').get('country'),
        temp_max=raw_api_dict.get('main').get('temp_max'),
        temp_min=raw_api_dict.get('main').get('temp_min'),
    )
    return data

# Affichage
def data_output(data):
    print('---------------------------------------')
    print('')
    print('Température à : {}, {}:'.format(data['city'], data['country']))
    print('Max: {}, Min: {}'.format(data['temp_max'], data['temp_min']))
    print('')
    print('---------------------------------------')
    print('')
     
# Enregistrement dans un fichier csv 
def WriteCSV(data):
    with open('weatherOpenMap.csv', 'w') as f:  
        w = csv.DictWriter(f, data.keys())
        w.writeheader()
        w.writerow(data)
        
       
def  ReadCSV():
    try:
    #ouverture de fichier en mode lecture en specifiant le encodage
        with open("weatherOpenMap.csv",'r') as Fichier:
        #lecture – utilisation du parseur csv en specifiant délimiteur
            csv_contenu = csv.reader(Fichier,delimiter=",") 
            reader = csv.DictReader(Fichier)
            dic={}
            for row in reader:
                print (row['city'])
                dic.update(row)
            #fermeture du fichier avec la méthode close()
            Fichier.close()
            return dic
    except IOError:
        print("Fichier n'est pas trouvé")
        

# Charger le fichier json

def getVilles():
    with open('city.list.json') as f:
        d = json.load(f)
        villes=pd.DataFrame(d)
        return villes
    
villes = getVilles()
v = villes[villes["country"]=='FR']['id']

if __name__ == '__main__':
    try:
        city_name=''
        country='FR'
        compteur = 0
        call = 0
        for idv in v :
            if call == 60:
                print ('Attendre une minute')
                time.sleep(60)
                call = 0
            else :
                city_id= idv 
                                    #Generation de l url
                print(colored('Generation de l url ', 'red',attrs=['bold']))
                url=url_builder(city_id,city_name,country)
                                    #Invocation du API afin de recuperer les données
                print(colored('Invocation du API afin de recuperer les données', 'red',attrs=['bold']))
                data=data_fetch(url)
                                    #Formatage des données
                print(colored('Formatage des donnée', 'red',attrs=['bold']))
                data_orgnized=data_organizer(data)
                                    #Affichage de données
                print(colored('Affichage de données ', 'red',attrs=['bold']))
                data_output(data_orgnized)
                print(colored('Enregistrement des données à dans un fichier CSV ', 'green',attrs=['bold']))
                WriteCSV(data_orgnized)  
                print(colored('Lecture des données à partir un fichier CSV ', 'green',attrs=['bold']))
                               #Lecture des données a partir de fichier CSV 
                data=ReadCSV()
                print(colored('Affichage des données lues de CSV ', 'green',attrs=['bold']))
                               #Affichage des données 
                data_output(data)
                compteur += 1
                call = call + 1
           
           
        
    except IOError:
        print('no internet')
            
print('Le nombre de villes parcourues est de : '+ str(compteur))
        



