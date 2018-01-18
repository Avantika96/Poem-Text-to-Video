import os
import sys

import imageio
import urllib
from urllib.request import urlretrieve

from textblob import TextBlob,Word
from bs4 import BeautifulSoup
import requests

blob = TextBlob(open("humpty.txt").read())

for item in blob.sentences:
     print(item.replace('\n', ' '))
print("\n\n")

print("Parts of Speech in the poems:\n1.NN->Noun\n2.VB->Verb\n3.JJ->Adjective\n4.IN->Prepositions\n5.RB->Adverb\n6.CC->Conjunction\n")
for item,pos in blob.tags:
     if pos=="NN" or pos=="VB" or pos=="JJ" or pos=="IN" or pos=="RB" or pos=="CC" or pos=="NNP" or pos=="VBP"  or pos=="VBD" or pos=="VBN" or pos=="VBG" or pos=="VBZ" or pos=="JJS" or pos=="JJR":
          print(item+" : "+pos)
print("\n\n")

nouns = list()
for word, tag in blob.tags:
    if tag == 'NN':
         if word not in nouns:
             nouns.append(word.lemmatize())
print("This Poem is about...")
for i,item in enumerate(nouns):
    word = Word(item)
    print(word.pluralize())
print("\n\n")


print("Noun phrase:")
phrases=[]
tags=[]
for item,tag in blob.tags:
     phrases.append(item)
     tags.append(tag)
i=0

filenames=[]
while i<len(phrases):
     data=""
     if tags[i]=='VB' or tags[i]=='VBP' or tags[i]=='VBD' or tags[i]=='VBN' or tags[i]=='VBG' or tags[i]=='VBZ' or tags[i]=='JJ' or tags[i]=='JJR' or tags[i]=='JJS':
          if i+1<len(phrases):
               if tags[i+1]=='NN' or tags[i+1]=='NNP' or tags[i+1]=='NNPS' or tags[i+1]=='IN' :
                  print(phrases[i]+" "+phrases[i+1])
                  url=requests.get("https://www.shutterstock.com/search/?search_source=base_landing_page&language=en&searchterm="+phrases[i]+"+"+phrases[i+1]+"&image_type=all")
                  data=url.text
                  i=i+1
               else:
                    print(phrases[i])
                    url=requests.get("https://www.shutterstock.com/search/"+phrases[i])
                    data=url.text
     elif tags[i]=='NP'or tags[i]=='ADJP' or tags[i]=='NN' or tags[i]=='NNP' or tags[i]=='NNPS':
        print(phrases[i])
        url=requests.get("https://www.shutterstock.com/search/"+phrases[i])
        data=url.text
        
        
     
     soup=BeautifulSoup(data,"html.parser")
     imgs=soup.findAll("div",{"class":"search-content"})
     for li in imgs:
          imgUrl=requests.get("https://www.shutterstock.com"+li.a['href'])
          data1=url.text
          s=BeautifulSoup(data1,"html.parser")
          imgs1=s.findAll("ul",{"class":"search-results-grid mosaic-grid js_mosaic js_responsive"})
          for li in imgs1:
               imageUrl=li.find("div",{"class":"img-wrap"})
               image="http:"+imageUrl.img['src']
               urlretrieve(image, os.path.basename(phrases[i]+".jpg"))
               filenames.append(phrases[i]+".jpg")
     i=i+1

#print(filenames)
#with imageio.get_writer('movie.gif', mode='I') as writer:
#    for filename in filenames:
#        image = imageio.imread(filename)
#         writer.append_data(image)

images = []
for filename in filenames:
    images.append(imageio.imread(filename))
imageio.mimsave("movie.gif", images, format='GIF', duration=1.5)
os.system("movie.gif")

