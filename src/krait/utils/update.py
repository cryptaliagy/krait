# -*- coding: utf-8 -*-
import subprocess
import sys
import os

import re


def should_check_update() -> bool:
    return os.environ.get('KRAIT_NO_UPDATE_CHECK', None) is None


def check_for_update() -> str:
    try:
        o = subprocess.check_output([
                sys.executable,
                '-m',
                'pip',
                '--timeout',
                '3',
                '--retries',
                '0',
                'search',
                'krait'
            ], stderr=subprocess.DEVNULL)

        pattern = r'LATEST:\s+(\d+\.\d+(\.\d+)?)'
        m = re.search(pattern, o.decode('utf-8'))
        if m:
            return m.group(1)
    except Exception:
        pass
    return ''
