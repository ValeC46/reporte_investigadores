from bs4 import BeautifulSoup
import requests
from serpapi import GoogleSearch
import pandas as pd
from tabulate import tabulate
from random import random
from fpdf import FPDF
from datetime import date

API_KEY = '85d081160e73cef8176cd0dce93a8111679c077faaa5dc5d14d5e6ac362d45b5'

def get_soup(url: str):
    response = requests.get(url)
    return BeautifulSoup(response.content, 'html.parser')

def output_df_to_pdf(pdf, df):
    # A cell is a rectangular area, possibly framed, which contains some text
    # Set the width and height of cell
    table_cell_width = 15
    table_cell_height = 6
    # Select a font as Arial, bold, 8
    pdf.set_font('Arial', 'B', 10)
    
    # Loop over to print column names
    cols = df.columns
    for col in cols:
        if col == 'Articulos':
            pdf.cell(150, table_cell_height, col, align='C', border=1)
        else:
            pdf.cell(table_cell_width, table_cell_height, col, align='C', border=1)
    # Line break
    pdf.ln(table_cell_height)
    # Select a font as Arial, regular, 10
    pdf.set_font('Arial', '', 10)
    # Loop over to print each data in the table
    for row in df.itertuples():
        for col in cols:
            value = str(getattr(row, col))
            if col == 'Articulos':
                pdf.cell(150, table_cell_height, value, align='C', border=1)
            else:
                pdf.cell(table_cell_width, table_cell_height, value, align='C', border=1)
        pdf.ln(table_cell_height)

# user = 'LM6o-YAAAAAJ'
pdf = FPDF()
pdf.add_page()
pdf.set_font('Arial', 'B', 18)

# 2. Layout the PDF doc contents
## Title
pdf.cell(40, 10, 'Publicaciones de Investigadores de FCFM')
## Line breaks
pdf.ln(20)

# params = {
#     'engine': 'google_scholar_author',
#     'author_id': user,
#     'api_key': API_KEY,
#     'sort': 'pubdate'
# }

# search = GoogleSearch(params)
# result = search.get_dict()
# for article in result.get("articles", []):
#     title = article.get("title")
#     cited_by = article.get("cited_by", {}).get("value")
#     year = article.get("year")
#     print(title, '\t', year, '\t', cited_by)

base = pd.read_csv('ScholarLink.csv')

for sep in range(0,3):
    articles = []
    cited = []
    years = []
    user = base['username'][sep]
    # params = {
    #     'engine': 'google_scholar_author',
    #     'author_id': user,
    #     'api_key': API_KEY,
    #     'sort': 'pubdate'
    # }
    # search = GoogleSearch(params)
    # result = search.get_dict()
    pdf.add_page()
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(40, 10, base['Name'][sep])
    article = 0
    for article in range(0,5): #result.get("articles", []):
        # titulo = article.get("title")
        # cited_by = article.get("cited_by", {}).get("value")
        # year = article.get("year")
        titulo = random()
        cited_by = random()
        year = random()
        articles.append(titulo)
        cited.append(cited_by)
        years.append(year)
    
    final = pd.DataFrame(articles, columns=['Articulos'])
    final['Año'] = years
    final['Citas'] = cited
    pdf.ln(20)
    output_df_to_pdf(pdf, final)
    # print('\n',base['Name'][sep])
    # print('\n', tabulate(final), '\n')

# 3. Output the PDF file
mydate = date.today()
year = mydate.year
month = mydate.month
pdf.output(f'fpdf_pdf_report.pdf', 'F')