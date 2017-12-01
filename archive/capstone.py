import time

try:
    import vrep
except:
    print ('--------------------------------------------------------------')
    print ('"vrep.py" could not be imported. This means very probably that')
    print ('either "vrep.py" or the remoteApi library could not be found.')
    print ('Make sure both are in the same folder as this file,')
    print ('or appropriately adjust the file "vrep.py"')
    print ('--------------------------------------------------------------')
    print ('')

import time

def getPosition(name):
    err, handle_cylinder = vrep.simxGetObjectHandle(clientID, name, vrep.simx_opmode_blocking)
    err, pos = vrep.simxGetObjectPosition(clientID, handle_cylinder, -1, vrep.simx_opmode_blocking)
    pos1 = [p * 100 for p in pos] 
    print(name, pos1)
    return pos

def testFunction(name):
    res,retInts,retFloats,retStrings,retBuffer=vrep.simxCallScriptFunction(clientID, name, vrep.sim_scripttype_childscript,
            'testFunction', [], [], ['Anand', 'Saha'], bytearray(), vrep.simx_opmode_blocking)
    print(res)
    print(retInts)
    print(retFloats)
    print(retStrings)
    print(retBuffer)

def computeAnglesFromGripperPositionEx(name, pos, vertical=0, radial=0):

    pos.append(vertical)
    pos.append(radial)
    res,retInts,retFloats,retStrings,retBuffer=vrep.simxCallScriptFunction(clientID, name, vrep.sim_scripttype_childscript,
            'computeAnglesFromGripperPositionEx', [], pos, [], bytearray(), vrep.simx_opmode_blocking)
    print(res)
    print(retInts)
    print(retFloats)
    print(retStrings)
    print(retBuffer)
    return retFloats

def moveToPositionEx(name, pos):
    time.sleep(0.5)
    res,retInts,retFloats,retStrings,retBuffer=vrep.simxCallScriptFunction(clientID, name, vrep.sim_scripttype_childscript,
            'moveToPositionEx', [], pos, [], bytearray(), vrep.simx_opmode_blocking)
    print(res)
    print(retInts)
    print(retFloats)
    print(retStrings)
    print(retBuffer)
    return retFloats


def enableGripperEx(name, enable):
    time.sleep(0.7)
    i_enable = 1
    if not enable:
        i_enable = -1

    res,retInts,retFloats,retStrings,retBuffer=vrep.simxCallScriptFunction(clientID, name, vrep.sim_scripttype_childscript,
            'enableGripperEx', [i_enable], [], [], bytearray(), vrep.simx_opmode_blocking)
    print(res)
    print(retInts)
    print(retFloats)
    print(retStrings)
    print(retBuffer)
    return retFloats


print ('Program started')
vrep.simxFinish(-1) # just in case, close all opened connections
clientID=vrep.simxStart('127.0.0.1',19997,True,True,5000,5) # Connect to V-REP
if clientID!=-1:
    print ('Connected to remote API server')

    # Now try to retrieve data in a blocking fashion (i.e. a service call):
    res,objs=vrep.simxGetObjects(clientID,vrep.sim_handle_all,vrep.simx_opmode_blocking)
    if res==vrep.simx_return_ok:
        print ('Number of objects in the scene: ',len(objs))
    else:
        print ('Remote API function call returned with error code: ',res)

    # Now send some data to V-REP in a non-blocking fashion:
    vrep.simxAddStatusbarMessage(clientID,'Hello V-REP!',vrep.simx_opmode_oneshot)

    ################################################################
    obj = 'uarm'
    cyl = getPosition('uarm_pickupCylinder')
    cyl1 = list(cyl)
    cyl1[2] += (4 * cyl1[2])
    #grip = getPosition('uarmGripper_motor1Method2')
    #cube = getPosition('uarm_cuboid')
    bin_ = getPosition('uarm_bin')
    bin_[2] += (2 * bin_[2])
    #testFunction(obj)
    print(cyl)
    print(cyl1)
    print(bin_)
    i = 0
    while i < 5:
        time.sleep(0.5)
        vrep.simxStartSimulation(clientID, vrep.simx_opmode_oneshot)
        enableGripperEx(obj, False)
        moveToPositionEx(obj, computeAnglesFromGripperPositionEx(obj, cyl))
        enableGripperEx(obj, True)
        moveToPositionEx(obj, computeAnglesFromGripperPositionEx(obj, cyl1))
        moveToPositionEx(obj, computeAnglesFromGripperPositionEx(obj, bin_))
        enableGripperEx(obj, False)
        vrep.simxStopSimulation(clientID, vrep.simx_opmode_oneshot)
        i += 1
        break
    ################################################################

    # Before closing the connection to V-REP, make sure that the last command sent out had time to arrive. You can guarantee this with (for example):
    vrep.simxGetPingTime(clientID)

    # Now close the connection to V-REP:
    vrep.simxFinish(clientID)
else:
    print ('Failed connecting to remote API server')
print ('Program ended')
