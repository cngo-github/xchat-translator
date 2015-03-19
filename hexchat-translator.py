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
import calendar
import time

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
	run_id = calendar.timegm(time.gmtime())
	thread_pool.submit(worker, run_id, url, useragent)

	return hexchat.EAT_ALL

help_message = '/TR <target language> <message> - translates message into the language specified. This assumes the default source language.' 
hexchat.hook_command("TR", translateDetectLang, help = help_message)

'''
	Translates the message to the specified language assuming that the source language is the one specified.
'''
def translateNoDetect(word, word_eol, userdata):
	srcLang = word[1]
	destLang = word[2]
	message = word_eol[3]

	url = makeUrl(message, tgt_lang = destLang, src_lang = srcLang);
	run_id = calendar.timegm(time.gmtime())
	thread_pool.submit(worker, run_id, url, useragent)

	return hexchat.EAT_ALL

help_message = '/TM <source_language> <target_language> <message> - translates message into the language specified.'
hexchat.hook_command("TM", translateNoDetect, help = help_message)

'''
	Adds a user to the watch list to automatically translate.
'''
def addUser(word, word_eol, userdata):
	if len(word) < 2:
		hexchat.prnt("You must specify a user.")
		return xchat.EAT_ALL

#	user = word[1]
#	dest = DEFAULT_LANG
#	src = None

#	if len(word) > 2 and Translator.findLangCode(word[2]) is not None:
#		dest = word[2]

#	if len(word) > 3 and Translator.findLangCode(word[3]) is not None:
#		src = word[3]

#	AUTOUSER[xchat.get_info('channel') + ' ' + user.lower()] = (dest, src)
#	xchat.prnt("Added user %s to the watch list." %user)

#	return xchat.EAT_ALL

#xchat.command('MENU ADD "$NICK/[+] AutoTranslate" "ADDTR %s"')
#xchat.hook_command("ADDTR", addUser, help = "/ADDTR <user_nick> <target_language> <source_language> - adds the user to the watch list for automatic translations.  If target_language is not specified, then the DEFAULT_LANG set will be used.  If source_language is not specified, then language detection will be used.")

'''
	Removes a user from the watch list to automatically translate.
'''
#def removeUser(word, word_eol, userdata):
#	if len(word) < 2:
#		xchat.prnt("You must specify a user.")
#		return xchat.EAT_ALL

#	user = word[1]

#	if AUTOUSER.pop(xchat.get_info('channel') + ' ' + user.lower(), None) is not None:
#		xchat.prnt("User %s has been removed from the watch list." %user)

#	return xchat.EAT_ALL

#xchat.command('MENU ADD "$NICK/[-] AutoTranslate" "RMTR %s"')
#xchat.hook_command("RMTR", removeUser, help = "/RMTR <user_nick> - removes user_nick from the watch list for automatic translations.")

'''
	Prints automatic translations watch list.
'''
def printWatchList(word, word_eol, userdata):
	users = [ key.split(' ')[1] for key in AUTOUSER.keys()]

	hexchat.prnt("WatchList: %s" %(" ".join(users)))
	hexchat.EAT_ALL

help_message = '/LSUSERS - prints out all users on the watch list for automatic translations to the screen locally.'
hexchat.hook_command("LSUSERS", printWatchList, help = help_message)

'''
	Adds a new translation job to the queue.
'''
def addJob(word, word_eol, userdata):
	channel = hexchat.get_info('channel')
#	key = channel + " " + word[0].lower()

#	if(AUTOUSER.has_key(key)):
#		dest, src = AUTOUSER[key]
#		ThreadController.addJob((xchat.get_context(), word[0], src, dest, word[1]))

#	return xchat.EAT_NONE

#xchat.hook_print("Channel Message", addJob)

'''
	Shuts down the threads and thread controller when unloading the module.
'''
def unload_translator(userdata):
	thread_pool.shutdown(wait = True)
	print('Translator is unloaded')

hexchat.hook_unload(unload_translator)

print('Translator script loaded successfully.')
