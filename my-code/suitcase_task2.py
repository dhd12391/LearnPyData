"""
Task 2:

Write a program that periodically monitors
the identified buses and reports their current
distance from Dave's office.

When the bus gets closer than 0.5 miles, have
the program issue an alert by popping up a
web-page showing the bus location on a map.
Travis will meet the bus and get his suitcase.

"""
#NOTE: building on top of task 1

#rt22.xml file is the dataset containing the current buses running along Route 22

#Searching for northbound buses past the office

import urllib
from xml.etree.ElementTree import parse
import time
import webbrowser

office_latitude = 41.980262

def update_rt22_file():
    u = urllib.urlopen('http://ctabustracker.com/bustime/map/getBusesForRoute.jsp?route=22')
    data = u.read()
    f = open('rt22.xml', 'wb')
    f.write(data)
    f.close()

def initial_check():
    buses = [] #list of bus_ids of likely candidates
    update_rt22_file()
    doc = parse('rt22.xml')

    for bus in doc.findall('bus'):
        bus_direction = bus.findtext('d')
        if bus_direction.startswith('North'):
            bus_latitude = float(bus.findtext('lat'))
            if bus_latitude > office_latitude: #checking if northbound bus is north of office
                bus_id = bus.findtext('id')
                buses.append(bus_id) #append likely candidates
    return buses

def distance(office_latitude, bus_latitude):
    return 69 * abs(office_latitude - bus_latitude) #approximation [miles] between the two latitudes
    
#this function tracks the buses that were recorded in the list of buses during initial check
def track_buses(candidates):
    update_rt22_file()
    doc = parse('rt22.xml')
    for bus in doc.findall('bus'):
        bus_id = bus.findtext('id')
        if bus_id in candidates:
            bus_latitude = float(bus.findtext('lat'))
            bus_longitutde = float(bus.findtext('lon'))
            bus_direction = bus.findtext('d')
            print bus_id+ ", %f" % (bus_latitude) + " currently moving " + bus_direction 
            if distance(office_latitude, bus_latitude) < 0.5:
                print "Bus #" + bus_id + " is arriving! Go outside and check if your suitcase is there!"
                webbrowser.open('http://maps.googleapis.com/maps/api/staticmap?size=500x500&sensor=false&markers=|%f,%f' % (bus_latitude, bus_longitude))
    
if __name__ == "__main__":
    likely_candidates = initial_check()
    while True:
        track_buses(likely_candidates)
        print #newline
        time.sleep(30)