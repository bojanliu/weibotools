from weibo import APIClient


appkey=''
appsecret=''
callback=''

client = APIClient(app_key=appkey, app_secret=appsecret,redirect_uri=callback)

url=client.get_authorize_url()

print url
code='6a1b0f4caeb2d120eae935b7db0d06fb'

r = client.request_access_token(code)
access_token = r.access_token
expires_in = r.expires_in

print access_token
print expires_in

