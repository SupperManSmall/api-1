#!/usr/bin/env
# coding=utf-8
import web
import platform, commands

urls = (
    '/', 'index',
    '/wph', 'index_wph',
    '/short', 'short',
    '/short_wph', 'short_wph'


)

render = web.template.render('templates/')

app = web.application(urls, globals())
application = app.wsgifunc()

web.config.debug = True
cache = False

pw = '123456'
path = '/Users/xcma/code/god_wph/'
if platform.system() == 'Linux':
    pw = 'wphxxtao2016'
    path = '/home/git/AutoTest/'
db = web.database(dbn='mysql', user='root', pw=pw, db='god', host='127.0.0.1')

class index:

    def GET(self):
        sql = "select count(*) from test_result where url_target LIKE 'xx%'"
        results = db.query(sql)
        total = results[0]['count(*)']
        sql = "select count(*) from test_result where result = 'Pass' AND url_target LIKE 'xx%'"
        results = db.query(sql)
        p = results[0]['count(*)']
        f = total-p
        results = [total, p, f]
        sql = "url_target='xxtao.com' or url_target='xxtao'"
        todos = db.select('test_result', where=sql, order='if_name')

        return render.index(todos, results)

class index_wph:
    def GET(self):
        sql = "select count(*) from test_result where url_target LIKE 'w%'"
        results = db.query(sql)
        total = results[0]['count(*)']
        sql = "select count(*) from test_result where result = 'Pass' AND url_target like 'w%'"
        results = db.query(sql)
        p = results[0]['count(*)']
        f = total - p
        results = [total, p, f]
        sql = "url_target='wanpinghui.com' or url_target='wanpinghui'"
        todos = db.select('test_result', where=sql, order='if_name')
        return render.index_wph(todos, results)

class short:
    def GET(self):
        sql = "SELECT count(*) FROM (SELECT * FROM (SELECT * FROM test_short_url WHERE url_target LIKE 'xx%') a ORDER BY id DESC LIMIT 100) b;"
        results = db.query(sql)
        total = results[0]['count(*)']
        sql = "SELECT count(*) FROM (SELECT * FROM (SELECT * FROM test_short_url WHERE url_target LIKE 'xx%') a ORDER BY id DESC LIMIT 100) b WHERE result = 'Pass';"
        results = db.query(sql)
        p = results[0]['count(*)']
        f = total - p
        results = [total, p, f]
        sql = "url_target='xxtao.com' or url_target='xxtao'"
        todos = db.select('test_short_url', where=sql, limit='100',order='id desc')
        return render.short_url(todos, results)

class short_wph:
    def GET(self):
        sql = "SELECT count(*) FROM (SELECT * FROM (SELECT * FROM test_short_url WHERE url_target LIKE 'w%') a ORDER BY id DESC LIMIT 100) b;"
        results = db.query(sql)
        total = results[0]['count(*)']
        sql = "SELECT count(*) FROM (SELECT * FROM (SELECT * FROM test_short_url WHERE url_target LIKE 'w%') a ORDER BY id DESC LIMIT 100) b WHERE result = 'Pass';"
        results = db.query(sql)
        p = results[0]['count(*)']
        f = total - p
        results = [total, p, f]
        sql = "url_target='wanpinghui.com' or url_target='wanpinghui'"
        todos = db.select('test_short_url', where=sql, limit='100', order='id desc')
        return render.short_url_wph(todos, results)

class add:

    def POST(self):
        i = web.input()
        if i.title in 'xxtao.com':
            (status, output) = commands.getstatusoutput('python '+path+'Run.py -m a -t xxtao')
        else:
            commands.getstatusoutput('python '+path+'Run.py -m a -t wanpinghui')
        # n = db.insert('todo', title=i.title)
        # raise web.seeother('/')

class short_add:

    def POST(self):
        i = web.input()
        if i.title in 'xxtao.com':
            (status, output) = commands.getstatusoutput('python '+path+'Run.py -m u -c ShortUrl -t xxtao')
        else:
            (status, output) = commands.getstatusoutput('python '+path+'Run.py -m u -c ShortUrl -t wanpinghui')
        # n = db.insert('todo', title=i.title)
        # raise web.seeother('/')

if __name__ == "__main__":
    app.run()