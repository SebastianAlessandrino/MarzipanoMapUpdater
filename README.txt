PROGRAM NAME:	MarzipanoMapUpdater
DATE (README):	11/02/2022
WRITTEN BY:	Sebastian Alessandrino


PURPOSE:
The 'MarzipanoMapUpdater' application allows the user to specify a Marzipano tour file to be edited or updated as required.
The program will update the files of the chosen tour folder based on the actions/functions selected by the user.
The user can choose to:
	- 'Update Tour':	The specified tour is updated based on a specified 'Image List' and 'Update Tour Folder'
	- 'Update Tour Menu':	The menu of the specified tour (index.html file) is updated based on a given 'Image List' file
	- 'Edit Image Links':	The data of the specified tour corresponding to links between images (data.js file) is edited based on user input.
	- 'Edit Image Info':	The data of the specified tour corresponding to info of certain images (data.js file) is edited based on user input.

Different menus will be provided based on the selected function to facilitate necessary data inputs with some levels of input validation to
ensure that user error does not lead to data corruption and therefore the selected tour not functioning.


PROGRAM PROCEDURE:
For information regarding the operation of the application, see the file: 'UserInfo/USER_GUIDE.txt'

FILES IN PROJECT:
For more detailed information on the files within the project, see the file: 'UserInfo/PROGRAM_INFO.txt'
Note that executable file can be found in subdirectory: MarzipanoMapUpdater/ApplicationFiles/dist/
The files in the project are:
 - MarzipanoMapUpdater.exe (This is a standalone executable file which does not require any of the files below)
 - Hotspot.py
 - InfoHotspot.py
 - LinkHotspots.py
 - LoggingFunctions.py
 - ProjectGUI.py (If running from console, use this script)
 - ProjectGUIFunctions.py
 - UpdateHotspotFunctions.py
 - UpdateMap.py
 - UpdateMapFunctions.py


INPUT DATA:
This section refers to input files or directories used within the application to provide extra clarity.
For a better description of the different input files, see the file: 'UserInfo/INPUT_DATA_INFO.txt'

	NAME		TYPE		NOTES
	-------------------------------------
	Main Tour	Folder		/app-files/ directory with the following: data.js, index.html, index.js, style.css, img/, tiles/, vendor/
					The above files/folders will be produced when exporting from the Marzipano Tool.

	Update Tour	Folder		Same as above, however only data.js and tiles/ are actually required from the update tour folder.


	Image List	Excel File	Must be in the specific style specified in 'INPUT_DATA_INFO.txt' and be of file type '.xlsx' or '.xls'
