from cgi import FieldStorage

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
        share = form[b"share"].value == 'on'
        self.process_upload(image, share)

        return redirectTo(form[b"return-url"].value, request)
