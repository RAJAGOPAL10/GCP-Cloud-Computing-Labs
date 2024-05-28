#!/usr/bin/env python
"""mapper.py"""

import sys
import re
# pattern to check urls in file 
url_pattern = r'href="([^"]*)"'
# input comes from STDIN (standard input)
for line in sys.stdin:
    # remove leading and trailing whitespace
    line = line.strip()
    # find all urls in each line
    line_urls = re.findall(url_pattern, line)
    # more than one url can exist in a line
    for url in line_urls:
        #trivial count is 1
        print('%s\t%s' % (url, 1))