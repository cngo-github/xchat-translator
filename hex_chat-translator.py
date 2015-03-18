# -*- coding: utf-8 -*-

__module_name__ = "translator"
__module_version__ = "1.0"
__module_description__ = "Translates from one language to others using Google Translate."
__module_author__ = "Chuong Ngo, karona75, briand"

from threading import Thread
from urllib import request as http

# http://translate.google.com/translate_a/t?q=This%20is%20a%20test&client=x&text=&sl=auto&tl=de&ie=UTF-8
# 'User-agent' : 'Mozilla/5.0 (Windows; U; Windows NT 5.1; de; rv:1.9.1.5) Gecko/20091102 Firefox/3.5.5'

url = 'http://translate.google.com/translate_a/t?q=This%20is%20a%20test&client=x&text=&sl=auto&tl=de&ie=UTF-8'
useragent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; de; rv:1.9.1.5) Gecko/20091102 Firefox/3.5.5'
headers = {'User-agent' : useragent}
req = http.Request(url, None, headers)
response = http.urlopen(req)
# response = http.urlopen("http://translate.google.com/translate_a/t?q=This%20is%20a%20test&client=x&text=&sl=auto&tl=de&ie=UTF-8")
#print(response.status_code)
print(response.read())