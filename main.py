import os
import csv
import requests
from bs4 import BeautifulSoup

os.system("clear")
alba_url = "http://www.alba.co.kr"

alba_result = requests.get(alba_url)
alba_soup = BeautifulSoup(alba_result.text,'html.parser')

superbrand = alba_soup.find("div",{"id":"MainSuperBrand"})
superbrand_urls = []
superbrand_name = []
for link in superbrand.find_all('a',{"class","goodsBox-info"}):
  superbrand_urls.append(link.get('href'))
  superbrand_name.append(link.find("span",{"class":"company"}).string)

#여기까지 브랜드의 이름과 주소 추출


for i in range(0 , len(superbrand_urls)):
  jobs = []
  url_request = requests.get(superbrand_urls[i])
  print(superbrand_urls[i])
  url_soup = BeautifulSoup(url_request.text,'html.parser')
  
  job_soups = url_soup.find("div",id = "NormalInfo").find("tbody").find_all("tr")
  
  job = {}
  for soup in job_soups[0::2]:
    #place
    place = soup.find("td",{"class":"local first"}).get_text()
    place = place.replace(u'\xa0',u'')
  
    #title
    title = str(soup.find("span",{"class":"company"}).string)
  
    #time
    time = soup.find("td",{"class":"data"}).get_text()
  
    #pay
    pay_soup = soup.find("td",{"class":"pay"})
    pay_string = ""
    for list in pay_soup.find_all("span"):
      if pay_string == "":
        pay_string = list.get_text()
      else:
        pay_string = pay_string + "," + list.get_text()
  
    #date
    date_soup = soup.find("td",{"class":"regDate last"})
    date = date_soup.get_text()
    
  
    job = {"place":place , "title":title, "time":time, "pay":pay_string, "date": date}
    jobs.append(job)
  
  # print(jobs)
  # 파일 만들기 후 저장
  
  file_name = superbrand_name[i].replace("/"," ")
  file = open(file_name + ".csv", mode = "w")
  writer = csv.writer(file)
  writer.writerow(["place","title","time","pay","date"])
  
  for job in jobs:
    writer.writerow([job["place"],job["title"],job["time"],job["pay"],job["date"]])
  
  file.close()

#여기서 값들 얻어내기


