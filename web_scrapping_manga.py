import requests
from bs4 import BeautifulSoup
import os
import shutil
import unicodedata
import sys

#Fuction that return a list of the urls of the images in a chapter
def ListPages(url):
    main_url=url_manga+str(url)
 
    req=requests.get(url)

    statusCode=req.status_code
    if statusCode==200:
        soup=BeautifulSoup(req.text, "html.parser")

        #list of each page where there are the images of the chapter (but there are not the final url)
        pages=soup.find('div',{'id':'selectpage'})
        options = pages.find_all('option')

        urls_pages=list(map(lambda option: url_manga+option['value'],options))

        return list(map(ListImg,urls_pages))

    else:
        print('Error %d Page List' % (statusCode))
        return None


#Fuction that return  the url of a page's images
def ListImg(url):
    req=requests.get(url)

    statusCode=req.status_code
    if statusCode==200:
        soup=BeautifulSoup(req.text, "html.parser")
        img_url=soup.find('div',{'id':'imgholder'}).find('img')
        return img_url['src']

    else:
        print ('Error %d in the image url' %(statusCode))
        return None


#Fuction that creates a folder
def CreateFolder(name,dir="./mangas",format='%3d'):
    if type(name) is int:
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


 #Fuction that download image of a url  
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


#Fuction that creates a list of urls of each chapter
def ListChapters(url):
    list_chapters=[]

    req = requests.get(url)

    statusCode=req.status_code
    if statusCode==200:
        soup=BeautifulSoup(req.text, "html.parser")

        #Get a chapters list
        table=soup.find('table',{'id':'listing'})
        chapters=table.find_all('tr')

        #Eliminate table_head (no chapter) of the list
        del chapters[0]

        #Go through all the entries to extract the title
        for i,chapter in enumerate(chapters,1):
            href=chapter.find('a', href=True)
            url_chapter=url_manga+str(href['href'])
            list_chapters.append(url_chapter)

        return list_chapters
            
    else:
        print ('Error searching for manga name')
        return list_chapters


#Fuction that downloads chapters
def Download_chapters_Range(chapters,n,format):
    print ('Downloading... ')
    
    #Check if mangas folder exists
    if not os.path.isdir('./mangas'):
        CreateFolder('mangas','./')
        print ('\tmangas folder created')

    #Make folder of the manga
    if not os.path.isdir('./mangas/'+name_manga_folder):
        CreateFolder(name_manga_folder)
        print('\t%s folder created'%(name_manga_folder))
    
    #Begining download
    for i,chapter in enumerate(chapters,n):
        #Create chapter folder
        CreateFolder(i,'./mangas/'+name_manga_folder,format)

        #List of the image urls of each chapter
        chapter_urls=ListPages(chapter)
        format_img= '%03d' if len(chapter_urls)>99 else '%02d'

        #Download images
        for j,chapter_url in enumerate(chapter_urls,1):          
            dir='./mangas/'+name_manga_folder+'/'+format % (i)+'/'+format_img % (j)
            DownloadImage(chapter_url,dir)
            
        print('\tChapter %d downloaded'%(i))



#------------------------------------------
#-------Main Web Scrapping-----------------
#------------------------------------------

url_manga = 'http://www.mangareader.net'

#Greeting
print ('Welcom to Web Scrapping \nThis program downloads manga from mangareader.com')

#Loop if manga name is incorrect
len_manga=0
counter=False
while len_manga is 0:

    #Choose exit program
    if counter is True:    
        finish=input ('Finish program? (Y/N): ')

        finish=finish.lower()
        if finish =='y':
            sys.exit()

    counter=True
            
    name_manga= input('Manga\'s name:')

    #Edit manga's name and manga's folder name
    name_manga= name_manga.lower()  #Lowercase
    name_manga=name_manga.strip()   #Remove spaces at the beginning and the end

    name_manga_folder=name_manga.title()
    name_manga_folder="_".join(name_manga_folder.split())

    name_manga="-".join(name_manga.split()) #Change many spaces by dash

    #Calculate list of chapters
    list_chapters=ListChapters(url_manga+'/'+name_manga)
    len_manga=len(list_chapters)

#Format of the chapter's folder name
if len_manga<100:
    format_chapter='%02d'
elif len_manga<1000:
    format_chapter='%03d'
else: format_chapter='%04d'

option=None

#Select chapter to download
print ('\nThere are %d chapters' % (len_manga))
print ('Choose one of the next options to download:\n A: All\n B: The First\n C: The Lastest\n D: Range\n E: Choose a chapter\n F: Nothing\n')

counter=False
while option is None:
    if counter is True:
        print('Try again')

    option=input('Option: ')

    option=option.lower()

    #Download chapters
    if option=='a' or option=='1':
        Download_chapters_Range(list_chapters,1,format_chapter)
    elif  option=='b' or option=='2':
        Download_chapters_Range([list_chapters[0]],1,format_chapter)
    elif option=='c'or option=='3':
        Download_chapters_Range([list_chapters[len_manga-1]],len_manga,format_chapter)
    elif option=='d'or option=='4':
        print ('Download:')
        start=input(' From chapter (number): ')
        end=input(' To chapter (number): ')
        Download_chapters_Range(list_chapters[int(start)-1:int(end)],int(start),format_chapter)
    elif option=='e'or option=='5':
        choise=input('Chapter to download (number): ')
        Download_chapters_Range([list_chapters[int(choise)-1]],int(choise),format_chapter)
    elif option=='f'or option=='6':
        pass
    else: 
        option=None
        counter=True

print ('Finish! Goodbye :)')