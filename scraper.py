from bs4 import BeautifulSoup
import re
import csv
import bs4

PROVINCE = 'nwt'

with open((PROVINCE + '.html'), 'r', encoding='utf8') as html:
    soup = BeautifulSoup(html, 'html.parser')

output = []

data = soup.find_all('li')

def parse_url(element):
    url = element.find('a', rel='noopener')
    if(isinstance(url,bs4.element.Tag)):
        return url['href']
    else:
        return 'No Link Found'

def parse_name(element):
    name = element.find_all()
    if(isinstance(name,bs4.element.ResultSet)):
        return name[0].text
    else:
        return 'No Name Found'

def parse_bio(element):
    output = str(element).split('<br/>')
    output[1] = output[1].replace('\n          ',' ')
    output[1] = output[1].replace(' — ','')
    return output[1]

def parse_email(element):
    email = element.select('a[href^=mailto]')
    for i in email:
        href = i['href']
        try:
            nothing, email = href.split(':')
        except ValueError:
            break

        return email

for line in data:
    name = parse_name(line)
    url = parse_url(line)
    bio = parse_bio(line)
    email = parse_email(line)

    new = [name.strip(), url, str(bio), email]
    output.append(new)

# print(output)

fields = ['Name', 'URL', 'Bio', 'Contact Email'] 

with open((PROVINCE + '.csv'), 'w', newline='') as file:
    write = csv.writer(file, delimiter= '|')
    write.writerow(fields)
    write.writerows(output)