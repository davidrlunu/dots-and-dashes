#! /usr/bin/python3
# vim: set fileencoding=UTF-8 :
from urllib import request as rq
from urllib.parse import urlparse
import xml.etree.ElementTree as ET

url = urlparse('https://mail.google.com/mail/feed/atom').geturl()
username = 'username'
passwd = '*******'
passwd_mgr = rq.HTTPPasswordMgrWithDefaultRealm()


passwd_mgr.add_password(None, url, username, passwd)

handler = rq.HTTPBasicAuthHandler(passwd_mgr)
opener = rq.build_opener(handler)
rq.install_opener(opener)
doc = opener.open(url)


dom = ET.parse(doc).getroot()

if __name__ == '__main__':
    with open('/tmp/mails', 'w+') as f:
        print(dom[2].text, file=f, flush=True)
        for mess in dom[5:]:
            print(mess[6][0].text.partition(' ')[0].rjust(20),\
                    file=f,\
                    flush=True)

