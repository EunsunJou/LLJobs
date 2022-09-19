# -*- coding:utf8 -*-

from bs4 import BeautifulSoup
import requests
import re
import datetime

# Timestamp for naming output file
nowDatetime = datetime.datetime.now().strftime('%Y%m%d_%H%M')

# Code will export job announcements into text file
out = open("LLjobs2019"+nowDatetime+".txt", "w", encoding='utf8')

# Assign the default url of the year to variable "base2017"
# In 2017 there were up to 4811 annoucements (Up to November 12th)
# So the last available url is https://linguistlist.org/issues/28/28-4811.html
base2019 = "https://linguistlist.org/issues/30/30-" 

def Soup(url):
    # Use headers; otherwise the site will block you as a "robot."
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    # Open some url,
    response = requests.get(url, headers=headers)
    # And create a BeautifulSoup object for the html code of that page.
    soup = BeautifulSoup(response.text, 'html.parser')
    return(soup)

# If you want to simply count how many job offers there are,
# Use the "Job Filter" here.
'''
def Jobfilter(soup):
    jobs = soup.find(content="Jobs")
    if jobs:
        return True
    else:
        return False
'''

# From a BS object of a job announcement, extract the following specifics.
def JobSpecs(soup):
    univ = soup.find(string=re.compile("University or Organization"))
    loc = soup.find(string=re.compile("Job Location"))
    rank = soup.find(string=re.compile("Job Rank"))
    area = soup.find(string=re.compile("Specialty Areas"))
    return([univ, loc, rank, area])


''' The basic idea:
   1) Look at each announcement of the year
   2) Check if it's a job announcement
   3) If it IS a job announcement, extract relevant info

   It's inefficient, but The whole loop takes only half a second for each page. '''
for num in range(1, 4975):   # Run code in two parts (1-2600 and 2601-4811) if necessary
    url = base2019+str(num)+'.html' # url of the specific announcement
    soup = Soup(url)  # make a BS object of the html in the url
    '''Check if url is job announcement  by checking whether the html code includes 
    the text "Job Location", which is unique in Job announcements. 
    ("University or Organization" is also present in internship announcements)'''
    if JobSpecs(soup)[1]:   
        # write out announcement num. for reference. 
        # The equal sign is the column delimiter for Excel later.
        out.write("30-"+str(num)+": =")
        # String splice is to exclude boilerplate.
        # E.g. "Job Location: California, USA" --> "California, USA"
        out.write(JobSpecs(soup)[0][29:].encode('utf8').decode()+'=')
        out.write(JobSpecs(soup)[1][14:].encode('utf8').decode()+"=")
        out.write(JobSpecs(soup)[2][10:].encode('utf8').decode()+"=")
        out.write(JobSpecs(soup)[3][17:].encode('utf8').decode())
        out.write("\n")  
        # Print Progress
        print("page "+str(num)+"...JOBS!")
    else:
        # Print Progress
        print("page "+str(num)+"...")


out.close()