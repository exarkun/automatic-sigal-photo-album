from cgi import FieldStorage
from email.parser import FeedParser

from twisted.web.resource import Resource
from twisted.web.util import redirectTo

class Upload(Resource):
    def __init__(self, process_upload):
        self.process_upload = process_upload


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
        upload = b"upload" in form

        if upload:
            filename = value = None
        else:
            p = FeedParser()
            p.feed("Content-Disposition: " + form['image'].headers.getheader('content-disposition'))
            m = p.close()
            filename = m.get_filename()
            value = image.value

        self.process_upload(filename, value, share, upload)

        return redirectTo(form[b"return-url"].value, request)
