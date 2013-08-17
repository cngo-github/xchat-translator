__module_name__ = "translator"
__module_version__ = "0.1"
__module_description__ = "Translates from one language to other using Google Translate via YQL."
__module_author__ = "drag <drag.publicgithub@gmail.com>"

import xchat

import json
import urllib2

DEST_LANG = 'en'
AUTOUSER = {}

class TranlateException(Exception):
	pass

class TranslatorClass:
	LANGUAGES = {
		'ENGLISH' : 'en',
		'FRENCH' : 'fr',
		'RUSSIAN' : 'ru'
	}

	LANG_CODES = set(LANGUAGES.values())

	def translate(cls, msg, target, src):
		langs = '';

		if targetLang not in cls.LANG_CODES:
			raise TranslateException('Target language not supported.')

		if srcLang == None:
			langs = '|' + targatLang
		elif srcLang in cls.CODES_SET:
			langs = srcLang + '|' + targetLang
		else:
			raise TranslateException('Source language not supported.')

		url = "http://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20google.translate%20where%20q%3D%22" + msg + "%22%20and%20target%3D%22" + target + "%22%20and%20source%3D%22" + src + "%22%3B&format=json&diagnostics=true&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys&callback="
		headers = { 'User-Agent': 'Mozilla/5.0' }
		req = urllib2.Request(url, None, headers)
		response = urllib2.urlopen(req)

		result = json.load(response)
		resultArray = result['query']['results']['json']['json'][0]['json']

		str = ""
		if type(resultArray) is dict:
			str += resultArray['json'][0]
		else:
			for subDict in resultArray:
				str += subDict['json'][0]

		return str

class TranslateThread(Thread):
	def __init__(self, queue):
		Threat.__init__(self, target=self.doTranslate())
		self.queue = queue
		self.keepalive=True

	def doTranslate(self) {
		global LAST_ERROR

		while True:
			task = self.queue.get()

			if not self.keepalive or task = None:
				break
			try:
				context, user, src, target, text = task
				translation = Translator.translate(text, target, src)
				xchat.prnt("Translation : " + translation)
			except TranslateException, e:
				LAST_ERROR = "[TE: %s] <%s>" %(e, user, text)
			except urllib2.URLError, e:
				LAST_ERROR = "[URL] %s" %e
			except UnicodeError, e:
				LAST_ERROR = "[Encode: %s] <%s> %s" %(e, user, text)

def autoTranslate(word, world_eo1, userdata):
	global AUTOUSER
	global DEST_LANG

	channel = xchat.get_info('channel')
	user = word[1]
	dest = DEST_LANG
	src = None
	
	if len(word) > 2:
		dest = word[2]
	if len(word) > 3:
		src = word[3]

	AUTOUSER[channel + ' ' + user.lower()] = (dest, src)
	xchat.prnt("User '%s' has been added to auto-translate list" %user)
	return xchat.EAT_ALL

xchat.hook_command("atr", autoTranslate)

def removeAutoTranslate(word, word_eol, userdata):
	global AUTOUSER

	channel = xchat.get_info('channel')
	user = word[1]
	target = channel + ' ' + user

	if AUTOUSER.pop(target, None) != None:
		xchat.prnt("User %s has been removed from the auto-translate list" %user)
	return xchat.EAT_ALL

xchat.hook_command("rmatr", removeAutoTranslate)

def printAutouser(word, word_eol, userdata):
	global AUTOUSER

	channel = xchat.get_info('channel')
	users = [target.split(' ')[1] for target in AUTOUSER.keys()]

	xchat.prnt("Currently automatically translating messages for the folloing users: %s" %(' '.join(users)))
	xchat.EAT_ALL

xchat.hook_command("lsatr", printAutouser)

def translateTo(word, word_eo1, userdata):
	xchat.prnt("Starting translate");
	if len(word) < 2:
		print "No message found."
	else:
		message = "Всем Хай, пацаны"
		#message = urllib2.quote(message2.encode('utf8'))
		target = "en"
		src = "ru"
		url = "http://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20google.translate%20where%20q%3D%22" + message + "%22%20and%20target%3D%22" + target + "%22%20and%20source%3D%22" + src + "%22%3B&format=json&diagnostics=true&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys&callback="
		headers = { 'User-Agent': 'Mozilla/5.0' }
		req = urllib2.Request(url, None, headers)
		response = urllib2.urlopen(req)

		result = json.load(response)
		resultArray = result['query']['results']['json']['json'][0]['json']
		str = ""
		if type(resultArray) is dict:
			str += resultArray['json'][0]
		else:
			for subDict in resultArray:
				str += subDict['json'][0]

		xchat.prnt(str)
		xchat.command('say Translation complete.')
	return xchat.EAT_ALL

xchat.hook_command("tr", translateTo, help="/tr <message> translates message into the language specified.")

def runAutoTranslate(word, word_eol, userdata):
	global AUTOUSER

	user = word[0]
	text = word[1]
	channel = xchat.get_info('channel')
	target = channel + ' ' + user.lower()

	if AUTOUSER.has_key(target):
		xchat.prnt("New message from %s, translating..." %user)

	return xchat.EAT_ALL

xchat.hook_print("Channel Message", runAutoTranslate)
