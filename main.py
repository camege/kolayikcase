import requests
import json
import csv

TOKEN = ""
BASE_URL = "https://kolayik.com/api/v2/"
person_list = []

class Person:
  def __init__(self,id, name, surname):
    self.id = id
    self.name = name
    self.surname = surname
  tckimlikNo = ''
  totalVacationDays = 0;

def getIDs():
  #collects internal IDs for individuals
  url = BASE_URL + "person/list"
  payload = {'status': 'active'}
  files = [
  ]
  headers= {"Authorization": TOKEN}

  response = requests.request("POST", url, headers=headers, data = payload, files = files)

  json_data = json.loads(response.text)

  for item in json_data['data']['items']:
    p1 = Person(item['id'],item['firstName'], item['lastName'])
    person_list.append(p1)
  

def kimlikNoRequest(person_id):
  #API request to get TC Kimlik No with Kolay IDs
  url = BASE_URL + "person/view/" + person_id

  payload = {}
  headers= {"Authorization":TOKEN}

  response = requests.request("GET", url, headers=headers, data = payload)

  json_data = json.loads(response.text)
  return json_data['data']['person']['idNumber']


def getKimlikNos():
  #Defines TC Kimlik Nos to the Kolay IDs
  for person in person_list:
    tcID = kimlikNoRequest(person.id)
    person.tckimlikNo = tcID
    

def vacationDayRequest(person_id):
  #Gets total approved vacation days per Kolay ID
  #timestamps are hardcoded for the sake of simplicity, dynamic variables can be used for future purposes

  url = BASE_URL + "leave/list?status=approved&startDate=2019-10-07 00:00:00&endDate=2022-10-07 23:59:59&limit=10&personId=" + person_id

  payload = {}
  headers= {"Authorization":TOKEN}

  response = requests.request("GET", url, headers=headers, data = payload)

  json_data = json.loads(response.text)
  tempVac = 0;
  for data in json_data['data']:
    tempVac += data['usedDays']
  return tempVac

def getVacationDays():
  #Defines total vacation days per Kolay ID
  for person in person_list:
    vac = vacationDayRequest(person.id)
    person.totalVacationDays = vac

def generateReport():
  #Does all the API calls to collect the relevant info and publishes a report with that info
  getIDs()
  getKimlikNos()
  getVacationDays()
  with open('izinraporu.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Ad", "Soyad", "TC Kimlik No", "Toplam Izin Gunu"])
    for person in person_list:
      writer.writerow([person.name, person.surname, person.tckimlikNo, person.totalVacationDays])


if __name__ == "__main__":
  generateReport()
  
