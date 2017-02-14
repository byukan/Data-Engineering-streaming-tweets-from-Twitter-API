import psycopg2 as pg
import yaml
import os

# load postgres credentials
pgcred = yaml.load(open(os.path.expanduser('~/postgres.yml')))['postgres']
dbname = pgcred['dbname']
user = pgcred['user']
password = pgcred['password']
host = pgcred['host']
port = pgcred['port']

conn = pg.connect(dbname=dbname, user=user, password=password, host=host, port=port)

cur = conn.cursor()
cur.execute('refresh materialized view clean_tweets; refresh materialized view tweets_hashtags;')
cur.close()

cur = conn.cursor()
cur.execute("SELECT * FROM hashtag_frequency LIMIT 10;")
query_result = cur.fetchall()
cur.close()

html_str = '<!DOCTYPE html><html><b>Twitter Top 10</b></br>'
for item in query_result:
        html_str += item[0] + ' ' + str(item[1]) + '</br>'
html_str += '</html>'

with open("twitter_top10.html", "w") as html:
        html.write(html_str.encode('utf-8'))
