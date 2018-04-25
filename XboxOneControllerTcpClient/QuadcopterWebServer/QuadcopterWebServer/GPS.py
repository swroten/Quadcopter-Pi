# Code for GPS
import gps
import logging
import sys
import time
import os
import serial


class GPS:
    def __init__(self):        
        # Print Statement about connecting to GPS
        print("Connecting to GPS...")
        
        # GPS
        self.session = gps.gps()
        
        # Get Data
        UpdateGPS()
        
    def UpdateGPS(self):
        # Get Data
        self.latitude = self.session.fix.latitude
        self.longitude = self.session.fix.longitude
        self.time = session.utc,' + ',session.fix.time
        self.altitude = self.session.fix.altitude
        self.eps = self.session.fix.eps
        self.epx = self.session.fix.epx
        self.epv = self.session.fix.epv
        self.ept = self.session.fix.ept
        self.speed = self.session.fix.speed
        self.climb = self.session.fix.climb
        self.track = self.session.fix.track
        self.mode = self.session.fix.mode
        self.satellites = self.session.satellites
                
    def PrintGPS(self):        
        print("GPS Reading:")
        print("  latitude:     ", self.session.fix.latitude)
        print("  longitude:    ", session.fix.longitude)
        print("  time utc:     ", session.utc,' + ',session.fix.time)
        print("  altitude (m): ", session.fix.altitude)
        print("  eps:          ", session.fix.eps)
        print("  epx:          ", session.fix.epx)
        print("  epv:          ", session.fix.epv)
        print("  ept:          ", session.fix.ept)
        print("  speed (m/s):  ", session.fix.speed)
        print("  climb:        ", session.fix.climb)
        print("  track:        ", session.fix.track)
        print("  mode:         ", session.fix.mode)
        print("  satellites:   ", session.satellites)
        print()




