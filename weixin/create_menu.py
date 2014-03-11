import pycurl, json
from io import *

token_req = pycurl.Curl()
token_resp = BytesIO()
token_req.setopt(pycurl.WRITEFUNCTION, token_resp.write)
token_req.setopt(token_req.URL, 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=wx784e3545d1e8273e&secret=822c0fe8ad5a99e81fe329c37b96a0d3')
#token_req.setopt(token_req.HTTPHEADER, ['Accept: text/html', 'Accept-Charset: UTF-8'])
#try:
if True:
    token_req.perform()
    print("token_req HTTP-code: %s" % (token_req.getinfo(token_req.HTTP_CODE)))
    token = json.loads(token_resp.getvalue().decode())['access_token']
    print('token is : %s' % (token))
    menu_req = pycurl.Curl()
    menu_resp = BytesIO()
    menu_req.setopt(pycurl.WRITEFUNCTION, menu_resp.write)
    menu_req.setopt(menu_req.URL, ('https://api.weixin.qq.com/cgi-bin/menu/create?access_token=%s' % (token)))
    menu_body = '''{
     "button":[
     {	
          "type":"click",
          "name":"今日知识",
          "key":"TODAY_KNOWLEDGE"
      },
      {
           "type":"click",
           "name":"周边",
           "key":"AROUD_BABY"
      },
      {
           "name":"其他",
           "sub_button":[
           {	
               "type":"view",
               "name":"搜索",
               "url":"http://www.soso.com/"
            },
            {
               "type":"view",
               "name":"关于我们",
               "url":"http://wjbb.cloudapp.net/"
            }]
       }]
 }'''
    menu_req.setopt(menu_req.POSTFIELDS, menu_body.encode('utf-8'))
    menu_req.perform()
    print("menu_req HTTP-code: %s" % (menu_req.getinfo(menu_req.HTTP_CODE)))
    ret = json.loads(menu_resp.getvalue().decode())
    print('ret is : %s' % (ret))
#except pycurl.error as error:
#    print('An error occurred: %s', error)
