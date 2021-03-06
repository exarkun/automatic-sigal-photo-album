from os import environ
from datetime import datetime

from twisted.python.filepath import FilePath
from twisted.web.resource import Resource
from twisted.web.static import File

from uploads import Upload
from uploads import Sync
from sigalthing import SigalIntegration

sigalint = SigalIntegration(
    epoch=datetime.strptime(environ[b"EPOCH"], "%Y-%m-%d"),
    gallery=FilePath(environ[b"SIGAL_GALLERY_PATH"]),
    bucket=environ[b"UPLOAD_BUCKET"],
)

resource = Resource()
resource.putChild(b"upload", Upload(sigalint.add_image))
resource.putChild(b"sync", Sync(sigalint.upload_images))
resource.putChild(b"", File(b"index.html"))
