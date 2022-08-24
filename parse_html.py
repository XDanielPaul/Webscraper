from bs4 import BeautifulSoup
from ftfy import fix_text
import requests
import json
import re

# Class containing resulting data
class DataObj:

    def __init__(self,title,place,salary,contract_type,contact_email):
        self.title = title
        self.place = place
        self.salary = salary
        self.contract_type = contract_type
        self.contact_email = contact_email
    
    # Converting to Json
    def jsonify(self):
        return json.dumps({"title": self.title, "place": self.place, "salary" : self.salary, "contract_type" : self.contract_type, "contact_email": self.contact_email}, ensure_ascii=False)
    
    # Debug print
    def __str__(self):
        return "Job title: " + self.title +"\nJob place: " + self.place   +"\nJob Salary: " + self.salary   +"\nContract Type: " + self.contract_type   +"\nContact Email: " + self.contact_email     

# Scraping place, salary and contract_type 
def extract_data(datalist, p_tags, attr, title, email):
    # Find all paragraphs that have desired attribute and "strong" child tag
    tags = [x for x in p_tags if x.has_attr(attr) and x.contents[0].name == "strong"]
    work_data = []
    for tag in tags:
        work_data.append(fix_text(tag.contents[2]))
    
    # Array out of bound check
    if len(work_data) > 2:
        datalist.append(DataObj(title, work_data[0], work_data[1], work_data[2], email))

### Find all jobs ###
url = 'https://www.hyperia.sk'
html = requests.get(url = url+"/kariera").text
soup = BeautifulSoup(html, 'html.parser')
a_tags = soup.find_all('a')
# Job parameters are contained in href html
hrefs = [x['href'] for x in a_tags if x.has_attr('data-v-7325ada6')]

### Find parameters for each job ###
datalist = []
# Attributes in each individual htmls of jobs
data_attr = ['data-v-40947e0c','data-v-33202b72', 'data-v-24b0271e', 'data-v-20aa20bd' , 'data-v-3c09929c', 'data-v-c46ea594']
# Getting desired informations
for href,attr in zip(hrefs,data_attr):
    # Connecting href route to url 
    dataurl = url + href
    html = requests.get(url = dataurl).text
    soup = BeautifulSoup(html, 'html.parser')

    # Scraping title
    title = soup.find('h1').text.replace('Å¡','Š')

    # Scraping e-mail
    email = soup.find('strong', text = re.compile("(\w*\@\w*\.\w*)")).text

    # Scraping place, salary and contract type
    p_tags = soup.find_all('p')
    extract_data(datalist, p_tags, attr , title, email)
    
### Creating json file ###
json_list = []
with open('result.json','w') as f:
    for data in datalist:
        json_list.append(data.jsonify())
    json.dump(json_list, f, ensure_ascii=False)
