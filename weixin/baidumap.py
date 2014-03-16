import sys
from urllib.parse import *
def get_baidu_address(latitude, longitude):
    import pycurl, json
    from io import BytesIO
    addr_req = pycurl.Curl()
    addr_resp = BytesIO()
    addr_req.setopt(pycurl.WRITEFUNCTION, addr_resp.write)
    ak = 'GLbmnUGjCe4B62dqW6l695fL'
    url = 'http://api.map.baidu.com/geocoder/v2/?ak=%s&callback=renderReverse&location=%s,%s&output=json&pois=1'%(ak, latitude, longitude)
    addr_req.setopt(addr_req.URL, url)
    addr_req.perform()
    addr = json.loads((addr_resp.getvalue().decode()[29:-1]))
    return addr['result']['formatted_address']


def get_baidu_location(address):
    import pycurl, json
    from io import BytesIO
    addr_req = pycurl.Curl()
    addr_resp = BytesIO()
    addr_req.setopt(pycurl.WRITEFUNCTION, addr_resp.write)
    ak = 'GLbmnUGjCe4B62dqW6l695fL'
    address = quote(address)
    url = 'http://api.map.baidu.com/geocoder/v2/?ak=%s&callback=showLocation&address=%s&output=json'%(ak, address)
    #print('url is :' + url)
    addr_req.setopt(addr_req.URL, url)
    addr_req.perform()
    response = json.loads((addr_resp.getvalue().decode()[27:-1]))
    return response

def convert_baidu_location(latitude, longitude):
    import pycurl, json
    from io import BytesIO
    addr_req = pycurl.Curl()
    addr_resp = BytesIO()
    addr_req.setopt(pycurl.WRITEFUNCTION, addr_resp.write)
    ak = 'GLbmnUGjCe4B62dqW6l695fL'
    url = 'http://api.map.baidu.com/geoconv/v1/?coords=%s,%s&from=1&to=5&ak=%s&output=json'%(longitude, latitude, ak)
    #print('url is :' + url)
    addr_req.setopt(addr_req.URL, url)
    addr_req.perform()
    response = json.loads((addr_resp.getvalue().decode()))#[27:-1]))
    return response['result'][0]['y'], response['result'][0]['x']

#print(sys.getdefaultencoding())
#print(get_baidu_location('百度大厦'))

#print(get_baidu_address('39.971353229973','116.30799772131'))
#print(convert_baidu_location('39.965202','116.301544'))

