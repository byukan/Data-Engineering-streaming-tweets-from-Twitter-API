#import dependencies
import os
import yaml
import twitter
import pandas as pd
import datetime

import smtplib
import email.utils
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def get_top_trends(WOEID, n_results):
    creds_path = os.path.join(os.path.expanduser("~"), 'api_creds.yml')
    credentials = yaml.load(open(creds_path))

    #Connect to Twitter API
    t = twitter.Api(
        credentials['twitter'].get('consumer_key'),
        credentials['twitter'].get('consumer_secret'),\
        credentials['twitter'].get('token'),\
        credentials['twitter'].get('token_secret'))

    #Get top topics in a particular region(Yahoo WOEID)
    top_topics = t.GetTrendsCurrent(WOEID)
    #Convert list of tuples to list of dicts
    top_n_topics = [t.AsDict() for t in top_topics[:n_results]]

    #Create a pandas dataframe
    df = pd.DataFrame.from_dict(top_n_topics, orient='columns')

    #Convert to HTML
    df_html = df.to_html()

    #get timestamp string
    timestamp = str('Timestamp: {:%Y-%m-%d %H:%M:%S}'.format(datetime.d$

   #Draft an html string
    html_string = '''
        <html>
            <head>
                <link rel="stylesheet"
        href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.1/css/boots$
                <style>body{ margin:0 100; background:whitesmoke; }</st$
                <meta charset="utf-8">
            </head>
            <body>
                <h1>Top 10 Topics on Twitter</h1>''' + df_html + '''

                <p>{}</p>
            </body>
        <html>
        '''.format(timestamp)

    #Write/update index.html
    index_html = open("index.html","wb")
    index_html.write(html_string.encode("utf-8"))
    index_html.close()

def email_report(sender, recipient):
    # Create message container - the correct MIME type is multipart/alt$
    # Create message container - the correct MIME type is multipart/alt$
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Twitter Trends"
    msg['From'] = email.utils.formataddr(('Anthony', sender))
    msg['To'] = email.utils.formataddr(('Alessandro', recipient))

    index_html = open('index.html','r')
    report = index_html.read()
    index_html.close()
    msg.attach(MIMEText(report, 'html'))

    # Send the message via local SMTP server.
    server = smtplib.SMTP('localhost')

    text = msg.as_string()
    server.sendmail(sender, recipient, text)
    server.quit()


if __name__ == '__main__':
    sender = 'student.Abercrombie@galvanize.it'
    #recipient = 'alessandro+homework@galvanize.it'
    recipient = 'alessandro+homework@galvanize.it'
    get_top_trends(2458833, 10)
    email_report(sender, recipient)
