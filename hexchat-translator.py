# -*- coding: utf-8 -*-

__module_name__ = "translator"
__module_version__ = "1.0"
__module_description__ = "Translates from one language to others using Google Translate."
__module_author__ = "Chuong Ngo, karona75, briand"

from urllib import request as http
from concurrent import futures as futures
import json
import pprint

max_threads = 10

url = 'http://translate.google.com/translate_a/t?q=This%20is%20a%20test&client=x&text=&sl=auto&tl=de&ie=UTF-8'
useragent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; de; rv:1.9.1.5) Gecko/20091102 Firefox/3.5.5'

def worker(id, url, useragent):
	print('Running translation job ' + str(id))
	headers = {'User-agent': useragent}
	req = http.Request(url, None, headers)
	response = http.urlopen(req)

	data = response.read().decode('utf-8')
	data = json.loads(data)

#	pp = pprint.PrettyPrinter(indent=4)
#	pp.pprint(data)
	print('Ran translation job ' + str(id))

thread_pool = futures.ThreadPoolExecutor(max_workers = maxworkers)

for i in range(max_threads):
	thread_pool.submit(worker, i, url, useragent)