import requests
from bs4 import BeautifulSoup
import pandas as pd 



def Arbitrage_2way(url):
    data = requests.get(url)
    soup = BeautifulSoup(data.text) 
    script_tag = soup.find_all('div', class_='px-1')
    name = []
    number = []

    for i in range(1, len(script_tag)-1):
        string = script_tag[i].text
        string = string.replace('\n', ' ')
        string = string.replace('X', ' ')
        string = string[20:]
        for k in range(len(string)):

            if string[k-1] == ' ' and string[k] == '1' and string[k+1] == ' ':
                new_string = string[:k] + string[k+1:]

        for k in range(len(new_string)):
            if new_string[k-1] == ' ' and new_string[k] == '2' and new_string[k+1] == ' ':
                string2 = new_string[:k] + new_string[k+1:]

        elements = string2.split()

        names = elements[:-2]
        numbers = elements[-2:]  
        names1 = ''.join(str(e) for e in names)
        numbers = list(map(float, numbers))
        name.append(names1)
        number.append(numbers)

    traspose = list(zip(*number))
    price1 = traspose[0]
    price2 = traspose[1]  
    data_ = {'Name': name,  'Price 1': price1, 'Price 2': price2}
    df_ = pd.DataFrame(data_)
    df_["arb"] = (1/df_[ 'Price 1'] + 1/df_['Price 2'] < 1).astype(int)
    return df_


def Arbitrage_3way(url):
    data = requests.get(url)
    soup = BeautifulSoup(data.text) 
    script_tag = soup.find_all('div', class_='px-1')
    name = []
    number = []
    date1 = []

    for i in range(1, len(script_tag)-1):
        string = script_tag[i].text
        string = string.replace('\n', ' ')
        string = string.replace('X', ' ')
        date = string[2:10]
        string = string[20:]
        for k in range(len(string)):

            if string[k-1] == ' ' and string[k] == '1' and string[k+1] == ' ':
               new_string = string[:k] + string[k+1:]

        for k in range(len(new_string)):
            if new_string[k-1] == ' ' and new_string[k] == '2' and new_string[k+1] == ' ':
                string2 = new_string[:k] + new_string[k+1:]
        
        date1.append(date)
        elements = string2.split()
        names = elements[:-3]
        numbers = elements[-3:]  
        names1 = ''.join(str(e) for e in names)
        numbers = list(map(float, numbers))
        name.append(names1)
        number.append(numbers)

    traspose = list(zip(*number))
    price1 = traspose[0]
    price2 = traspose[1]
    price3 = traspose[2] 
    data_ = {'date': date1, 'Name': name,  'Price 1': price1, 'Price 2': price2, 'Price 3': price3}
    df_ = pd.DataFrame(data_)
    df_["arb"] = (1/df_[ 'Price 1'] + 1/df_['Price 2'] + 1/df_['Price 3'] < 1).astype(int)
    df_["percent"] = 1/df_[ 'Price 1'] + 1/df_['Price 2'] + 1/df_['Price 3']
    return df_



url = 'https://www.sportytrader.com/es/apuestas/futbol/'
df = Arbitrage_3way(url)
df2 = df[df['arb']==1]
df2 = df2[df2["percent"] < 0.96]
print(df2)