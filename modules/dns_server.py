# -*- encoding:utf-8 -*-
import dns.resolver
import sys
from gevent.pool import Pool

dns_servers = []


def load_dns_server():
    pool = Pool(20)
    for dns_server in open('dict/dns_server_list.txt').readlines():
        dns_server = dns_server.strip()
        if dns_server:
            pool.apply_async(detect_dns_server, (dns_server,))
    pool.join()
    if len(dns_servers) == 0:
        print 'No available.'
        sys.exit(1)
    print 'Avaiable Dns in total: %d' % (len(dns_servers))
    return dns_servers


def detect_dns_server(dns_server):
    res = dns.resolver.Resolver()
    res.lifetime = res.timeout = 5.0
    try:
        res.nameservers = [dns_server]
        answer = res.query('ip.cn')
        if answer[0].address != '118.184.180.46':
            raise Exception('Error Dns:%s' % dns_server)
        try:
            res.query('bad.bad.python.org')
        except Exception as e:
            dns_servers.append(dns_server)
        print '+ DNS Server %s < OK >' % (dns_server)
    except dns.exception.DNSException:
        print '- DNS Server %s < Fail >' % (dns_server)
