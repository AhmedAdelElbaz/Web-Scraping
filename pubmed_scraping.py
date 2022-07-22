##### This code scrape Pubmed website looking for all articles related to list of genes
######## Used Libraries
import requests
from bs4 import BeautifulSoup
import csv
from itertools import zip_longest
## Creating the list of genes
list_of_genes = ["CTTNBP2NL"]
file_path = "D:/MAIN/WORK/BIOMET/PRODUCTS/"
#Starting the for loop for each gene
for gene in list_of_genes:
    print(gene)
    page_num = 1
    links = []
    abstracts = []
    PMIDs = []
    Authors = []
    Titles = []
    Journals = []
    Dates = []
    Citations = []
#While loop until we reach the last page of articles for this particular gene
    while True:
        print(f"page {page_num}")
        result = requests.get(f"https://pubmed.ncbi.nlm.nih.gov/?term={gene}&page={page_num}")
        # save page content as a variable called src 
        src = result.content
        # Create soup object to parse content
        soup = BeautifulSoup(src , "lxml")
        number = soup.find("label" , {"class": "of-total-pages"}).text #to get max number of pages include articles related to this gene
        if page_num > int(str(number)[3:]):
            print("Last Page")
            break
        #getting the div that contains the link
        info = soup.find_all("div", {"class": "docsum-content"})
        #extracting the links for all the article related to that gene
        for i in range(len(info)):
            link = info[i].find("a", {"class" : "docsum-title"})
            links.append(link.attrs['href'])
        #increasing the page number in the while loop
        page_num += 1 
        print("Page Switched")

    #Accessing each link
    link_num = 1
    for link in links:
        print(f"link number {link_num}")
        #extracting html tags from the page
        result = requests.get(f"https://pubmed.ncbi.nlm.nih.gov/{link}")
        src = result.content
        soup = BeautifulSoup(src , "lxml")
        #extracting abstract , ID , authors , Title , Journal , Date , number of citations as tags
        abstract = soup.find("div" , {"class": "abstract-content selected" , "id": "enc-abstract"})
        PMID = soup.find("strong" , {"class" : "current-id" , "title" : "PubMed ID"})
        Author_list = soup.find_all("a" , {"class": "full-name" , "data-ga-category": "search" })
        Title = soup.find("h1" , {"class": "heading-title"})
        Journal = soup.find("button" , {"class": "journal-actions-trigger trigger" , "id" : "full-view-journal-trigger"})
        Date = soup.find("span" , {"class": "cit"})
        cited_by = soup.find("em" , {"class" : "amount"})
        #if this tag is not empty get the text inside
        if Author_list is not None:
            temp = []
            for each in Author_list:
                temp.append(str(each.get_text()))
        else:
            temp = []
        #the same for abstract
        if abstract is not None:
            abstracts.append(abstract.find("p").text.strip())
        else:
            abstracts.append("Unknow Abstract")
        #Citations
        if cited_by is not None:
            Citations.append(cited_by.text)
        else:
            Citations.append(0)
        #Journals
        if Journal is not None:
            Journals.append(Journal.text.strip())
        else:
            Journals.append("Unknown Journal")
        #title
        if Title is not None:
            Titles.append(Title.text.strip())
        else:
            Titles.append("Unknown Title")
        #date
        if Date is not None:
            Dates.append(Date.text.strip().split(';')[0])
        else:
            Dates.append("Unknow Date")
        #Author list
        if Author_list is not None:
            Authors.append(temp[0:int(len(temp)/2)])
        else:
            Authors.append("Unknown Authors")
        #ID
        if PMID is not None:
            PMIDs.append(PMID.text)
        else:
            PMIDs.append("Unknown PMID")
        link_num +=1
    #Creating a list to be filled in the excel sheet
    File_list = [Titles , abstracts , PMIDs , Authors ,  Journals , Dates, Citations]
    exported = zip_longest(*File_list) #To fill be column
    with open(f"{file_path}{gene}-pubmed.csv", "w",encoding="utf-8") as myfile:
        wr = csv.writer(myfile)
        wr.writerow(["Titles" , "Abstracts" , "Pubmid IDs" , "Authors" , "Journals" , "Dates of Publications", "Number of citations"])
        wr.writerows(exported)
    #finshed the first gene 
    print("Finished")

    print(len(PMIDs))
print(f"check : {file_path}")  