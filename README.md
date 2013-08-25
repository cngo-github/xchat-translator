XChat-Translator
================

A translator for xchat using Google Translate via YQL.

This script is based on the script by Young Ng.  The original script can be found at:

	http://code.google.com/p/gtranslatecmd/downloads/detail?name=translator.py

By default, the script translates everything to English (en) unless otherwise specified.  This can be changed by changing the language code for DEFAULT_LANG on line 16.

COMMANDS
========
/TR target_language message - translates message into the language specified.  This auto detects the source language.  This is not threaded.

/TM source_language target_language message - translates message into the language specified.  This is not threaded.

/ADDTR user_nick target_language source_language - adds the user to the watch list for automatic translations.  If target_language is not specified, then the DEFAULT_LANG value will be used.  If source_language is not specified, then language detection will be used.

/RMTR user_nick - removes user_nick from the watch list for automatic translations.

/LSUSERS - prints out all users on the watch list for automatic translations to the screen locally.

/LASTERROR - prints out the last error message to screen locally.

ASSIGNMENTS:
============


BUGS:
=====
- If the message has the usernick of the person using the script, automatic translations won't run.  This must be due to the XChat event being different.
- All detected languages seems to be en_US.  This need to be corrected.  The translations are correct, however, en_US is printed to the screen as the source language even when it is not.

TODO:
=====
For version 1.0:
- Add better error handling.
- Add automated translations based on user nicks. - Incoming messages done
- Add a hook to print out the language codes locally.
- Add better comments to the script.
- Bug fixes.
	- Trigger auto translations even when the user's nick is used in a message.
	- Verify the returned detected language.
- Anything else that comes to mind.

= DONE =
- Add threading to not hang XChat while waiting for a response from the server.

Further Development:
- Remove the dependency on YQL.

CHANGE LOG
==========
v0.9
- Added context menu to Add/Remove user from AutoTranslate list [briand]

v0.8
- Added threading and automatic translations for incoming messages based on usernicks.
- Rewired /TR to run through the Translator class and it now sends a message to the channel.
- Renamed /trm to /TM.  /TM now runs through the Translator class as well and will print locally.
- Removed /TRT
- Added /ADDTR to add a usernick to the watch list for automatic translations.
- Added /RMTR to remove a usernick from the watch list.
- Added /LSUSERS to print all usernicks currently on the watch list.
- Added /LASTERROR to print the last error encountered in translations.
- The program can now accept both language codes and the language names (i.e. fr and French).
- Added some error handling.
- Added comments
- Cleaned up code
- Found 2 bugs:
	- If the message has the usernick of the person using the script, automatic translations won't run.  This must be due to the XChat event being different.
	- All detected languages seems to be en_US.  This need to be corrected.

v0.6
- Added automated language detection using google translate.
- Rewired /tr to use the new translation with automated language detection.
- Renamed /trt to /tt and rewired it to use the translation with automated language detection.
- Created /trm which uses the old translation without language detection.
- Removed /trf as a command.

v0.3
- successfully demonstrated translation without language detection.
- Added xchat hooks: /tr, /trt, and /trf

LICENSE
=======
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
