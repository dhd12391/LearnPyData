"""
Coding Challenge: The Traveling Suitcase

Scenario: 
Travis traveled to Chicago and took
the Clark Street #22 bus up to
Dave's office.

He left his briefcase on the bus!
Try to get it back!

Task 1:
Travis doesn't know the number of the bus he
was riding. Find likely candidates by parsing
the data just downloaded and identifying
vehicles traveling northbound of Dave's office.

Dave's office is located at:

latitude 41.980262
longitude -87.668452

"""

#rt22.xml file is the dataset containing the current buses running along Route 22
u = urllib.urlopen('http://ctabustracker.com/bustime/map/getBusesForRoute.jsp?route=22')
data = u.read()
f = open('rt22.xml', 'wb')
f.write(data)
f.close()

#Searching for northbound buses past the office

from xml.etree.ElementTree import parse

office_latitude = 41.980262
doc = parse('rt22.xml')

for bus in doc.findall('bus'):
    bus_direction = bus.findtext('d')
    if bus_direction.startswith('North'):
        bus_latitude = float(bus.findtext('lat'))
        if bus_latitude > office_latitude: #checking if northbound bus is north of office
            bus_id = bus.findtext('id')
            print(bus_id, bus_latitude) # printing likely candidates