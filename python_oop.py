import requests
import resilient
import configparser
import time
import os
global basedir
basedir = os.path.abspath(os.path.dirname(__file__))

class alienVault():
    url = 'https://otx.alienvault.com/api/v1/pulses/5d120d47d09d67b4d8dc5241'
    def __init__(self, url, headers):
        self.headers=headers


    def fetch_feed(self):
        response = requests.get(self.url, headers=self.headers)
        response_json = response.json()
        print(json.dumps(response_json, indent=4))


    def send_feed(self,feed):
        with open('eventfeeds.json','a+') as write_file:
            json.dump(feed, write_file)


class resilient(alienVault()):
    def __init__(self,host,port,email,password,org):
        self.host=host
        self.port=port
        self.email=email
        self.password=password
        self.org=org


    def client_connection():
        url = "https://{0}:{1}".format(host, port or 443)
        client = resilient.SimpleClient(org_name=org,
                                        base_url=url,
                                        verify=False)
        assert client
        userinfo = client.connect(email, password)
        assert userinfo
        print("working")
        return client

    def fetch_incident():
        incident_id = 2120
        url = "/incidents/{}?handle_format=names".format(incident_id)
        response = client.get(url)
        assert response
        return response
    
    
