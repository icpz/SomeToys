from lxml import etree
import socks
import socket
socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 1080)
socket.socket = socks.socksocket
import urllib
import urllib2
import cookielib
import re
import json

header = {
        # 'Connection': 'close',
        # 'Upgrade-Insecure-Requests': '1',
        # 'Origin': 'https://leetcode.com',
        'Host': 'leetcode.com',
        'Referer': 'https://leetcode.com/accounts/login/',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36',
        # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        # 'Accept-Encoding': 'gzip, deflate, sdch, br',
        # 'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4'
        }

saved = {}

def loginProc(opener, url, form):
    return opener.open(urllib2.Request(url, urllib.urlencode(form), header))

def generateOpener(proxy):
    cookiejar = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookiejar)
                                  # , urllib2.ProxyHandler({'socks5': proxy})
                                )
    return opener, cookiejar

def loadConfig():
    with open('cfg/user.ini', 'r') as ifs:
        username = ifs.readline().replace('\n', '')
        password = ifs.readline().replace('\n', '')
        return username, password

opener = None

def main():
    global header
    global opener
    host = 'https://leetcode.com'
    login_url = 'https://leetcode.com/accounts/login/'
    
    username, password = loadConfig()
    opener, cookiejar = generateOpener('127.0.0.1:1080')
    # opener.open(urllib2.Request(host, None, header))
    opener.open(host)
    for item in cookiejar:
        if item.name == 'csrftoken':
            csrftoken = item.value
            break

    formdata = {
            'login': username,
            'password': password,
            'csrfmiddlewaretoken': csrftoken,
            'remember': 'on'
        }
    print formdata
    
    loginProc(opener, login_url, formdata)
    print 'Login success'
    
    i = 1
    url_format = 'https://leetcode.com%s'
    while True:

        header['Referer'] = 'https://leetcode.com/problemset/algorithms/'
        print 'processing %s' % (url_format % ('/submissions/%d' % i))
        response = opener.open(urllib2.Request(
                    url_format % ('/submissions/%d' % i),
                    data = None,
                    headers = header))
        response_body = response.read()
        selector = etree.HTML(response_body)
        ac_urls = selector.xpath("//a[@class='text-danger status-accepted']/@href")
        if len(ac_urls) == 0:
            break
        for url in ac_urls:
            try:
                download_code(opener, url_format % url)
            except IndexError:
                download_code(opener, url_format % url)
                open('error.log', 'a').write(url)
        i += 1
    print 'All Complete'
    loginOut(opener)

def loginOut(opener):
    global header
    header['Referer'] = 'https://leetcode.com/problemset/algorithms/'
    opener.open(urllib2.Request('https://leetcode.com/accounts/logout/', None, header))

def download_code(opener, url):
    global header
    global saved
    header['Referer'] = 'https://leetcode.com/submissions/'
    print 'requiring submittion %s' % url
    response = opener.open(urllib2.Request(
                    url,
                    data = None,
                    headers = header))
    
    selector = etree.HTML(response.read())
    jsonstr = selector.xpath("/html/body/script[10]/text()")[0]
    jsonstr = '{' + jsonstr[jsonstr.find('questionId'): jsonstr.find('editCodeUrl')]
    jsonstr = jsonstr[: len(jsonstr) - jsonstr[::-1].find(',') - 1] + '}'
    
    keys = ["questionId", "sessionId", "getLangDisplay", "submissionCode"]
    # jsonstr = re.sub(r"([^ :{']+)[ ]*: '", r'"\1" : "', jsonstr)
    for key in keys:
        jsonstr = jsonstr.replace(key, '"%s"' % key)
    jsonstr = jsonstr.replace("'", '"')
    # print jsonstr
    page_data = json.loads(jsonstr)
    title = selector.xpath("/html/body/div[1]/div[2]/div/div[1]/h4/a/text()")[0]
    print 'processing %s %s' % (page_data['questionId'], title)
    if saved.has_key(page_data['questionId']):
        print '    which has been saved, pass\n'
        return
    saved[page_data['questionId']] = 1
    filename = '%s_%s' % (page_data['questionId'], title)
    filename = filename.lower().replace(' ', '_')
    with open('output/%s.cpp' % filename, 'w') as ofs:
        ofs.write(page_data['submissionCode'].encode('utf-8'))
        print 'file: %s.cpp wrote.\n' % filename

try:
    main()
except KeyboardInterrupt:
    loginOut(opener)


