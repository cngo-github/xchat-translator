# -*- coding: utf-8 -*-

__module_name__ = "translator"
__module_version__ = "1.0"
__module_description__ = "Translates from one language to others using Google Translate."
__module_author__ = "Chuong Ngo, karona75, briand"

from urllib import parse as encoder
from urllib import request as http
from concurrent import futures as futures
import json
import hexchat
import pprint

max_threads = 10
default_tgt = 'en'
default_src = 'auto'
default_encoding = 'UTF-8'

AUTOUSER = {}

# url = 'http://translate.google.com/translate_a/t?q=This%20is%20a%20test&client=x&text=&sl=auto&tl=de&ie=UTF-8'
useragent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; de; rv:1.9.1.5) Gecko/20091102 Firefox/3.5.5'

base_url = 'http://translate.google.com/translate_a/t?'
base_client = 'x'
base_text = ''

def worker(id, url, useragent):
	print('Running translation job ' + str(id))
	headers = {'User-agent': useragent}
	req = http.Request(url, None, headers)
	response = http.urlopen(req)

	data = response.read().decode('utf-8')
	data = json.loads(data)

	print('Ran translation job ' + str(id))
	translation = data['sentences'][0]['trans']
	hexchat.command('say ' + translation)

def makeUrl(message, tgt_lang = default_tgt, src_lang = default_src, client = 'x', text = '', encoding = default_encoding):
	translation_params = {
		'q': message,
		'client': client,
		'text': text,
		'sl': src_lang,
		'tl': tgt_lang,
		'ie': encoding
	}
	url = base_url + encoder.urlencode(translation_params)
	return url;

thread_pool = futures.ThreadPoolExecutor(max_workers = max_threads)

'''
	Translates the message to the specified language with source language detection
'''
def translateDetectLang(word, word_eol, userdata):	
	destLang = word[1]
	message = word_eol[2]

	url = makeUrl(message, tgt_lang = destLang);
	thread_pool.submit(worker, 1, url, useragent)

	return hexchat.EAT_ALL

help_message = '/TR <target language> <message> - translates message into the language specified.  This auto detects the source language.  This is not threaded.' 
hexchat.hook_command("TR", translateDetectLang, help = help_message)

'''
	Shuts down the threads and thread controller when unloading the module.
'''
def unload_translator(userdata):
	thread_pool.shutdown(wait = True)
	print('Translator is unloaded')

hexchat.hook_unload(unload_translator)

print('Translator script loaded successfully.')