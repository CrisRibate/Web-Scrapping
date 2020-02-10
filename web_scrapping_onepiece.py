import requests
from bs4 import BeautifulSoup
import os
import shutil

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

        '''
        #Pasar una lambda es como declarar una funcion como esta
        def fun(option):
            return url_manga+option['value']
        #y pasarla como parametro
        urls_pages=list(map(fun,options))
        '''
        return list(map(ListImg,urls_pages))

        '''
        max_page=paginas.split('of ')[1]
        print (max_page)

        #Lista url de cada pagina
        urls_img=[]
        i=1
        while i<int(max_page):
            url_img= str(main_url)+'/'+str(i)
            if i==1:
                url_img= str(main_url)
            urls_img.append(url_img)
            print (url_img)
            i+=1
        print (len(urls_img))
        

        #Ubicacion imagen
        ub_image=soup.find('id', {'imgholder'})
        '''
    else:
        print ("Status Code %d en %s" %(status_code,name))
        return None

def ListImg(url):
    req=requests.get(url)

    statusCode=req.status_code
    if statusCode==200:
        soup=BeautifulSoup(req.text, "html.parser")

        img_url=soup.find('div',{'id':'imgholder'}).find('img')
        #print (img_url['src'])
        return img_url['src']


    else:
        print ("Status Code %d en %s" %(status_code,name))
        return None


def CreateFolder(name,dir="./mangas"):
    if type(name) is int:
        #print ('%04d' % (name))
        path=os.path.join(dir,'%04d' % (name))
    else: path = os.path.join(dir,name)

    #directory = name
    #parent_dir= "./mangas"
    #path = os.path.join(dir,directory)
    try:
        os.rmdir(path)
    except OSError as error:
        pass
    try:
        os.mkdir(path)
    except OSError as error:
        print(error)
        #dir_error=dir+'/'+name
        #shutil.rmtree(dir_error, ignore_errors=True)
        #CreateFolder(name,dir)

    
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

anime='OnePiece'
url_manga = 'http://www.mangareader.net'
url=url_manga+'/one-piece'

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

    #Crear carpeta OnePiece
    CreateFolder(anime)

    #Recorrer todas las entradas para extraer el titulo
    for i,capitulo in enumerate(capitulos[0:5],1):
        #Con el métdo "getText()" devuelve el HTML
        href=capitulo.find('a', href=True)
        url_capitulo=url_manga+str(href['href'])
        titulo=capitulo.find('td').getText().split(':')[1]
        

        print ("%s: %s" % (href.getText(),titulo))
        #print ('http://www.mangareader.net'+str(url_capitulo))
        #print (url_capitulo)

        #Crear carpeta del capitulo
        CreateFolder(i,'./mangas/'+anime)

        #Lista de las urls de las imagenes de cada capitulo
        urls_capitulos=ListPages(url_capitulo)
        format= '%03d' if len(urls_capitulos)>99 else '%02d'
        # if len(urls_capitulos)>99:
        #     format='%03d'
        # else:
        #     format='%02d'

        for j,url_capitulo in enumerate(urls_capitulos,1):
            
            dir='./mangas/'+anime+'/'+'%04d' % (i)+'/'+format % (j)

            #print (dir)
            print (url_capitulo)
            DownloadImage(url_capitulo,dir)

else:
    print ("Status Code %d" % statusCode)
