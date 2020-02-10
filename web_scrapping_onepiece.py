import requests
from bs4 import BeautifulSoup
import os
import shutil

URL_MANGA = 'http://www.mangareader.net'

def ListPages(url, name):

    main_url=URL_MANGA+str(url)
    print (main_url)

    req=requests.get(url)

    statusCode=req.status_code
    if statusCode==200:
        #Pasar el contenido HTML de la web a un objeto BeautifulSoup()
        soup=BeautifulSoup(req.text, "html.parser")

        #Numero imagenes
        paginas=soup.find('div',{'id':'selectpage'})
        options = paginas.find_all('option')
        urls_imgs=list(map(lambda option: URL_MANGA+option['value'],options))

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
        '''

        #Ubicacion imagen
        ub_image=soup.find('id', {'imgholder'})
    else:
        print ("Status Code %d en %s" %(status_code,name))

'''
def Folder():
    def CreateFolder(name):
        directory = name
        parent_dir= "./mangas"
        path = os.path.join(parent_dir,directory)

        try:
            os.mkdir(path)
        except OSError as error:
            print(error)
    
    def DownloadImage(url):
        # Open the url image, set stream to True, this will return the stream content
        resp=requests.get(url, stream=True)

        local_file=open('local_image.jpg','wb')

        # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
        resp.raw.decode_content = True
        
        # Copy the response stream raw data to local image file.
        shutil.copyfileobj(resp.raw, local_file)
        
        # Remove the image url response object.
        del resp
'''

url=URL_MANGA+'/one-piece'

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
    for i,capitulo in enumerate(capitulos[0:5]):
        #Con el métdo "getText()" devuelve el HTML
        href=capitulo.find('a', href=True)
        url_capitulo=URL_MANGA+str(href['href'])
        titulo=capitulo.find('td').getText().split(':')[1]
        

        print ("%s: %s" % (href.getText(),titulo))
        #print ('http://www.mangareader.net'+str(url_capitulo))
        #print (url_capitulo)
 
        ListPages(url_capitulo,href.getText())

else:
    print ("Status Code %d" % statusCode)
