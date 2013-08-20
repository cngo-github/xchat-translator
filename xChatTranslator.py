# -*- coding: utf-8 -*-

__module_name__ = "translator"
__module_version__ = "0.1"
__module_description__ = "Translates from one language to other using Google Translate via YQL."
__module_author__ = "drag, karona75"

import xchat

import json
import urllib2

DEST_LANG = 'en'
AUTOUSER = {}

class translator:
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

def getPage(message, src, dest):
	url = "http://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20google.translate%20where%20q%3D%22" + message + "%22%20and%20target%3D%22" + dest + "%22%20and%20source%3D%22" + src + "%22%3B&format=json&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys&callback="

	headers = { 'User-Agent' : 'Mozilla/5.0' }
	req = urllib2.Request(url, None, headers)
	response = urllib2.urlopen(req)
	return response.read()

def getPageDetectLang(message, dest):
	url = "http://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20google.translate%20where%20q%3D%22" + message + "%22%20and%20target%3D%22" + dest + "%22%3B&format=json&diagnostics=true&env=http%3A%2F%2Fdatatables.org%2Falltables.env&callback="

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

def translateDetectLang(word, word_eol, userdata):	
	destLang = word[1]
	message = word_eol[2]

	uMessage = unicode(message, "utf-8" )
	page = getPageDetectLang(urllib2.quote(message), destLang)
	result = json.loads(page)

	xchat.prnt("Translated: " + parseJsonResult(result))
	return xchat.EAT_ALL

xchat.hook_command("tr", translateDetectLang, help="/tr <target language> <message> translates message into the language specified.  This auto detects the source language.")

def translate(word, word_eol, userdata):
	print "Starting translation"
	
	srcLang = word[1]
	destLang = word[2]
	message = word_eol[3]

	uMessage = unicode(message, "utf-8" )
	page = getPage(urllib2.quote(message), srcLang, destLang)
	result = json.loads(page)

	xchat.prnt("Translated: " + parseJsonResult(result))
	return xchat.EAT_ALL

xchat.hook_command("trm", translate, help="/trm <source language> <target language> <message> translates message into the language specified.")

def translateTo(word, word_eol, userdata):
	destLang = word[1]
	message = word_eol[2]

	uMessage = unicode(message, "utf-8" )
	page = getPageDetectLang(urllib2.quote(message), destLang)
	result = json.loads(page)

	xchat.command('say ' + parseJsonResult(result))
	return xchat.EAT_ALL

xchat.hook_command("tt", translateTo, help="/tt <target language> <message> translates message into the language specified and sends it as a /say command.")
