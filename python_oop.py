import json
import requests
import resilient
import configparser
import time
import os
global basedir
basedir = os.path.abspath(os.path.dirname(__file__))

class alienVault():
    url = 'https://otx.alienvault.com/api/v1/pulses/5d120d47d09d67b4d8dc5241'
    def __init__(self,headers):
        self.headers=headers


    def fetch_feed(self):
        response = requests.get(self.url, headers=self.headers)
        response_json = response.json()
        # print(json.dumps(response_json, indent=4))
        return response_json

    #def send_feed(self,feed):
    #   with open('eventfeeds.json','a+') as write_file:
    #      json.dump(feed, write_file)
    #     write_file.write("\n")


class resilientAPI():
    def __init__(self):
        pass



    def client_connection(self):
        config = configparser.ConfigParser()
        section = "resilient"

        config.read("config.cfg")
        host = config.get(section, 'host')
        port = config.get("resilient", 'port')
        email = config.get("resilient", 'email')
        password = config.get("resilient", 'password')
        org = config.get("resilient", 'org')
        url = "https://{0}:{1}".format(host, port or 443)
        client = resilient.SimpleClient(org_name=org,
                                        base_url=url,
                                        verify=False)

        userinfo = client.connect(email, password)
        assert userinfo
        print("working")
        return client

    def fetch_incident(self, client):
        incident_id = 2120
        url = "/incidents/{}?handle_format=names".format(incident_id)
        response = client.get(url)
        assert response
        return response

class KeyInfomationGathering():
    eventFeeds=[]

    def __init__(self):
        pass

    def save_feeds(self, feed):
        list_of_feeds=[]
        list_of_feeds.append(feed)
        print(list_of_feeds)
        #with open('eventfeeds.json', 'a+') as write_file:
        #   json.dump(feed, write_file)
        #  write_file.write(",\n")

    def temp(self):
        with open('eventfeeds.json', 'a+') as write_file:
            write_file.write("]")

    def retrieve_key_info(self):
        with open('eventfeeds.json','r') as read_file:
            data=json.load(read_file)

        for i in data:
            print(json.dumps(i, indent=4))
            tempFeed={}
            if 'id' in i or 'author' in i:
                try:
                    # resilient info gathering
                    id = i['id']
                    eventName=i['name']
                    orgName=i['properties']['gsma_member']
                    date=i['create_date']
                    tlp=i['severity_code']
                    category=i['incident_type_ids'][0]
                    store_key_info(id, eventName, orgName, tlp, category, date)
                except:
                    # alien vault info gathering
                    id = i['author']['id']
                    eventName = i['name']
                    orgName = i['author_name']
                    tlp = i['TLP']
                    category = i['industries'][0]
                    date = i['created']
                    store_key_info(id, eventName, orgName, tlp, category, date)

    def store_key_info(self, id, eventName, orgName, tlp, category, date):
        tempFeed.update( {"id":id, 'eventName':eventName, 'orgName':orgName,
                          'date':date, 'tlp':tlp, 'category':category})
        eventFeed.append(tempFeed)

def main():
    headers = {
        'X-OTX-API-KEY': '4dcb5c735bcbc704ab7c3744df540e5d8caece6089684dcb68feb2c733a1b5d9'
    }
    apiObject = KeyInformationGathering()
    otxObject = alienVault(headers)
    otx_feed = otxObject.fetch_feed()
    # otxObject.send_feed(otx_feed)
    KeyInformationGathering.save_feed(otx_feed)

    resilientObject = resilientAPI()
    resilient_feed = resilientObject.fetch_incident(resilientObject.client_connection())
    KeyInformationGathering.save_feed(resilient_feed)
#  otxObject.send_feed(feed)

if __name__ == "__main__":
    main()
