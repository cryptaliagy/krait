# -*- coding: utf-8 -*-
import sys

if __name__ == '__main__':
    type = sys.argv[1]

    mapper = {
        'release candidate': 'rc',
        'alpha': 'a',
        'beta': 'b',
        'dev': 'dev',
        'post': 'post'
    }

    print(mapper[type])
