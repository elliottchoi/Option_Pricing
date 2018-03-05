from bs4 import BeautifulSoup
import pandas as pd
import requests

'''
Intiating panda frame to store option data
'''
df=pd.DataFrame({'Type of Option':[],'Last Price':[],'Strike Price':[],'Last Trade':[],'Bid':[],'Ask':[],'volume':[],'open interest':[],'expiration date':[],'mid':[],'spread':[]})

'''
Per Stock Code
'''


#Which url we want to scrape
url_stock_ticker='https://www.marketwatch.com/investing/stock/mmm/options'
response=requests.get(url_stock_ticker)
#Assinging a beautiful soup object
soup_stock_ticker = BeautifulSoup(response.content,'html.parser')
#print in a nice context
#print (soup.prettify())

'''
Getting all option data for a MMM for that month (puts and options)
Store this into a list that contains all the hrefs
'''
list=[]
for option in soup_stock_ticker.findAll('a', class_='optionticker'):
    list.append(option.get('href'))
i=0
while i <len(list):
    list[i]='https://www.marketwatch.com'+list[i]
    i+=1

#gathering specific option data
url_option_data=list[1]
print(url_option_data)
#print(url_option_data)
response=requests.get(url_option_data)
soup_option_data=BeautifulSoup(response.content,'html.parser')
#print(soup_option_data.prettify())

#Finding call or put:
generic_header=soup_option_data.find(class_="block sixwide")
#print(generic_header.prettify())
type_of_option=generic_header.find('h2').get_text()
type_of_option=type_of_option[0:3]


#General
generic_header=soup_option_data.find(id="optioninfo")
#print(generic_header.prettify())
'''
                                 0             1        2      3       4  5   6           7              8        
Define an array with indexes: [type of option,last,strike,last trade,bid,ask,volume,open interest, expiration date]
'''
option_info=[]
option_info.append(type_of_option)

option_info.append(generic_header.find(class_='data lastcolumn subheader').get_text())
#print(option_info)

#Gathering all the option data
for option in generic_header.findAll(class_='data lastcolumn'):
    option_info.append(option.get_text())

#Cleaning all option data for xml parsing
option_info.remove(option_info[2])
option_info.remove(option_info[4])
option_info.remove(option_info[6])
option_info.remove(option_info[6])
for i in range(8):
    option_info[i]=option_info[i].replace('\xa0',"0")
    option_info[i]=option_info[i].replace(' ','')
    option_info[i]=option_info[i].replace('\r\n','')

#Array is created in ['Type of option','Last Price','Strike Price','Last Trade','Bid','Ask','volume','open interest','expiration date',mid,spread]
#mid_value=(int(option_info[4])+int(option_info[5]))/2
#spread_percentage=(mid_value)/int(option_info[4])
#option_info.append(mid_value)
#option_info.append(spread_percentage)

'''
Adding to pandas frame
'''
#df=pd.DataFrame({'Type of Option':[],'Last Price':[],'Strike Price':[],'Last Trade':[],'Bid':[],'Ask':[],'volume':[],'open interest':[],'expiration date':[],'mid':[],'spread':[]})
#print(df)




