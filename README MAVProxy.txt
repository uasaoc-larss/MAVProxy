-----------------------------
---How to use MAVProxy---
--Written by Mark Palframan--
-----Last Edit: 8/8/2013-----
-----------------------------

Note: Unless set up specially, all waypoint files to be used with MaVProxy must be located in the same folder as MAVProxy
======================================Newly added commands=======================================

-wp
    -4Dset
	Usage is "wp 4Dset <wpindex> <time>"
	This command will send the UAS to arrive at wpindex after the time provided (in seconds).
	A "COMMAND_YAW" (115) must be placed at the end of the waypoint file as a marker.
	-----------------------------------------------------------------------------------------
	To accomplish this, waypoints are downloaded, edited, and reuploaded to the APM.
	The "wp update" command is not used, so this command will work with MAVlink 0.9
	All waypoints after the COMMAND_YAW will be deleted and replaced with new waypoints.
	Time intervals of more than 255 seconds will be split into multiple waypoints.
	The TRIM_ARSPD_CM parameter is used to guage whether or not the supplied time is reasonable.
	If the time provided is excessive, a 4 waypoint "loiter path" is automatically generated.
	An initial waypoint is placed directly in the aircraft's path in order to trigger 4D waypoints to turn on.
    -validate
	Usage is "wp validate <filename>"
	Validates that the waypoints currently loaded on the APM match those in a waypoint file.
	----------------------------------------------------------------------------------------
	Reports which waypoints, if any, were not loaded properly.
	Attempts to repair the broken way   
    -closest
	Usage "wp closest <filename>"
	Uploads the provided waypoint pattern and sets the APM's current wp to the optimal wp
	----------------------------------------------------------------------------------------
	The optimal waypoint is determined through proximity, current direction of travel, of waypoint pattern direction

-kill
    -Sets servo positions such that the plane will crash

-print
    -Outputs some text for debugging and testing MAVProxy

======================================Other useful commands=======================================

-wp
    -list
	prints out the waypoints as downloaded from the APM
    -update
	Usage "wp update <filename> <wpnum>"
	Uploads a specific waypoint to the APM
	-----------------------------------------
	This command does not work with MAV 0.9!
    -load
	Usage "wp load <filename>"
	Uploads a wp file to the APM
	-----------------------------
	This works significantly better than some versions of Mission Planner!
    -save
	Usage "wp save <filename>"
	Saves a wp file from the APM to the computer
    -set
	Usage "wp set <wpnum>"
	Sets the APM's current waypoint
    -clear
	Clears all wps currently on the APM

-fence
    -list
	prints out the geofence points as downloaded from the APM
    -load
	Usage "fence load <filename>"
	Uploads a geofence file to the APM
    -save
	Usage "fence save <filename>"
	Saves a geofence file from the APM to the computer
    -clear
	Clears all geofence points currently on the APM

------------Mode Settings------------

-auto
    -Sets APM in auto mode

-manual
    -sets APM in manual mode

-rtl
    -sets APM in return to launch

-loiter
    -sets mode to loiter

-fbwa
    -sets mode to fly by wire A

-----------Setup Commands------------

-reboot
    -reboots APM

-accelcal
    -Does a 3D accelerometer calibration

-level
    -Set's the current APM position as level