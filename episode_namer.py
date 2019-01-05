from requests import get
from urllib.request import urlretrieve
from bs4 import BeautifulSoup
import os

url = 'https://en.wikipedia.org/wiki/List_of_Elementary_episodes'
path = 'E:\\TV\\Elementary'
response = get(url)

# The 'html.parser' argument indicates that we want to do the parsing using
#   python's built-in HTML parser.
html_soup = BeautifulSoup(response.text, 'html.parser')

entries = html_soup.find_all('table', attrs={'class':'wikitable plainrowheaders wikiepisodetable'})
# The above has all information of all six seasons
# print(entries[0])

s1_info = entries[0].find_all('tr', attrs={'class': 'vevent'})
print(s1_info[0])
print(s1_info[1])
# s1_info contains all info for all episodes of season 1

e1_title = s1_info[0].find('td', attrs={'class': 'summary'}).renderContents()
print(e1_title.strip())
print(len(s1_info))

# We try to build a list of all the titles of season 1 episodes as an exercise

print(list(range(24)))

s1_epis = {}
for ep in list(range(24)):
    ep_title = s1_info[ep].find('td', attrs={'class': 'summary'}).renderContents().strip()
    s1_epis[ep+1] = ep_title

print(s1_epis.keys())
print(s1_epis.values())


file_list = os.listdir(path + '\\1')
print(file_list)


def get_epi_num(file_name):
    return file_name[-6:-4]


def get_vid_format(file_name):
    return file_name[-4:]


print(get_epi_num(file_list[0]))
print(get_vid_format(file_list[0]))


for f in file_list:
    dst = get_epi_num(f) + get_vid_format(f)
    src = f

    os.rename(src, dst)


# info_row = entries.find_all('tr', attrs={'class': 'vevent'})
# print(infor_row)
# for season in range(1,6):
#     info_row = entries.find_all('tr', attrs={'class': 'vevent'})


