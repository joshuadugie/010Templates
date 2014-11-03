Rename Package Name
===================

renamepack.py is used to alter the package name of an APK file.
It is able to modify AndroidManifest.xml in binary format.
This code is still ugly, please re-write it and send pull-requests, if you want to use this.

Running
=======

* Unzip AndroidManifest.xml from APK file and place it in the same folder with renamepack.py

* Run the command:
	`python renamepack.py oldpackagename newpackagename
	
* Zip the modified AndroidManifest.xml back to APK file and resign it
 