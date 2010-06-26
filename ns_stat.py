#!/usr/bin/env python

import os, sys, logging
from optparse import OptionParser
# we have config in our home directory, so add that to python path and import it
sys.path.append(os.getenv("HOME"))
import ns_config as config
import NSLib


def main():
    cli_parser = OptionParser("Usage: %prog [OPTIONS]")
    cli_parser.add_option("-l", dest="list_config", action="store_true", help="List available configurations")
    cli_parser.add_option("-s", dest="loadbalancer_conf", default="default", help="Select a loadbalancer")
    cli_parser.add_option("-v", dest="verbose", action="store_true", help="Verbose output (list healthy vservers and all services")
    cli_parser.add_option("-q", dest="vserver_query", default="", help="Query a virtual server and it's services")

    (OPTS, ARGS) = cli_parser.parse_args()

    if OPTS.list_config:
        list_configurations()
    lb_config = OPTS.loadbalancer_conf
    if OPTS.loadbalancer_conf == 'default':
        lb_config = config.netscalers['default']
       

    ns = NSLib.NSStatApi(hostname=config.netscalers[lb_config]['NS_ADDR'], 
                         username=config.netscalers[lb_config]['USERNAME'], 
                         password=config.netscalers[lb_config]['PASSWORD'])
    results = ns.system_health_check()

    print "*" * 50
    print "Health check for loadbalancer: %s" % config.netscalers['primary']['NS_ADDR']
    print ""
    print " Memory usage: %2f%%" % float(results['mem'])
    print "    CPU usage: %s%%" % results['cpu']
    print "  Temperature: %sC" % results['temp']
    print "     Requests: %s/sec" % results['http_req_rate']
    print ""

    ns_c = NSLib.NSConfigApi(hostname=config.netscalers[lb_config]['NS_ADDR'], 
                             username=config.netscalers[lb_config]['USERNAME'], 
                             password=config.netscalers[lb_config]['PASSWORD'])

    # itereate through all vservers on the loadbalancer
    for (vs, data) in ns.get_vservers_list(name=OPTS.vserver_query).iteritems():
        if (data['status'] != 'UP' or data['health'] != 100) and vs not in config.netscalers['primary']['vserver_ignore_list'] or OPTS.verbose:
            print "-" * 30
            print " SERVICE: %s (%s:%s)" % (vs, data['ip'], data['port'])
            print "    LOAD: %s req/s" % data['requestsrate']
            print "  HEALTH: %s%%" % data['health']
            print ""
            for srv in sorted(ns_c.get_services_list(vs)):
                service = ns.get_service_details(srv)
                if service['status'] != 'UP' or OPTS.vserver_query or OPTS.verbose:
                    print ' * %s (%s:%s) - %s (%s req/sec)' % (srv, service['ip'], service['port'], service['status'], service['requestsrate'])
            print ""


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
    sys.exit(0)


if __name__ == '__main__':
    main()
