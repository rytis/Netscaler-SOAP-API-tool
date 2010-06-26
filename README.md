Netscaler SOAP API tool
=======================

This tool uses the SOAP API interface to get the statistics and perform
simple configuration tasks on the Citrix Netscaler load balancer devices.

The application was initially developed as an example for one
of the ["Pro Python System Administration"](http://apress.com/book/view/9781430226055) book chapters.

You can find more information about the application on [the project website](http://www.sysadminpy.com).

Configuration
-------------

The tool uses a python module to get the required configuration such as
the IP addresses of the load balancers and the authentication details.
This python module must be placed in your home directory.

The easiest way to create a configuration is to make a copy of the
`sample_ns_config.py` file by copying and renaming it:

    $ cp sample_ns_config.py ~/ns_config.py

Usage
-----

There are two tools available:

* `ns_stat.py` that present basic status information from a load balancer device
* `ns_conf.py` that allows to perform simple configuration tasks

The status utility accepts the follwing options:

    $ ./ns_stat.py --help
    Usage: ns_stat.py [OPTIONS]
    
    Options:
      -h, --help            show this help message and exit
      -l                    List available configurations
      -s LOADBALANCER_CONF  Select a loadbalancer
      -v                    Verbose output (list healthy vservers and all services
      -q VSERVER_QUERY      Query a virtual server and it's services

The options supported by the configuration tool:

    $ ./ns_conf.py --help
    Usage: ns_conf.py enable|disable [OPTIONS]
    
    Options:
      -h, --help            show this help message and exit
      -l                    List available configurations
      -s LOADBALANCER_CONF  Select a loadbalancer
      --vserver=VSERVER     Name of a virtual server
      --service=SERVICE     Service name
      --group=GROUP         Service group name

For example, you can request a detailed information about any available
individual virtual service:

    $ ./ns_stat.py -q test-web-vserver -v
    **************************************************
    Health check for loadbalancer: 192.168.1.1
    
    Memory usage: 5.812803%
    CPU usage: 0%
    Temperature: 38C
    Requests: 8980/sec
    
    ------------------------------
    SERVICE: test-web-vserver (192.168.2.1:80)
    LOAD: 723 req/s
    HEALTH: 100%
    
    * web-service-1 (192.168.101.1:8080) - UP (162 req/sec)
    * web-service-2 (192.168.101.2:8080) - UP (183 req/sec)
    ...
