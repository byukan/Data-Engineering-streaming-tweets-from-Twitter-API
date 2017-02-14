
# coding: utf-8

# In[3]:

from boto.s3.connection import S3Connection
from boto.s3.key import Key

conn = S3Connection()


# In[5]:

# Get the bucket.
# Warning: This will fail if your bucket name has a period in it.
# Keep reading to see how to fix it.

# website_bucket = conn.create_bucket('dsci.web')


# In[6]:

# This failed because our bucket name has a period in it.
# Here is the workaround for this bug.

import ssl
if hasattr(ssl, '_create_unverified_context'):
    ssl._create_default_https_context = ssl._create_unverified_context


# In[8]:

# Now lets try to get the bucket again.

website_bucket = conn.create_bucket('shakespeare.sonnets.web')


# In[9]:

website_bucket.set_policy('''{
  "Version":"2012-10-17",
  "Statement": [{
    "Sid": "Allow Public Access to All Objects",
    "Effect": "Allow",
    "Principal": "*",
    "Action": "s3:GetObject",
    "Resource": "arn:aws:s3:::%s/*"
  }
 ]
}''' % website_bucket.name)


# In[10]:

index_html = '''<!DOCTYPE html>
<html>
  <body>
    <p>Hello, World!</p>
  </body>
</html>
'''


# In[11]:

index_key = website_bucket.new_key('index.html')
index_key.content_type = 'text/html'
index_key.set_contents_from_string(index_html, policy='public-read')


# In[12]:

error_html = '''<!DOCTYPE html>
<html>
  <body>
    <p>This is an error page.</p>
  </body>
</html>
'''


# In[13]:

error_key = website_bucket.new_key('error.html')
error_key.content_type = 'text/html'
error_key.set_contents_from_string(error_html, policy='public-read')


# In[14]:

website_bucket.configure_website('index.html', 'error.html')


# ---

# In[16]:

from boto.s3.connection import S3Connection
from boto.s3.key import Key

conn = S3Connection()


# In[17]:

get_ipython().system(u'curl -o shakespeare-sonnets.txt http://www.gutenberg.org/cache/epub/1041/pg1041.txt')


# In[20]:

website_bucket = conn.get_bucket('shakespeare.sonnets.web')


# In[21]:

k = website_bucket.new_key('shakespeare-sonnets.txt')
k.set_contents_from_filename('shakespeare-sonnets.txt')


# In[22]:

sonnets = website_bucket.get_key('shakespeare-sonnets.txt')
text = sonnets.get_contents_as_string()

for line in text.split('\n')[:10]:
    print line


# In[23]:

text.lower().split()[:10]


# In[24]:

from collections import Counter


# In[25]:

wc = Counter(text.lower().split())


# In[26]:

import pandas as pd


# In[27]:

wc_frame = pd.DataFrame(wc.most_common(20))


# In[28]:

wc_frame.index = wc_frame.index + 1


# In[29]:

output_file = website_bucket.new_key('shakespeare-word-freq.txt')
output_file.content_type = 'text'
output_file.set_contents_from_string(wc_frame.to_string(), policy='public-read')


# [dsci.web/shakespeare-word-freq.txt](http://dsci.web.s3-website-us-east-1.amazonaws.com/shakespeare-word-freq.txt)

# In[ ]:
