Bugsense-Symbolicater
=====================

Small tool that takes iOS crash logs from BugSense and symbolicates them to human readable error reports.
You should note that you must use the dSYM file that was generated when building the build that is causeing the crashes, otherwise it will not work.

How to use:
- Copy the crash report from BugSense (ensuring you copy the raw text) and paste it in the bugsense.txt file.
- Run the python script, ensure you provide the path to the dSYM file.
- Usage: python Symbolicate.py FILE_DIR
- It will then output the human readable report.

Wherw to get dSYM file:
- Open Xcode and go to the organiser.
- Go to the Archives tab.
- You will be presented with the list of archived builds (provided that you have any).
- Ensure you select the same build that is causing the crashes.
- Right click the build and click "Show in Finder".
- Right click the build and click "Show package contents".
- Go into the "dSYMs" folder. Inside it will be a file called [AppName].app.dSYM.
- Make note of the file path to this file (or just copy it to somewhere that is easier to access).
- You now have the necessary file, you can run the Python script now.

Dependencies:
- Python v2.7.2 or higher
