#!/usr/local/opt/python@2/bin/python2.7
# EASY-INSTALL-ENTRY-SCRIPT: 'spotinstcli==0.1.2','console_scripts','spotinst-cli'
__requires__ = 'spotinstcli==0.1.2'
import re
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(
        load_entry_point('spotinstcli==0.1.2', 'console_scripts', 'spotinst-cli')()
    )