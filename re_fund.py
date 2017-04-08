import web

render = web.template.render('templates/')

class Refund:
    def GET(self):
        return render.refund()