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

    def send_feed(self,feed):
        with open('eventfeeds.json','a+') as write_file:
            json.dump(feed, write_file)
            write_file.write("\n")


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

def main():
    headers = {
        'X-OTX-API-KEY': '4dcb5c735bcbc704ab7c3744df540e5d8caece6089684dcb68feb2c733a1b5d9'
    }
    otxObject = alienVault(headers)
    otx_feed = otxObject.fetch_feed()
    otxObject.send_feed(otx_feed)
    resilientObject = resilientAPI()
   # feed = resilientObject.fetch_incident(resilientObject.client_connection())
  #  otxObject.send_feed(feed)

if __name__ == "__main__":
    main()
