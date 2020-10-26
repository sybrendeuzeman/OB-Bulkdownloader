import urllib3, certifi, json
import xml.etree.ElementTree as ET

def getxml(url):
    http_data_doc = http.request('GET', url).data.decode('utf-8')
    return ET.fromstring(http_data_doc)

def getjson(url):
    http_data_doc = http.request('GET', url).data.decode('utf-8')
    return json.loads(http_data_doc)

http = urllib3.PoolManager(
    cert_reqs='CERT_REQUIRED',
    ca_certs=certifi.where()
)

def download(url, file_name):
    # open in binary mode
    with open(file_name, "wb") as file:
        # get request
        response = http.request('GET', url).data
        # write to file
        file.write(response)

