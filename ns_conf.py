#!/usr/bin/env python

import os, sys, logging
from optparse import OptionParser
# we have config in our home directory, so add that to python path and import it
sys.path.append(os.getenv("HOME"))
import ns_config as config
import NSLib


def main():
    # define cli parser configuration and options
    cli_parser = OptionParser("Usage: %prog enable|disable [OPTIONS]")
    cli_parser.add_option("-l", dest="list_config", action="store_true", help="List available configurations")
    cli_parser.add_option("-s", dest="loadbalancer_conf", default="default", help="Select a loadbalancer")
    cli_parser.add_option("--vserver", dest="vserver", default="", help="Name of a virtual server")
    cli_parser.add_option("--service", dest="service", default="", help="Service name")
    cli_parser.add_option("--group",   dest="group",   default="", help="Service group name")

    (OPTS, ARGS) = cli_parser.parse_args()

    # list configuration
    if OPTS.list_config:
        list_configurations()

    # must specify one argument and it must be recognised
    if not (len(ARGS) == 1 and ARGS[0].lower() in ('enable', 'disable')):
        print "ERROR: You must specify only one argument: 'enable' or 'disable'"
        cli_parser.print_help()
        sys.exit(-1)
    action = ARGS[0].lower()
    
    # must specify at least one (empty parameters will get handled automatically)
    if not (OPTS.vserver or OPTS.service or OPTS.group):
        print "ERROR: You must specify at least one of the following 'vserver', 'service' or 'group'"
        cli_parser.print_help()
        sys.exit(-1)

    # see which lb configuration we're told to use
    lb_config = OPTS.loadbalancer_conf
    if OPTS.loadbalancer_conf == 'default':
        lb_config = config.netscalers['default']

    # initialise SOAP connection object (performs login automatically)
    ns_c = NSLib.NSConfigApi(hostname=config.netscalers[lb_config]['NS_ADDR'],
                             username=config.netscalers[lb_config]['USERNAME'],
                             password=config.netscalers[lb_config]['PASSWORD'])

    # need to build a list of services that we enable or disable
    # source is three options: vserver, service and group
    # start with empty list and add service from each option

    services = []

    # services from vserver: query loadbalancer and retrieve list of services
    if OPTS.vserver:
        # we accept comma separated lists as well
        for vs in OPTS.vserver.split(','):
            services += ns_c.get_services_list(vs)

    # services from service: very simple, just add them
    if OPTS.service:
        services += OPTS.service.split(',')

    # services from group: add group list to them
    if OPTS.group:
        for gr in OPTS.group.split(','):
            services += config.netscalers[lb_config]['groups'][gr]

    print '*** the following services will be %sD:' % action.upper()
    for s in services:
        print '- %s' % s

    confirm = raw_input('Do you want to proceed? (yes|no) ')
    if confirm.upper() != 'YES':
        print 'Terminated...'
        sys.exit(-1)

    ns_c.set_service_state(action, services, verbose=True)



def list_configurations():
    for c in config.netscalers:
        if c != 'default':
            print '-' * 30
            print c
            if c == config.netscalers['default']:
                print "(default)"
            print ""
            print " ADDRESS: %s" % config.netscalers[c]['NS_ADDR']
            print "USERNAME: %s" % config.netscalers[c]['USERNAME']
            print ""
            if 'vserver_ignore_list' in config.netscalers[c]:
                print 'Virtual servers that will be ignored when checking for errors:'
                for vs in config.netscalers[c]['vserver_ignore_list']:
                    print "  %s" % vs
            if 'groups' in config.netscalers[c]:
                print 'Following service groups are defined:'
                for (grp_name, list) in config.netscalers[c]['groups'].iteritems():
                    print '   %s: %s' % (grp_name, repr(list))
    sys.exit(0)


if __name__ == '__main__':
    main()
