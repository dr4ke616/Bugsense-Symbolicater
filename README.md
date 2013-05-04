Bugsense-Symbolicater
=====================

Small tool that takes iOS crash logs from BugSense and symbolicates them to human readable error reports.
You should note that you must use the dSYM file that was generated when building the build that is causeing the crashes, otherwise it will not work.

How to use:
	1. Copy the crash report from BugSense (ensuring you copy the raw text) and paste it in the bugsense.txt file.
	2. Run the python script, ensure you provide the path to the dSYM file.
	3. It will then output the human readable report.

Wherw to get dSYM file:
	1. Open Xcode and go to the organiser.
	2. Go to the Archives tab.
	3. You will be presented with the list of archived builds (provided that you have any).
	4. Ensure you select the same build that is causing the crashes.
	5. Right click the build and click "Show in Finder".
	6. Right click the build and click "Show package contents".
	7. Go into the "dSYMs". Inside it will be a file called <AppName>.app.dSYM.
	8. Make note of the file path to this file (or just copy it to somewhere that is easier to access).
	9. You now have the necessary file, you can run the Python script now.

Dependencies:
	Python v2.7.2 or higher