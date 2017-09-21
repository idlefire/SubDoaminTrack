# -*- encoding:utf-8 -*-
import requests
import sys


def detect_target(target, Check=False):
    response = {}
    try:
        if target:
            header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:55.0) Gecko/20100101 Firefox/55.0'}
            target = 'http://'+target
            resp = requests.get(target, headers=header)
            if Check:
                print '+ %s is Running.' % (target)
            else:
                response = resp.headers
                response['status_code'] = resp.status_code
                return response
    except (requests.exceptions.InvalidURL) as _:
        pass
    except Exception as _:
        if Check:
            print '- %s is Woring.' % (target)
            sys.exit(1)
