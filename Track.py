# -*- encoding:utf-8 -*-
import gevent
from gevent import monkey
import time
from gevent.queue import PriorityQueue
import dns.resolver
import dns.exception
import sys
import optparse
import traceback
from modules import load_subdomain_name
from modules import detect_target
from modules import dns_server
monkey.patch_all()


class Track:
    def __init__(self, options, target):
        self.start_time = time.time()
        self.dns_servers = []
        self.options = options
        self.target = target
        self.resolvers = [dns.resolver.Resolver(configure=False) for _ in range(self.options.threads)]
        self.all_dns = dns.resolver.Resolver(configure=False)
        self.all_dns.nameservers = self.dns_servers
        detect_target.detect_target(self.target, True)
        self.dns_servers = dns_server.load_dns_server()
        self.dns_server_count = len(self.dns_servers)
        self.queue = PriorityQueue()
        self.priority = 0
        self.scan_count = self.confirm_count = 0
        self.confirm_subdomain = set()
        self.cdn = ''
        self.load_status = {}
        self.load_status = load_subdomain_name.load_sub_name(self.options, self.target, self.priority, self.queue)
        self.priority = self.load_status['priority']
        self.queue = self.load_status['queue']
        self.print_header_info()
        self.outfile = self.outfile_descriptor()


    def outfile_descriptor(self):
        if self.options.outfile:
            outfile_name = self.options.outfile + '.txt'
        else:
            outfile_name = self.target + '.txt'
        f = open(outfile_name, 'w')
        return f

    def print_header_info(self):
        print 'Domain Name\t\t\t\tIp Adress\t\tStatus\tCDN\tServer'
        print '------------\t\t\t\t----------\t\t------\t------\t---------'

    def subdomain_track(self, serial):
        dns_serial_number = serial % self.dns_server_count
        self.resolvers[serial].nameservers = [self.dns_servers[dns_serial_number]]
        while not self.queue.empty():
            try:
                subdomain_name = self.queue.get(timeout=1)[1]
                msg = '%.1fs | Found %d \r' % (time.time()-self.start_time, self.confirm_count)
                sys.stdout.write(msg)
                sys.stdout.flush()
                self.scan_count += 1
            except traceback:
                traceback.print_exc()
                sys.exit(1)
            try:
                if subdomain_name in self.confirm_subdomain:
                    continue
                if not self.options.crt:
                    subdomian_url = subdomain_name + '.' + self.target
                else:
                    subdomian_url = subdomain_name

                try:
                    dns_responses = self.resolvers[serial].query(subdomian_url)
                except dns.resolver.NoAnswer, e:
                    dns_responses = self.all_dns.query(subdomian_url)

                if len(dns_responses) > 1:
                    self.cdn = 'Yes'
                else:
                    self.cdn = 'Unknown'

                server_responses = detect_target.detect_target(subdomian_url)

                if dns_responses and server_responses:
                    self.confirm_subdomain.add(subdomain_name)
                    self.confirm_count += 1
                    ip = dns_responses[0].address
                    if server_responses.get('Server'):
                        server_info = server_responses['Server']
                    else:
                        server_info = 'Unknown'
                    status_code = server_responses['status_code']
                    print '%s\t\t%s\t\t%s\t%s\t%s' % (subdomian_url.ljust(30), ip, status_code, self.cdn, server_info)

                    msg = '%s\t\t%s\t\t%s\t%s\t%s' % (subdomian_url.ljust(30), ip, status_code, self.cdn, server_info)
                    self.outfile.write(msg)
                    self.outfile.flush()

            except (dns.resolver.NoAnswer, dns.resolver.NoNameservers, dns.exception.Timeout, dns.resolver.NXDOMAIN) as e:
                pass
            except Exception as e:
                traceback.print_exc()
                sys.exit(1)

    def run(self):
        gevent_list = [gevent.spawn(self.subdomain_track, serial) for serial in range(self.options.threads)]

        try:
            gevent.joinall(gevent_list)
        except traceback as _:
            traceback.print_exc()
            sys.exit(1)


if __name__ == '__main__':
    opt = optparse.OptionParser("Usage: %prog [option] domain.com")
    opt.add_option('-t', '--threads', type=int, default=150, dest='threads',
                   help='Num of Scan Threads, Default 150')
    opt.add_option('-f', '--file', default='wordlist.txt', dest='file',
                   help='Scan list of Domain, Please put file in dict floder below, Default wordlist.txt')
    opt.add_option('-c', '--crt', dest='crt', action='store_true',
                   help='Through the Https certificate',)
    opt.add_option('-o', '--outfile', dest='outfile',
                   help='Output a file')
    (option, arg) = opt.parse_args()

    if len(arg) < 1:
        opt.print_help()
        sys.exit(0)

    track = Track(option, arg[0])
    track.run()
