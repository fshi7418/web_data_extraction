# Downloads all the mathNEWS articles from a single website

from requests import get
from urllib.request import urlretrieve
from bs4 import BeautifulSoup
import os

url = 'http://mathnews.uwaterloo.ca/?m=201803'
basic_path = 'C:\\Users\\Frank Shi\\Dropbox\\mathNEWS'
response = get(url)

# The 'html.parser' argument indicates that we want to do the parsing using
#   python's built-in HTML parser.
html_soup = BeautifulSoup(response.text, 'html.parser')

entries = html_soup.find_all('div',class ='entry-content')

# print(entries)

pdfs = []
for i in range(len(entries)):
    pdf = entries[i].find_all('a')
    pdfs.append(pdf)
    
#print(pdfs)
issue = str(pdfs[0][0])

# get_pdf(s) returns the url of the pdf file
def get_pdf(s):
    relevant = s[9:]
    i=4
    while i < len(relevant):
        if relevant[-i:][:4] == '.pdf':
            break
        i += 1
    return relevant[:-i+4]

# month_dict is a dictionary that stores month in English in accordance to month in number

month_dict={'01':'Jan','02':'Feb','03':'Mar','04':'Apr','05':'May','06':'Jun',
            '07':'Jul','08':'Aug','09':'Sep','10':'Oct','11':'Nov','12':'Dec'}

## naming_pdf(s) consumes a pdf url (type str) as s and returns a string that
##   indicates the correct path of the download.

## get_volume(s) consumes a pdf url s and returns the volume of the pdf
def get_volume(s):
    extension = s.split('/')[-1].split('-')
    volume = extension[-2]
    issue = extension[-1].split('.')[0]
    #answer = volume+'.'+issue
    return 'Volume '+volume

def naming_pdf(s):
    ## get_issue(s) consumes a PDF url and returns the issue of the PDF
    def get_issue(s):
        extension = s.split('/')[-1].split('-')
        volume = extension[-2]
        issue = extension[-1].split('.')[0]
        answer = volume+'.'+issue
        return answer
    
    year = s.split('/')[-3]
    month = month_dict[s.split('/')[-2]]
    return year+month+get_issue(s)+'.pdf'

## The main program

for i in range(len(pdfs)):
    folder_name = get_volume(get_pdf(str(pdfs[i][0])))
    folder_path = basic_path+'\\'+folder_name
    if not os.path.exists(folder_path) == True:
        os.mkdir(folder_path)
    print(folder_path)
    for j in range(len(pdfs[i])):
        issue = str(pdfs[i][j])
        print(issue)
        pdf_url = get_pdf(issue)  # The URL of the pdf file
        print(pdf_url)
        pdf_path = folder_path+'\\'+naming_pdf(pdf_url)
        print(pdf_path)
        urlretrieve(pdf_url,pdf_path)
        
## The next goal is to loop through all the archives of mathNEWS
