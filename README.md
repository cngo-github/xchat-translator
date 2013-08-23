XChat-Translator
================

A translator for xchat using Google Translate via YQL.

This script is based on the script by Young Ng.  The original script can be found at:

	http://code.google.com/p/gtranslatecmd/downloads/detail?name=translator.py

COMMANDS
========
/tr <destination_language_code> <message> - this command will translate the message to the destination_language_code and print the returned translation locally only.

/tt <destination_language_code> <message> - this command will translate the message to the destination_language_code and will send the returned translation to XChat as though the user used /say <translated_message>.

/trm <source_language_code> <destination_language_code> <message> - this command will translate the message to destination_language_code from source_language_code and print it locally.

ASSIGNMENTS:
============
Drag: Threading

NOTE: Tried to implement threading.  However, that resulted in XChat crashing on start.  Still working on it.

TODO:
=====
For version 1.0:
- Add better error handling.
- Add threading to not hang XChat while waiting for a response form the server.
- Add automated translations based on user nicks.
- Add a hook to print out the language codes locally.
- Add better comments to the script.
- Bug fixes.
- Anything else that comes to mind.

Further Development:
- Remove the dependency on YQL.

CHANGE LOG
==========
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
