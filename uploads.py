from cgi import FieldStorage
from email.parser import FeedParser

from twisted.web.resource import Resource
from twisted.web.util import redirectTo

class Sync(Resource):
    def __init__(self, sync):
        self.sync = sync


    def render_POST(self, request):
        self.sync()
        form = request.args
        return redirectTo(form[b"return-url"][0], request)



class Upload(Resource):
    def __init__(self, process_image):
        self.process_image = process_image


    def render_POST(self, request):
        # XXX request.requestHeaders
        headers = request.getAllHeaders()
        form = FieldStorage(
            fp=request.content,
            headers=headers,
            environ={
                b'REQUEST_METHOD': request.method,
                b'CONTENT_TYPE': headers[b'content-type'],
                }
            )
        image = form[b"image"]
        share = b"share" in form

        p = FeedParser()
        p.feed(
            "Content-Disposition: " +
            form['image'].headers.getheader('content-disposition'))
        m = p.close()
        filename = m.get_filename()
        value = image.value

        self.process_image(filename, value, share)

        return redirectTo(form[b"return-url"].value, request)
