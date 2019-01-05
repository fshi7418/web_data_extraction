from bs4 import BeautifulSoup
from requests import get
from datetime import date


# get_content(element) returns a string that represents the text content of an html element
def get_content(element):
    return element.renderContents().decode('utf-8')


# list_average(lis) consumes a list of floats or integers and returns a float that is the average value of lis
def list_average(lis):
    return sum(lis) / len(lis)


stock_ticker = 'g'

earnings_root_url = 'https://web.tmxmoney.com/earnings.php?qm_symbol='
earnings_url = earnings_root_url + stock_ticker
earnings_site = get(earnings_url)
earnings_soup = BeautifulSoup(earnings_site.text, 'html.parser')

# financials_root_url = 'https://web.tmxmoney.com/financials.php?qm_symbol='
# financials_url = financials_root_url + stock_ticker

quote_root_url = 'https://web.tmxmoney.com/quote.php?qm_symbol='
quote_url = quote_root_url + stock_ticker
quote_site = get(quote_url)
quote_soup = BeautifulSoup(quote_site.text, 'html.parser')

# Get the full company name
quote_name = earnings_soup.find_all('div', attrs={'class': 'quote-name'})[0]
company_name = get_content(quote_name.find_all('h2')[0])

# Get the current price
quote_price = earnings_soup.find_all('div', attrs={'class': 'quote-price priceLarge'})[0]
current_price = get_content(quote_price.find_all('span')[0])

# Get the market cap
quoting_table = quote_soup.find_all('table', attrs={'class': 'detailed-quote-table'})
market_cap = get_content(quoting_table[1].find_all('td', attrs={'class': ''})[5])
market_cap = market_cap.replace(',', '')
market_cap = int(market_cap)

# Get the table where all the historical EPS values exist
table = earnings_soup.find_all('div', attrs={'class': 'earningstable'})
all_rows = table[0].find_all('tr', attrs={'class': lambda x: x != ''})
l = len(all_rows)
# print(all_rows[l - 1].find_all('td'))

# get the current year and the year seven years ago
today = str(date.today())
current_year = int(today[:4])
current_year_sub_seven = current_year - 7


# compile the list containing all the quarterly data on the EPS
historical_eps_list = {}
i = 0
while i < l - 1:
    k = i
    each_row = all_rows[i].find_all('td')
    # each_row is a list of <td> objects
    # print(each_row)
    if get_content(each_row[0]) != 'N/A':
        year = int(get_content(each_row[0])[-4:])
        # print(year)
        if year < current_year_sub_seven:
            break
        increment = 0
        while k < l - 1:
            year_next_row = int(get_content(all_rows[k].find_all('td')[0])[-4:])
            if year_next_row == year:
                k += 1
                increment += 1
            else:
                break
        temp_counter = 0
        annual_eps = 0
        while temp_counter < increment:
            interim_eps = get_content(all_rows[i + temp_counter].find_all('td')[2])
            if interim_eps == '--':
                break
            else:
                interim_eps = float(interim_eps)
            annual_eps = annual_eps + interim_eps
            temp_counter += 1
        historical_eps_list[year] = annual_eps
        i = i + increment
    else:
        i += 1

# print the result
intro_phrase_a = 'The detailed historical EPS of stock ' + stock_ticker.upper() + ' over the last 7 yeras is: '
intro_phrase_b = 'The average EPS of stock ' + stock_ticker.upper() + ' over the last seven years is: '


keys_list = list(historical_eps_list.keys())
list_length = len(historical_eps_list.keys())

for i in range(list_length):
    key = keys_list[i]
    if historical_eps_list[key] == 0:
        del historical_eps_list[key]


a_billion = 1000000000
print(historical_eps_list.values())
print(intro_phrase_b + str(round(list_average(historical_eps_list.values()), 3)))
print('Company full name is: ' + company_name)
print('Current price is: ' + current_price)
print('Market Cap is: ' + str(round(market_cap / a_billion, 1)) + 'B')

