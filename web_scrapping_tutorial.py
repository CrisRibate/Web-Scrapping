import requests
from bs4 import BeautifulSoup

url='https://jarroba.com/'

#Peticion a la web
req = requests.get(url)

#Comprobacion de que la peticion devuelve un Status Code = 200 (exito)
# Si empieza por 4 o 5 significa que ha habido un error
statusCode=req.status_code
if statusCode==200:
    #Pasar el contenido HTML de la web a un objeto BeautifulSoup()
    soup=BeautifulSoup(req.text, "html.parser")

    #Obtener todos los divs donde estan las entradas
    entradas=soup.find_all('div',{'class':'col-md-4 col-xs-12'})

    #Recorrer todas las entradas para extraer el titulo, autor y fecha
    for i, entrada in enumerate(entradas):
        #Con el métdo "getText()" devuelve el HTML
        titulo=entrada.find('span', {'class':'tituloPost'}).getText()

        #Si no se llama al metodo "getText()",devolverátambién el HTML
        autor=entrada.find('span',{'class':'autor'}).getText()
        fecha=entrada.find('span', {'class':'fecha'}).getText()

        #Imprimir el Titulo, Autor y Fecha de las entradas
        print ("%d-%s |%s|%s" % (i+1,titulo,autor,fecha))
else:
    print ("Status Code %d" %status_code)