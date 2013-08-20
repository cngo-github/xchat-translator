XChat-Translator
================

A translator for xchat using Google Translate via YQL.

This script is based on the original script by Young Ng.  Many thanks to him for his work.  The original script can be found at:

	http://code.google.com/p/gtranslatecmd/downloads/detail?name=translator.py

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

COMMANDS
========
/tr <destination_language_code> <message> - this command will translate the message to the destination_language_code and print the returned translation locally only.

/tt <destination_language_code> <message> - this command will translate the message to the destination_language_code and will send the returned translation to XChat as though the user used /say <translated_message>.

/trm <source_language_code> <destination_language_code> <message> - this command will translate the message to destination_language_code from source_language_code and print it locally.


TODO:
=====
- Add better error handling.
- Add automated translations based on user nicks.
- Remove the dependency on YQL.
- Add a hook to print out the language codes locally.
- Add better comments to the script.
- Bug fixes.
- Anything else that comes to mind.

CHANGE LOG
==========
v0.6
- Added automated language detection using google translate.
- Rewired /tr to use the new translation with automated language detection.
- Renamed /trt to /tt and rewired it to use the translation with automated language detection.
- Created /trm which uses the old translation without language detection.

v0.3
- successfully demonstrated translation without language detection.
- Added xchat hooks: /tr, /trt, and /trf
