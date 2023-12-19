from bs4 import BeautifulSoup
import requests
import pandas as pd
from serpapi import GoogleSearch
from datetime import date
import openpyxl

API_KEY = '85d081160e73cef8176cd0dce93a8111679c077faaa5dc5d14d5e6ac362d45b5'
LIMITE = 10

def get_soup(url: str):
    response = requests.get(url)
    return BeautifulSoup(response.content, 'html.parser')

def get_hrefs(x: int, titles: list, hrefs: list):
    soup = get_soup(f"https://www.uanl.mx/investigadores/page/{x}")
    table = soup.find_all('ul')[21].find_all('li')
    for x in range(len(table)):
        title = soup.find_all('ul')[21].find_all('li')[x].a.string
        href = soup.find_all('ul')[21].find_all('li')[x].a.get('href')
        titles.append(title)
        hrefs.append(href)

## DECLARACION DE VARIABLES
titles = []
hrefs = []
scholar = []
usuarios = []
names = ['Álvaro Eduardo Cordero Franco', 'Abraham Benito Barragán Amigón', 'Alfredo Tlahuice Flores']

## OBTENCION DE LINKS DE CADA INVESTIGADOR A SU PAGINA DE LA UANL
for x in range(1, 100):
   get_hrefs(x, titles, hrefs)
   print(f'Page {x} done!')
# print(titles,hrefs)

data = pd.DataFrame(titles, columns=['Name'])
data['HREF'] = hrefs

cleandata = data.query('Name not in ("Mail", "Facebook", "Twitter", "YouTube")')

print(cleandata.head())
# cleandata.to_csv('LinkOriginal.csv')

## DADA LA LISTA DE NOMBRES SE OBTIENE EL LINK A GOOGLE SCHOLAR Y SU USUARIO
i = 0
for name in names:
    i += 1
    for ind in cleandata.index:
        if cleandata['Name'][ind] == name:
            soup = get_soup(cleandata['HREF'][ind])
            table = soup.find_all('ul')[21].find_all('li')
            for x in range(len(table)):
                title = soup.find_all('ul')[21].find_all('li')[x].a.string
                if title == "Google Scholar" or title == " Google Scholar" or title == "Google Scholar ":
                    href = soup.find_all('ul')[21].find_all('li')[x].a.get('href')
                    link_partido = href.split('=')
                    user_sucio = link_partido[1].split('&')
                    user = user_sucio[0]
                    if user == 'en' or user == 'es':
                        user_sucio = link_partido[2].split('&')
                        user = user_sucio[0]
                    scholar.append(href)
                    usuarios.append(user)
                    # print(user)
    if scholar.__len__() != i:
        href = 'N/A'
        user = 'N/A'
        scholar.append(href)
        usuarios.append(user)

base = pd.DataFrame(names, columns=['Name'])
base['Link Scholar'] = scholar
base['username'] = usuarios
print(base)
# base.to_csv('ScholarLink.csv')

## OBTENER ARTICULOS DE CADA INVESTIGADOR
mydate = date.today()
ano = mydate.year
month = mydate.month
day = mydate.day

with pd.ExcelWriter('excel_report.xlsx', engine='openpyxl') as writer:
    for sep in base.index:
        articles = []
        cited = []
        years = []
        user = base['username'][sep]
        params = {
            'engine': 'google_scholar_author',
            'author_id': user,
            'api_key': API_KEY,
            'sort': 'pubdate'
        }
        search = GoogleSearch(params)
        result = search.get_dict()
        y = 0
        for article in result.get("articles", []):
            if y <= LIMITE:
                titulo = article.get("title")
                cited_by = article.get("cited_by", {}).get("value")
                year = article.get("year")
                articles.append(titulo)
                cited.append(cited_by)
                years.append(year)
            y+=1
        
        final = pd.DataFrame(articles, columns=['Articulos'])
        final['Año'] = years
        final['Citas'] = cited
        final.to_excel(writer, base['Name'][sep])
      