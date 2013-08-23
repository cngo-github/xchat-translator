# -*- coding: utf-8 -*-

__module_name__ = "translator"
__module_version__ = "0.6"
__module_description__ = "Translates from one language to other using Google Translate via YQL."
__module_author__ = "drag, karona75"

import xchat

import json
import urllib2
import Queue
import threading
from threading import Thread
import traceback

DEFAULT_LANG = 'en'

AUTOUSER = {}
LAST_ERROR=''

class TranslateException(Exception):
	pass

class Translator:

	LANGUAGES = {
		'AFRIKAANS' : 'af',
	        'ALBANIAN' : 'sq',
	        'AMHARIC' : 'am',
	        'ARABIC' : 'ar',
	        'ARMENIAN' : 'hy',
	        'AZERBAIJANI' : 'az',
	        'BASQUE' : 'eu',
	        'BELARUSIAN' : 'be',
	        'BENGALI' : 'bn',
	        'BIHARI' : 'bh',
	        'BULGARIAN' : 'bg',
	        'BURMESE' : 'my',
	        'CATALAN' : 'ca',
	        'CHEROKEE' : 'chr',
	        'CHINESE' : 'zh',
	        'CHINESE_SIMPLIFIED' : 'zh-CN',
	        'CHINESE_TRADITIONAL' : 'zh-TW',
	        'CROATIAN' : 'hr',
	        'CZECH' : 'cs',
	        'DANISH' : 'da',
	        'DHIVEHI' : 'dv',
	        'DUTCH': 'nl',  
	        'ENGLISH' : 'en',
	        'ESPERANTO' : 'eo',
	        'ESTONIAN' : 'et',
	        'FILIPINO' : 'tl',
	        'FINNISH' : 'fi',
	        'FRENCH' : 'fr',
	        'GALICIAN' : 'gl',
	        'GEORGIAN' : 'ka',
	        'GERMAN' : 'de',
	        'GREEK' : 'el',
	        'GUARANI' : 'gn',
	        'GUJARATI' : 'gu',
	        'HEBREW' : 'iw',
	        'HINDI' : 'hi',
	        'HUNGARIAN' : 'hu',
	        'ICELANDIC' : 'is',
	        'INDONESIAN' : 'id',
	        'INUKTITUT' : 'iu',
	        'IRISH' : 'ga',
	        'ITALIAN' : 'it',
	        'JAPANESE' : 'ja',
	        'KANNADA' : 'kn',
	        'KAZAKH' : 'kk',
	        'KHMER' : 'km',
	        'KOREAN' : 'ko',
	        'KURDISH': 'ku',
	        'KYRGYZ': 'ky',
	        'LAOTHIAN': 'lo',
	        'LATVIAN' : 'lv',
	        'LITHUANIAN' : 'lt',
	        'MACEDONIAN' : 'mk',
	        'MALAY' : 'ms',
	        'MALAYALAM' : 'ml',
	        'MALTESE' : 'mt',
	        'MARATHI' : 'mr',
	        'MONGOLIAN' : 'mn',
	        'NEPALI' : 'ne',
	        'NORWEGIAN' : 'no',
	        'ORIYA' : 'or',
	        'PASHTO' : 'ps',
	        'PERSIAN' : 'fa',
	        'POLISH' : 'pl',
	        'PORTUGUESE' : 'pt-PT',
	        'PUNJABI' : 'pa',
	        'ROMANIAN' : 'ro',
	        'RUSSIAN' : 'ru',
	        'SANSKRIT' : 'sa',
	        'SERBIAN' : 'sr',
	        'SINDHI' : 'sd',
	        'SINHALESE' : 'si',
	        'SLOVAK' : 'sk',
	        'SLOVENIAN' : 'sl',
	        'SPANISH' : 'es',
	        'SWAHILI' : 'sw',
	        'SWEDISH' : 'sv',
	        'TAJIK' : 'tg',
	        'TAMIL' : 'ta',
	        'TAGALOG' : 'tl',
	        'TELUGU' : 'te',
	        'THAI' : 'th',
	        'TIBETAN' : 'bo',
	        'TURKISH' : 'tr',
	        'UKRAINIAN' : 'uk',
	        'URDU' : 'ur',
	        'UZBEK' : 'uz',
	        'UIGHUR' : 'ug',
	        'VIETNAMESE' : 'vi',
	        'WELSH' : 'cy',
	        'YIDDISH' : 'yi'
	}

	CODES_SET = set(LANGUAGES.values())

#	def findLangCode(codeSet, language):
#		language = language.upper()

