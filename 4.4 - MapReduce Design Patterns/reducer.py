#!/usr/bin/env python
<<<<<<< HEAD
import sys
from collections import Counter
from operator import itemgetter

hashtags_count = Counter()
for line in sys.stdin:
    line = line.split(' ')
    hashtags_count[line[0]] += 1

for h in sorted(hashtags_count.items(), key=itemgetter(0)):
    print '%s %s' % (h[0], h[1])
=======

import sys

last_key = None
running_total = 0

for input_line in sys.stdin:
   input_line = input_line.strip()
   this_key, value = input_line.split("\t", 1)
   value = int(value)

   if last_key == this_key:
       running_total += value
   else:
       if last_key:
           print( "%s\t%d" % (last_key, running_total) )
       running_total = value
       last_key = this_key

if last_key == this_key:
   print( "%s\t%d" % (last_key, running_total) )
>>>>>>> zipfian/master
