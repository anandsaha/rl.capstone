Instructions for running this project on Linux
==========================================================================
The solution was developmed with:

Ubuntu 16.04
Python 3.5 (Permissible as mentioned in https://discussions.udacity.com/t/only-python-2-7/227331)
Numpy 1.12.1

Setup the V-REP environment
==========================================================================
1. Download the software from http://coppeliarobotics.com/files/V-REP_PRO_EDU_V3_4_0_Linux.tar.gz to any directory of your choosing.

2. Unzip V-REP software and edit the 'remoteApiConnections.txt' file to contain the following (comment out all other lines):

// Let's start a continuous remote API server service on port 19997:
portIndex1_port             = 19997
portIndex1_debug            = true
portIndex1_syncSimTrigger   = false

3. Invoke vrep.sh from the V-REP directory. This will start the V-REP UI.

4. Go to 'File > Open Scene' and select the 'scene.ttt' file which is provided with my codebase.

This will open the scene which we will use for training.


Starting the learning
==========================================================================

1. To initiate the learning, run:

python3 main.py --train

!!NOTE!!: The first 3 invocations will fail because the fresh installation of V-REP will popup a message saying "This simulation will run with custom simulation parameters". You have to select the checkbox saying "Do not show ..." 3 times for it to go away permanently. Then you can start the real training.

2. Once the above is done, to test the derived q-table, run:

python3 main.py --test

Note
==========================================================================
1. The folder qtables/ contain transient data. If you want to restart the learning from scratch, make sure you delete this directory.

2. You can explore the config.py file for tuning any configurable parameters.



