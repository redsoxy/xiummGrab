import urllib.request
import urllib.response
import http.cookiejar
import http.cookies
import datetime
import re
import os
import threading


def getUrlOpener():
    expiration = datetime.datetime.now() + datetime.timedelta(days=30)
    cookies = http.cookies.SimpleCookie()
    cookies["_ga"] = "GA1.2.1175941441.1524069802"
    cookies["_gat"] = "1"
    cookies["_gid"] = "GA1.2.1369455583.1524069802"
    cookies["seeAll"] = "undefined"
    cookies["vipDate"] = "2018-7-24"
    cookies["xmmvip2"] = "fight5"
    cookie_item = None
    for c in cookies:
        cookie_item = http.cookiejar.Cookie(version=0,
                                            name=c,
                                            value = expiration.strftime("%a, %d-%b-%Y %H:%M:%S PST"),
                                            port= None,
                                            port_specified = None,
                                            domain = ".xiumeim.com",
                                            domain_specified = None,
                                            domain_initial_dot=None,
                                            path=".xiumeim.com",
                                            path_specified=None,
                                            secure=None,
                                            expires=None,
                                            discard=None,
                                            comment=None,
                                            comment_url=None,
                                            rest=None,
                                            rfc2109=False)
    cookie_jar = http.cookiejar.CookieJar()
    cookie_jar.set_cookie(cookie_item)
    handler = urllib.request.HTTPCookieProcessor(cookie_jar)
    opener = urllib.request.build_opener(handler)
    urllib.request._opener = opener
    return opener


def getPage(pageNo):
    url = "http://www.xiumeim.com/albums/page-%s.html"%pageNo
    request = urllib.request.Request(url)
    response = opener.open(request)
    return str(response.read().decode())


def downloadAlbumJPG(page, index, albumUrl):
    savepath = "d:\\catch\\page_%s"%page
    if not os.path.exists(savepath):
        os.mkdir(savepath)

    savepath2 = savepath + "\\%s"%index
    if not os.path.exists(savepath2):
        os.mkdir(savepath2)

    urllib.request.urlretrieve(albumUrl, "%s\\album.jpg"%savepath2)


def getReallyPhotoMainPage(url):
    request = urllib.request.Request(url)
    response = opener.open(request)
    return str(response.read().decode())


def downloadOnePagePhoto(path, html, url):
    groups = patten2.findall(html)
    for g in groups:
        urllib.request.urlretrieve(g[0], "%s\\%s.jpg" %(path, g[1]))


def downloadAllPhotos(pageNo, modelindx, modelPhotoUrl):
    #1.获取每页的详情
    html = getReallyPhotoMainPage(modelPhotoUrl)
    groups = patten1.findall(html)
    totalPage = groups[0]  #总页数

    path = "d:\\catch\\page_%s\\%s"%(pageNo, modelindx)
    #2.下载首页
    downloadOnePagePhoto(path, html, modelPhotoUrl)
    #3.下载其他页
    for page in range(2, int(totalPage)+1):
        nextPageUrl = modelPhotoUrl.replace(".html", "-%s.html"%page)
        nexthtml = getReallyPhotoMainPage(nextPageUrl)     #http://www.xiumeim.com/photos/DKGirl-190926-4.html
        downloadOnePagePhoto(path, nexthtml, nextPageUrl)


def main(start, end):
    for pageNo in range(start, end):
        html = getPage(pageNo)
        groups = patten0.findall(html)
        modelindx = 0
        for g in groups:
            modelPhotoUrl = g[0]
            modelAlbumUrl = g[1] + g[2]
            downloadAlbumJPG(pageNo, modelindx, modelAlbumUrl)
            downloadAllPhotos(pageNo, modelindx, modelPhotoUrl)
            modelindx += 1


opener = getUrlOpener()
patten0 = re.compile('(?:.*)<a class="photosUrl" href="(.*)" ><img class="lazy"(?:.*)(?:src="|data-original=")(.*)(album.jpg)')
patten1 = re.compile("共(.*)页")
patten2 = re.compile('(?:.*)<img class="photosImg" src="(.*)" alt="(.*)" />')


class catchThread(threading.Thread):
    def __init__(self, s, e):
        threading.Thread.__init__(self)
        self.s = s
        self.e = e

    def run(self):
        main(self.s, self.e)


th0 = catchThread(2, 40)
th1 = catchThread(40, 80)
th2 = catchThread(80, 120)
th3 = catchThread(120, 160)
th4 = catchThread(160, 200)
th5 = catchThread(200, 240)
th6 = catchThread(240, 280)



th0.start()
th1.start()
th2.start()
th3.start()
th4.start()
th5.start()
th6.start()

