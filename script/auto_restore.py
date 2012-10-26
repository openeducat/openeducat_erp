#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xmlrpclib
import time

from ConfigParser import ConfigParser

print "Srcipt Starts",time.strftime("%Y-%m-%d %H:%M:%S")
config = ConfigParser()
config.read('config.conf')
mapping = dict(config.items('openerp'))
print "FFFFFFFFFFFFFF",mapping
sock = xmlrpclib.ServerProxy(mapping['url'])
sock.drop(mapping['admin_password'],mapping['db'])
print "DROP"
sock.create_database(mapping['admin_password'], mapping['db'], True, 'en_US', mapping['new_password'])
print "CREATE"
sock = xmlrpclib.ServerProxy(mapping['url'].replace("db","object"))
print sock

module_ids = sock.execute(mapping['db'], 1, mapping['new_password'], 'ir.module.module', 'search', [('name','=',mapping['module_name'])])
print "$$$$$$$$$$$",module_ids
sock.execute(mapping['db'], 1, mapping['new_password'], 'ir.module.module', 'button_immediate_install', module_ids,)
print "Script Ends",time.strftime("%Y-%m-%d %H:%M:%S")
