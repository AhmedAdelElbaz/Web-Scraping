############################################
#Code to scrap NUPCO website to look for all info about tenders as a dataframe for further analysys#
#Date: 14/July/2022
#Python 3.8.9
#USED libraries (requests , BeautifulSoup , csv , itertools)
import requests
from bs4 import BeautifulSoup
import csv
from itertools import zip_longest
# use requests to fitch the url
result = requests.get("https://www.nupco.com/%d8%a7%d9%84%d9%85%d9%86%d8%a7%d9%81%d8%b3%d8%a7%d8%aa/")
# save page content as a variable called src 
src = result.content
# Create soup object to parse content
soup = BeautifulSoup(src , "lxml")
#Create lists
Tender_Numbs = []
Tender_states = []
Tender_Disc = []
Links = []
Dates_open =[]
Dates_open_table =[]
Dates_close_table =[]
Prices = []
#run the function find all to return a list containing the mentioned tag with specific class from the HTML code
Tender_Number = soup.find_all("div" , {"class": "box_arbic_col01"})#div is the chosen tag
Tender_State = soup.find_all("p" , {"class": "box_arbic_text_p"})#p is the chosen tag
Tender_Description = soup.find_all("div" , {"class": "box_aric04"})#div is the chosen tag
box = soup.find_all("div", {"class": "box"})#here the chosen tag includes much more i need 
for i in range(len(box)):#So i wrote this code to seelct only the divs with class box that includes a link "a"
    if box[i].find("a") == None:
        continue
    else:
        Links.append(box[i].find("a").attrs['href'])
#scraping each link 
for link in Links:
    result = requests.get(link)
    src = result.content
    soup = BeautifulSoup(src , "lxml")
    date = soup.find_all("div", {"class":"text_wrap_tender_details"})#this div contains all what i need
    Dates_open.append(date)
#filling my lists
for i in range(len(Tender_State)):
    Tender_Numbs.append(Tender_Number[i].text[16:27])
    Tender_states.append(Tender_State[i].text)
    Tender_Disc.append(Tender_Description[i].text[19:].strip())
    Dates_open_table.append(Dates_open[i][2].find('p').text)
    Dates_close_table.append(Dates_open[i][1].find('p').text)
    Prices.append(Dates_open[i][3].find('p').text)
#Create a csv file to fill
File_list = [Tender_Numbs , Tender_states , Tender_Disc , Dates_open_table , Dates_close_table , Prices, Links]
exported = zip_longest(*File_list)#to fill by column not by row
with open("D:/MAIN/WORK/BIOMET/PRODUCTS/Nupco.csv", "w") as myfile:
    wr = csv.writer(myfile)
    wr.writerow(["Tender_Numbs" , "Tender_states" , "Tender_Disc" , "Dates_open_table" , "Dates_close_table" , "Prices", "Links"])
    wr.writerows(exported)
#Happy end
print(len(Tender_State))
print("FINISHED")