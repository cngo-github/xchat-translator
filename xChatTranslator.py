# -*- coding: utf-8 -*-

__module_name__ = "translator"
__module_version__ = "0.8"
__module_description__ = "Translates from one language to others using Google Translate via YQL."
__module_author__ = "Chuong Ngo, karona75"

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
		'ENGLISH (USA)' : 'en-US',
	        'VIETNAMESE' : 'vi',
	        'WELSH' : 'cy',
	        'YIDDISH' : 'yi'
	}

	# Mapping to get the language from the language code
	LANGUAGES_REVERSE = dict([(v,k) for (k,v) in LANGUAGES.iteritems()])

	CODES_SET = set(LANGUAGES.values())

	'''
		Returns the url string to be used to translate the text.
	'''
	def getUrl(cls, message, destLang, sourceLang = None):
		src = cls.findLangCode(sourceLang)
		dest = cls.findLangCode(destLang)

		if src is None and dest is not None:
			# No source language was provided, automatically detect the language
			return "http://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20google.translate%20where%20q%3D%22" + urllib2.quote(message) + "%22%20and%20target%3D%22" + dest + "%22%3B&format=json&diagnostics=true&env=http%3A%2F%2Fdatatables.org%2Falltables.env&callback="
		
		if src is not None and dest is not None:
			# Source language was provided, don't detect the language
			return "http://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20google.translate%20where%20q%3D%22" + urllib2.quote(message) + "%22%20and%20target%3D%22" + dest + "%22%20and%20source%3D%22" + src + "%22%3B&format=json&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys&callback="

		return None
	getUrl = classmethod(getUrl)

	'''
		Checks if the specifed language is in the dict
	'''
	def findLangCode(cls, language):
		if language is None:
			return None

		if language.upper() in cls.LANGUAGES:
			# The language is in the dict LANGUAGES
			return cls.LANGUAGES[language.upper()]

		if language in cls.LANGUAGES_REVERSE:
			# The language code was used.
			return language

		# The language is not in the dict LANGUAGES
		return None
	findLangCode = classmethod(findLangCode)

	'''
		Contacts the translation website via YQL to translate the message.
	'''
	def translate(cls, message, sourceLang, destLang):
		url = cls.getUrl(message, sourceLang, destLang)

		if url is None:
			# The Url could not be created
			LAST_ERROR = "No valid destination/target language specified"
			return (None, None)

		headers = { 'User-Agent' : 'Mozilla/5.0' }
		response = urllib2.urlopen(urllib2.Request(url, None, headers))

		return cls.parseJsonResult(response.read())
	translate = classmethod(translate)

	'''
		Parse the JSON returned from calling YQL to get the translated information.
	'''
	def parseJsonResult(cls, result):
		data = json.loads(result)

		sourceLang = data['query']['lang']
		dataArr = data['query']['results']['json']['json'][0]['json']
		translation = ""

		if type(dataArr) is dict:
			translation += dataArr['json'][0]
		else:
			for subDict in dataArr:
				translation += subDict['json'][0]

		return (cls.LANGUAGES_REVERSE[sourceLang], translation.encode("utf-8"))
	parseJsonResult = classmethod(parseJsonResult)

'''
	Performs the translations in threads so as not to lock up XChat.
'''
class TranslatorThread(Thread):
	def __init__(self, queue):
		threading.Thread.__init__(self, target = self.run)
		self.queue = queue
		self.kill = False;

	def run(self):
		global LAST_ERROR

		while True:
			job = self.queue.get()

			if self.kill or job == None:
				break;
			try:
				context, user, srcLang, destLang, text = job

				lang, translatedText = Translator.translate(text, destLang, srcLang)

				if translatedText.strip().lower() != text.strip().lower():
					context.emit_print("Channel Message", "[%s][%s]" %(user, lang), translatedText)
			except TranslateException, e:
				LAST_ERROR = "[TE: %s] <%s> %s" %(e, user, text)
			except urllib2.URLError, e:
				LAST_ERROR = "[URL] %s" %e
			except UnicodeError, e:
				LAST_ERROR = "[Encode: %s] <%s> %s" %(e, user, text)

'''
	Controls the threads
'''
class ThreadController:
	jobs = Queue.Queue()
	worker = TranslatorThread(jobs)
	worker.setDaemon(True)
	worker.start()

	def addJob(cls, job):
		cls.jobs.put(job)
	addJob = classmethod(addJob)

