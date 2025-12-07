# EE250 Project
# Victor Gutierrez, Angie Vasquez

# NOTE: All content relating to the ML model used in this project came from the following repository from user SHAIK-AFSANA:
# https://github.com/SHAIK-AFSANA/facialemotionrecognizerinrealtime

## Requirements
For all nodes:
* Python
* paho-mqtt
* moquitto-clients

For studier:
* TensorFlow
* Keras
* OpenCV
* Pandas
* Numpy
* Seaborn
* Matplotlib

For monitor:
* Tkinter

For action device:
* RPi.GPIO


# Files related to ML model:
* haarcascade_frontalface_default.xml
* real-time-facial-emotion-classification-cnn-using-keras.ipynb
* model.h5
# Note: the xml file and the model.h5 file are necessary for running the studier python file. The python notebook is primarily for reference or for retraining the model if desired

# Execution
The studier node should run "studier.py"
The monitor node should run "monitor.py"
The action device node should run "action_device.py"

The action device should be started before the monitor to ensure that action requests are fulfilled.
These studier and monitor nodes can be activated in any order, but the session statistics for the monitor will only begin recording after the monitor starts its code. Any emotions exhibited by the studier before the monitor starts their code will not be recorded/displayed.


