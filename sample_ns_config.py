#!/usr/bin/env python

# THIS FILE SHOULD BE MODIFIED WITH THE CORRECT SETTINGS
# AND PLACED IN YOUR HOME DIRECTORY

netscalers = {
                'default': 'primary',

                'primary':    {
                                 'USERNAME': 'admin',
                                 'PASSWORD': 'test',
                                 'NS_ADDR' : '192.168.1.1',
                                 'groups': {},
                                 'vserver_ignore_list': ('test-ignore',),
                              },

                'secondary':  {
                                 'USERNAME': 'admin',
                                 'PASSWORD': 'test',
                                 'NS_ADDR' : '192.168.1.2',
                                 'groups': {},
                                 'vserver_ignore_list': ('test-ignore',),
                              },

             }
