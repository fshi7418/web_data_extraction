import requests
import xlwt
from bs4 import BeautifulSoup


def name(txt):

    start = 5
    end = txt.find(" ", txt.find(", ") + 2)
    new_str = txt[start:end]
    first_name = new_str[new_str.find(", ") + 2:]
    last_name = new_str[:new_str.find(", ")]
    return first_name, last_name


def extent(num):

    if num.find("<b>") is not None and num.find("</b>") is not None:
        start = num.find("<b>") + 3
        end = num.find("</b>")
        new_str = num[start:end]

        return new_str
    return "Oops"

profile_url = 'https://ist.uwaterloo.ca/phone/pers_dir_detail.html'
source_code = requests.get(profile_url)
plain_text = source_code.text
soup = BeautifulSoup(plain_text, 'html.parser')
table_entries = soup.find_all('tr')
records = []
counter1 = 0

for entry in table_entries:

    info = entry.find_all('td')
    counter2 = 0

    for x in info:
        if counter2 == 0:
            first_name, last_name = name(str(x))
            records.append([first_name, last_name])
            counter2 += 1

        elif counter2 == 1:
            extents = extent(str(x))
            records[counter1].append(extents)
            counter2 += 1

    counter1 = len(records)

book = xlwt.Workbook(encoding="utf-8")
sheet1 = book.add_sheet("Sheet 1")
sheet1.write(0, 0, "First Name")
sheet1.write(0, 1, "Last Name")
sheet1.write(0, 2, "Extension")

counter = 1

for record in records:

    sheet1.write(counter, 0, record[0])
    sheet1.write(counter, 1, record[1])
    sheet1.write(counter, 2, record[2])

    counter += 1

book.save("UW Contacts.xls")
print("finished")