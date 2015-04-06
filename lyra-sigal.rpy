from os import environ

from datetime import datetime

from twisted.python.filepath import FilePath
from twisted.web.resource import Resource
from twisted.web.static import File

from uploads import Upload, Sync, index
from sigalthing import SigalIntegration

gallery = FilePath(environ[b"SIGAL_GALLERY_PATH"])
sigalint = SigalIntegration(
    epoch=datetime.strptime(environ[b"EPOCH"], "%Y-%m-%d"),
    gallery=gallery,
    bucket=environ[b"UPLOAD_BUCKET"],
)

resource = Resource()
resource.putChild(b"upload", Upload(sigalint.add_image))
resource.putChild(b"sync", Sync(sigalint.upload_images))
resource.putChild(
    b"album",
    File(gallery.child(b"sigal").child(b"_build"))
)
resource.putChild(
    b"",
    index(
        environ[b"ONLINE_ALBUM"].decode("ascii"),
        FilePath(b"index.html")
    )
)
