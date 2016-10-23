# -*- coding: utf-8 -*-

import socket
import cookielib
import urllib
import urllib2


class HttpClient:

    __cookie = cookielib.CookieJar()
    __req = urllib2.build_opener(urllib2.HTTPCookieProcessor(__cookie))
    __req.addheaders = [
        ('Accept', 'application/javascript, */*;q=0.8'),
        ('User-Agent', "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.125 Safari/537.36")
    ]
    urllib2.install_opener(__req)

    def Get(self, url, refer=None):
        try:
            # logging.debug("GET: %s", url)
            req = urllib2.Request(url)
            if not (refer is None):
                req.add_header('Referer', refer)
            return urllib2.urlopen(req).read()
        except urllib2.HTTPError, e:
            return e.read()

    def Post(self, url, data, refer=None):
        try:
            # logging.debug("POST: %s, %s", url, data)
            req = urllib2.Request(url, urllib.urlencode(data))
            if not (refer is None):
                req.add_header('Referer', refer)
            return urllib2.urlopen(req, timeout=180).read()
        except urllib2.HTTPError, e:
            return e.read()
        except socket.timeout:
            return ''
        except socket.error:
            return ''

    def Download(self, url, file):
        output = open(file, 'wb')
        output.write(urllib2.urlopen(url).read())
        output.close()

    def getCookie(self, key):
        for c in self.__cookie:
            if c.name == key:
                return c.value
        return ''

    def setCookie(self, key, val, domain):
        ck = cookielib.Cookie(version=0, name=key, value=val, port=None, port_specified=False, domain=domain, domain_specified=False, domain_initial_dot=False, path='/', path_specified=True, secure=False, expires=None, discard=True, comment=None, comment_url=None, rest={'HttpOnly': None}, rfc2109=False)
        self.__cookie.set_cookie(ck)


if __name__ == "__main__":
    c = HttpClient()
    # print c.Get('http://www.baidu.com')

    c.Post('http://dl.web2.qq.com/channel/poll2', {})
    # {'r': '{"ptwebqq":"b42c4a5b1248079708dd62759de28018d4ee4665244b6c6ceecd8a3e85b81e2b","clientid":53999199,"psessionid":"8368046764001d636f6e6e7365727665725f77656271714031302e3133332e34312e383400001ad00000066b026e040015808a206d0000000a406172314338344a69526d0000002859185d94e66218548d1ecb1a12513c86126b3afb97a3c2955b1070324790733ddb059ab166de6857","key":""}'})