'''
	Translates the message to the specified language with source language detection
'''
def translateDetectLang(word, word_eol, userdata):	
	destLang = word[1]
	message = unicode(word_eol[2], "utf-8")

	src, text = Translator.translate(word_eol[2], destLang, None)

	if src is None or text is None:
		xchat.prnt("Error occurred during translation.")
	else:
		xchat.command("say " + text)

	return xchat.EAT_ALL

xchat.hook_command("TR", translateDetectLang, help="/TR <target language> <message> - translates message into the language specified.  This auto detects the source language.  This is not threaded.")

'''
	Translates the message to the specified language assuming that the source language is the one specified.
'''
def translateNoDetect(word, word_eol, userdata):
	srcLang = word[1]
	destLang = word[2]
	message = word_eol[3]

	src, text = Translator.translate(word_eol[2], destLang, srcLang)

	if src is None or text is None:
		xchat.prnt("Error occurred during translation.")
	else:
		xchat.prnt("Translated from " + src + " to " + Translator.findLangCode(destLang) + ": " + text)
	return xchat.EAT_ALL

xchat.hook_command("TM", translateNoDetect, help="/TM <source_language> <target_language> <message> - translates message into the language specified.  This is not threaded.")

'''
	Adds a user to the watch list to automatically translate.
'''
def addUser(word, word_eol, userdata):
	if len(word) < 2:
		xchat.prnt("You must specify a user.")
		return xchat.EAT_ALL

	user = word[1]
	dest = DEFAULT_LANG
	src = None

	if len(word) > 2 and Translator.findLangCode(word[2]) is not None:
		dest = word[2]

	if len(word) > 3 and Translator.findLangCode(word[3]) is not None:
		src = word[3]

	AUTOUSER[xchat.get_info('channel') + ' ' + user.lower()] = (dest, src)
	xchat.prnt("Added user %s to the watch list." %user)

	return xchat.EAT_ALL

xchat.hook_command("ADDTR", addUser, help = "/ADDTR <user_nick> <target_language> <source_language> - adds the user to the watch list for automatic translations.  If target_language is not specified, then the DEFAULT_LANG set will be used.  If source_language is not specified, then language detection will be used.")

'''
	Removes a user from the watch list to automatically translate.
'''
def removeUser(word, word_eol, userdata):
	if len(word) < 2:
		xchat.prnt("You must specify a user.")
		return xchat.EAT_ALL

	user = word[1]

	if AUTOUSER.pop(xchat.get_info('channel') + ' ' + user.lower(), None) is not None:
		xchat.prnt("User %s has been removed from the watch list." %user)

	return xchat.EAT_ALL

xchat.hook_command("RMTR", removeUser, help = "/RMTR <user_nick> - removes user_nick from the watch list for automatic translations.")

'''
	Prints automatic translations watch list.
'''
def printWatchList(word, word_eol, userdata):
	users = [ key.split(' ')[1] for key in AUTOUSER.keys()]

	xchat.prnt("WatchList: %s" %(" ".join(users)))
	xchat.EAT_ALL

xchat.hook_command("LSUSERS", printWatchList, help = "/LSUSERS - prints out all users on the watch list for automatic translations to the screen locally.")

'''
	Prints out the last error.
'''
def readError(word, word_eol, userdata):
	xchat.prnt("Last error: " + LAST_ERROR)
xchat.hook_command("LASTERROR", readError, help = "/LASTERROR - prints out the last error message to screen locally.")

'''
	Adds a new translation job to the queue.
'''
def addJob(word, word_eol, userdata):
	channel = xchat.get_info('channel')
	key = channel + " " + word[0].lower()

	if(AUTOUSER.has_key(key)):
		dest, src = AUTOUSER[key]
		ThreadController.addJob((xchat.get_context(), word[0], src, dest, word[1]))

	return xchat.EAT_NONE

xchat.hook_print("Channel Message", addJob)

'''
	Shuts down the threads and thread controller when unloading the module.
'''
def unload_translator(userdata):
	ThreadController.TranslatorThread.kill = True
	ThreadController.addJob(None)
	print 'Translator is unloaded'

xchat.hook_unload(unload_translator)

# Load successful, print message
print 'Translator script loaded successfully.'
