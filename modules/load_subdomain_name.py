# -*- encoding:utf-8 -*-
import os
import sys
from through_crt import *



def load_sub_name(options, target, priority, queue):
    if options.crt:
        return through_crt(target, priority, queue)
    else:
        if options.file != 'wordlist.txt':
            file_path = 'dict/'+options.file
            if os.path.exists(file_path):
                file_name = file_path
            else:
                file_name = 'dict/wordlist.txt'
        else:
            file_name = 'dict/wordlist.txt'

        with open(file_name) as f:
            for i in f:
                sub = i.strip()
                priority += 1
                try:
                    queue.put((priority, sub))
                except Exception as e:
                    print '- Load sub names < Fail >'
                    sys.exit(1)
        print '+ Load sub names < OK >'
        return {'priority': priority, 'queue': queue}
