"""
A simple example of using the wmr_cba CBA4 python library.

For more information about the wmr_cba package, drivers and documentation, see
the GitHub repo at:
https://github.com/da66en/python_wmr_cba

Will connect to first available CBA4, draw 150mA for 10 seconds and then stop.
While it is drawing current it will print voltage/current status on the console
every second.

The CBA will not draw power if there is no voltage connected to it.  So if
you do not have voltage connected to it this is the reason why the feedback 
result will show 0 Amps even if you requested it to draw current.

Windows users:
If there is an error finding the CBA drivers, you have some options.  If you
are using the libusb/WinUSB drivers (the .inf file provided in the GitHub repo)
then you either need to install libusb so that the drivers can be found in the
global search path, or place libusb-1.0.dll (from libusb) into the same 
directory as the script.  If you are using the drivers provided by West
Mountain Radio, then place mpusbapi.dll into the same directory as the 
Python script.
"""
import sys
sys.path.append("..")

from wmr_cba import wmr_cbacc
import time

def cbacc_example():
    def show_status():
        disp = " Feedback=" + str(cbacc.get_measured_current()) + "A"
        disp += " Running=" + str(cbacc.is_running())
        print(disp)
        #end show_status()

    test = wmr_cbacc.CBACC.test()
    if test:
        print("Test ERROR: " + test)
    else:
        print("Test OK")

    devices = wmr_cbacc.CBACC.scan()
    print("Found "+str(len(devices))+" devices.")

    cbacc = wmr_cbacc.CBACC()

    if not cbacc.is_valid():
        print("ERROR!  Couldn't open a device!")
        exit(-1)
    
    print("Opened CBACC, serial #" + str(cbacc.get_serial_number()))

    show_status()

    print("Charging started")

    cbacc.charge_start()

    reads = 10
    while reads:
        time.sleep(1)
        show_status()
        reads -= 1
    
    cbacc.charge_stop()
    print("Stopped test")

    reads = 5
    while reads:
        time.sleep(1)
        show_status()
        reads -= 1

    cbacc.close()

    print("Done")
    #end __test_cbacc

if __name__ == "__main__":
    print("running ex_wmr_cbacc.py")

    cbacc_example()
