#!/usr/bin/python

from __future__ import absolute_import, print_function, unicode_literals

from gi.repository import GObject

import dbus
import dbus.mainloop.glib
from optparse import OptionParser, make_option
import bluezutils

compact = False
devices = {}

def print_compact(address, properties):
	name = ""
	address = "<unknown>"

	for key, value in properties.items():
		if type(value) is dbus.String:
			value = unicode(value).encode('ascii', 'replace')
		if (key == "Name"):
			name = value
		elif (key == "Address"):
			address = value

	if "Logged" in properties:
		flag = "*"
	else:
		flag = " "

	print("%s%s %s" % (flag, address, name))

	properties["Logged"] = True

def print_normal(address, properties):
	print("[ " + address + " ]")

	for key in properties.keys():
		value = properties[key]
		if type(value) is dbus.String:
			value = str(value).encode('ascii', 'replace')
		if (key == "Class"):
			print("    %s = 0x%06x" % (key, value))
		else:
			print("    %s = %s" % (key, value))

	print()

	properties["Logged"] = True

def skip_dev(old_dev, new_dev):
	if not "Logged" in old_dev:
		return False
	if "Name" in old_dev:
		return True
	if not "Name" in new_dev:
		return True
	return False

def interfaces_added(path, interfaces):
	properties = interfaces["org.bluez.Device1"]
	if not properties:
		return

	if path in devices:
		dev = devices[path]

		if compact and skip_dev(dev, properties):
			return
		devices[path] = dict(devices[path].items() + properties.items())
	else:
		devices[path] = properties

	if "Address" in devices[path]:
		address = properties["Address"]
	else:
		address = "<unknown>"

	if compact:
		print_compact(address, devices[path])
	else:
		print_normal(address, devices[path])

def properties_changed(interface, changed, invalidated, path):
	if interface != "org.bluez.Device1":
		return

	if path in devices:
		dev = devices[path]

		if compact and skip_dev(dev, changed):
			return
		devices[path] = dict(list(devices[path].items()) + list(changed.items()))
	else:
		devices[path] = changed

	if "Address" in devices[path]:
		address = devices[path]["Address"]
	else:
		address = "<unknown>"

	if compact:
		print_compact(address, devices[path])
	else:
		print_normal(address, devices[path])

def property_changed(name, value):
	if (name == "Discovering" and not value):
		mainloop.quit()

if __name__ == '__main__':
	dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

	bus = dbus.SystemBus()

	option_list = [
			make_option("-i", "--device", action="store",
					type="string", dest="dev_id"),
			make_option("-c", "--compact",
					action="store_true", dest="compact"),
			]
	parser = OptionParser(option_list=option_list)

	(options, args) = parser.parse_args()

	adapter = bluezutils.find_adapter(options.dev_id)

	if options.compact:
		compact = True

	bus.add_signal_receiver(interfaces_added,
			dbus_interface = "org.freedesktop.DBus.ObjectManager",
			signal_name = "InterfacesAdded")

	bus.add_signal_receiver(properties_changed,
			dbus_interface = "org.freedesktop.DBus.Properties",
			signal_name = "PropertiesChanged",
			arg0 = "org.bluez.Device1",
			path_keyword = "path")

	bus.add_signal_receiver(property_changed,
					dbus_interface = "org.bluez.Adapter1",
					signal_name = "PropertyChanged")

	om = dbus.Interface(bus.get_object("org.bluez", "/"),
				"org.freedesktop.DBus.ObjectManager")
	objects = om.GetManagedObjects()
	for path, interfaces in objects.items():
		if "org.bluez.Device1" in interfaces:
			devices[path] = interfaces["org.bluez.Device1"]

	adapter.StartDiscovery()

	mainloop = GObject.MainLoop()
	mainloop.run()
