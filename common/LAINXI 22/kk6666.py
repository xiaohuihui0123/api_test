



from requests import request

# url = 'http://api.keyou.site:8000/user/register/'
# data = {'username':'huih44','email':'19482388@qq.com'}
# re = request(url=url,method='post',json=data)
# res = re.json()
# print(res)

url = 'http://api.keyou.site:8000/user/h54848 i/count/'
r = request(url=url,method='get')
re = r.json()
print(re)