# -*- encoding:utf-8 -*-
import requests
import lxml.html
import traceback
import sys
from gevent.queue import PriorityQueue


def through_crt(target, priority, queue):
    print 'Throgh Https Certificate...'
    url = 'https://crt.sh/?Identity=%%.%s' % target
    try:
        header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:55.0) Gecko/20100101 Firefox/55.0'}
        resp = requests.get(url, headers=header)
        if resp.status_code == 200:
            lxml_ent = lxml.html.fromstring(resp.text)
            subdomain_list = lxml_ent.xpath('/html/body/table[2]/tr/td/table/tr/td[4]')
            for subdomian in subdomain_list:
                if '@' not in subdomian.text:
                    priority += 1
                    queue.put((priority, subdomian.text))
        print '+ Load sub names < OK >'
        return {'priority': priority, 'queue':queue}
    except traceback:
        traceback.print_exc()
        sys.exit(1)
