import requests
from bs4 import BeautifulSoup
import os
import shutil
import unicodedata
import sys

def ListPages(url):

    main_url=url_manga+str(url)
    #print (main_url)

    req=requests.get(url)

    statusCode=req.status_code
    if statusCode==200:
        #Pasar el contenido HTML de la web a un objeto BeautifulSoup()
        soup=BeautifulSoup(req.text, "html.parser")

        #lista url paginas
        paginas=soup.find('div',{'id':'selectpage'})
        options = paginas.find_all('option')
        urls_pages=list(map(lambda option: url_manga+option['value'],options))

        return list(map(ListImg,urls_pages))

    else:
        #print ("Status Code %d en %s" %(statusCode,name))
        print('Error %d Lista Paginas' % (statusCode))
        return None

def ListImg(url):
    req=requests.get(url)

    statusCode=req.status_code
    if statusCode==200:
        soup=BeautifulSoup(req.text, "html.parser")

        img_url=soup.find('div',{'id':'imgholder'}).find('img')
        return img_url['src']


    else:
        #print ("Status Code %d en %s" %(statusCode,name))
        print ('Error %d con la url de la imagen' %(statusCode))
        return None


def CreateFolder(name,dir="./mangas",format='%3d'):
    if type(name) is int:
        #print ('%04d' % (name))
        path=os.path.join(dir,format % (name))
    else: path = os.path.join(dir,name)

    try:
        os.rmdir(path)
    except OSError as error:
        pass
    try:
        os.mkdir(path)
    except OSError as error:
        print(error)


    
def DownloadImage(url,name):
    # Open the url image, set stream to True, this will return the stream content
    resp=requests.get(url, stream=True)

    local_file=open(name,'wb')

    # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
    resp.raw.decode_content = True
        
    # Copy the response stream raw data to local image file.
    shutil.copyfileobj(resp.raw, local_file)
        
    # Remove the image url response object.
    del resp


def ListaCapitulos(url):
    #Lista capitulos
    list_capitulos=[]

    #Peticion a la web
    req = requests.get(url)

    #Comprobacion de que la peticion devuelve un Status Code = 200 (exito)
    # Si empieza por 4 o 5 significa que ha habido un error
    statusCode=req.status_code
    if statusCode==200:
        #Pasar el contenido HTML de la web a un objeto BeautifulSoup()
        soup=BeautifulSoup(req.text, "html.parser")

        #Obtener lista de capitulos
        tabla=soup.find('table',{'id':'listing'})
        capitulos=tabla.find_all('tr')

        #Eliminar table_head (no capitulo) de la lista
        del capitulos[0]

        #Recorrer todas las entradas para extraer el titulo
        for i,capitulo in enumerate(capitulos,1):
            #Con el métdo "getText()" devuelve el HTML
            href=capitulo.find('a', href=True)
            url_capitulo=url_manga+str(href['href'])

            list_capitulos.append(url_capitulo)

        return list_capitulos
            
    else:
        #print ("Status Code %d" % statusCode)
        print ('Error al buscar el manga')
        return list_capitulos

def Descargar_capitulos_rango(capitulos,n,format):
    print ('Preparando descarga... Espere')

    #Recorrer todas las entradas para extraer el titulo
    for i,capitulo in enumerate(capitulos,n):

        #Crear carpeta del capitulo
        CreateFolder(i,'./mangas/'+name_manga_folder,format)

        #Lista de las urls de las imagenes de cada capitulo
        urls_capitulos=ListPages(capitulo)
        format_img= '%03d' if len(urls_capitulos)>99 else '%02d'

        for j,url_capitulo in enumerate(urls_capitulos,1):
            
            dir='./mangas/'+name_manga_folder+'/'+format % (i)+'/'+format_img % (j)

            #print (dir)
            #print (url_capitulo)
            DownloadImage(url_capitulo,dir)
            
        print('\tCapitulo %d descargado'%(i))


#------------------------------------------
#-------Main Web Scrapping-----------------
#------------------------------------------

#anime='OnePiece'
url_manga = 'http://www.mangareader.net'
#url=url_manga+'/one-piece'


#Bienvenida
print ('Bienvenido a Web Scrapping \nEste programa descarga mangas de la página MangaReader')

#Bucle por si se introduce mal el nombre del manga
len_manga=0
counter=False
while len_manga is 0:

    #Opción cerrar programa
    if counter is True:
        
        finish=input ('¿Finalizar Programa? (S/N): ')

        finish=finish.lower()
        if finish =='s':
            sys.exit()

    counter=True
            
    #print ('\n Indica el manga que desea descargar')
    name_manga= input('\nIndica el manga:')

    #Editar entrada manga
    name_manga= name_manga.lower()  #Minusculas
    name_manga=name_manga.strip()   #Eliminar espacios en blanco del princio y final

    name_manga_folder=name_manga.title()
    name_manga_folder="_".join(name_manga_folder.split())

    name_manga="-".join(name_manga.split()) #Sustituir varios espacios en blanco por uno solo

    # print('Ha seleccionado:' + str(name_manga))

    #Calcular lista de capitulos
    lista_caps=ListaCapitulos(url_manga+'/'+name_manga)
    len_manga=len(lista_caps)

#Formato nombre de la carpeta de los capitulos
#format_caps='%02d' if len_manga<100 else format_caps='%03d' if len_manga<1000 else fromat='%04d' 

if len_manga<100:
    format_caps='%02d'
elif len_manga<1000:
    format_caps='%03d'
else: fromat='%04d'


#Comprobación de si existe la carpeta mangas
if not os.path.isdir('./mangas'):
    CreateFolder('mangas','./')
    print ('Carpeta mangas creada')

#Crear carpeta del manga seleccionado
if not os.path.isdir('./mangas/'+name_manga_folder):
    CreateFolder(name_manga_folder)
    print('Carpeta %s creada'%(name_manga_folder))

opcion=None

#Seleccionar capitulos a descargar
print ('\nHay %d capitulos en total' % (len_manga))
print ('Indica una de las siguientes opciones de descarga:\n A: Todos\n B: Primero\n C: Ultimo\n D: Rango\n E: Elegir capitulo\n')

counter2=False
while opcion is None:
    if counter2 is True:
        print('Volver a intentar')

    opcion=input('Opcion: ')

    opcion=opcion.lower()
    #print (opcion)

    #Descargar capitulos
    if opcion=='a' or opcion=='1':
        Descargar_capitulos_rango(lista_caps,1,format_caps)
    elif  opcion=='b' or opcion=='2':
        Descargar_capitulos_rango([lista_caps[0]],1,format_caps)
    elif opcion=='c'or opcion=='3':
        Descargar_capitulos_rango([lista_caps[len_manga-1]],len_manga,format_caps)
    elif opcion=='d'or opcion=='4':
        print ('Descargar:')
        inicio=input(' Del capitulo (numero): ')
        fin=input(' Al capitulo (numero): ')
        Descargar_capitulos_rango(lista_caps[int(inicio)-1:int(fin)],int(inicio),format_caps)
    elif opcion=='e'or opcion=='5':
        eleccion=input('Capitulo a descargar (numero): ')
        Descargar_capitulos_rango([lista_caps[int(eleccion)-1]],int(eleccion),format_caps)
    else: 
        opcion=None
        counter2=True