#		if codeSet.LANGUAGES.has_key(language):
#			return codeSet.LANGUAGES[language]
#		else:
#			return None
#	findLangCode = classmethod(findLangCode)

	def translate(message, dest):
		url = "http://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20google.translate%20where%20q%3D%22" + message + "%22%20and%20target%3D%22" + dest + "%22%3B&format=json&diagnostics=true&env=http%3A%2F%2Fdatatables.org%2Falltables.env&callback="
		print 'Here3'
		headers = { 'User-Agent' : 'Mozilla/5.0' }
		req = urllib2.Request(url, None, headers)
		response = urllib2.urlopen(req)
		print 'Here4'
		return self.parseJsonResult(response.read())
	translate = classmethod(translate)

	def parseJsonResult(resultStr):
		result = resultStr
		resultArray = result['query']['results']['json']['json'][0]['json']
		retStr = ""
		print 'Here'
		if type(resultArray) is dict:
			retStr += resultArray['json'][0]
		else:
			for subDict in resultArray:
				retStr += subDict['json'][0]
		print 'Here2'
		retStr = retStr.encode("utf-8")
		return retStr
	parseJsonResult = classmethod(parseJsonResult)

class TranslatorThread(Thread):
	def __init__(self, queue):
		threading.Thread.__init__(self, target = self.run)
		self.queue = queue
		self.kill = False;

	def run(self):
		while True:
			job = self.queue.get()
			print 'running thread'
			if self.kill or task == None:
				break;
			try:
				context, user, targetLang, text = task

				translatedText = Translator.translate(text, targetLang)

				if translatedText.strip().lower() != text.strip().lower():
					context.emit_print("Channel Message", nick, translatedText)
			except TranslateException, e:
				LAST_ERROR = "[TE: %s] <%s> %s" %(e, user, text)
			except urllib2.URLError, e:
				LAST_ERROR = "[URL] %s" %e
			except UnicodeError, e:
				LAST_ERROR = "[Encode: %s] <%s> %s" %(e, user, text)

class WorkerController:
	jobs = Queue.Queue()
	worker = TranslatorThread(jobs)
	worker.setDaemon(True)
	worker.start()

	def addJob(cls, job):
		cls.jobs.put(job)
	addJob = classmethod(addJob)
'''
def getPage(message, src, dest):
	url = "http://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20google.translate%20where%20q%3D%22" + message + "%22%20and%20target%3D%22" + dest + "%22%20and%20source%3D%22" + src + "%22%3B&format=json&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys&callback="

	headers = { 'User-Agent' : 'Mozilla/5.0' }
	req = urllib2.Request(url, None, headers)
	response = urllib2.urlopen(req)
	return response.read()

def parseJsonResult(resultStr):
	result = resultStr
	resultArray = result['query']['results']['json']['json'][0]['json']
	retStr = ""

	if type(resultArray) is dict:
		retStr += resultArray['json'][0]
	else:
		for subDict in resultArray:
			retStr += subDict['json'][0]

	retStr = retStr.encode("utf-8")
	return retStr
'''

def translateDetectLang(word, word_eol, userdata):	
	destLang = word[1]
	message = unicode(word_eol[2], "utf-8")
	print 'translating'
	text = Translator.translate(message, destLang)

#	uMessage = unicode(message, "utf-8" )
#	page = getPageDetectLang(urllib2.quote(message), destLang)
#	result = json.loads(page)

	xchat.prnt("Translated: " + text)
	return xchat.EAT_ALL

xchat.hook_command("tr", translateDetectLang, help="/tr <target language> <message> translates message into the language specified.  This auto detects the source language.")

#def translate(word, word_eol, userdata):	
#	srcLang = word[1]
#	destLang = word[2]
#	message = word_eol[3]

#	uMessage = unicode(message, "utf-8" )
#	page = getPage(urllib2.quote(message), srcLang, destLang)
#	result = json.loads(page)

#	xchat.prnt("Translated: " + parseJsonResult(result))
#	return xchat.EAT_ALL

#xchat.hook_command("trm", translate, help="/trm <source language> <target language> <message> translates message into the language specified.")

#def translateTo(word, word_eol, userdata):
#	destLang = word[1]
#	message = word_eol[2]

#	uMessage = unicode(message, "utf-8" )
#	page = getPageDetectLang(urllib2.quote(message), destLang)
#	result = json.loads(page)

#	xchat.command('say ' + parseJsonResult(result))
#	return xchat.EAT_ALL

#xchat.hook_command("tt", translateTo, help="/tt <target language> <message> translates message into the language specified and sends it as a /say command.")

def unload_translator(userdata):
	WorkerController.TranslatorThread.kill = true
	WorkerController.addJob(None)
	print 'Translator is unloaded'

xchat.host_unload(unload_translator)

# Load successful, print message
print 'Translator script loaded successfully.'
