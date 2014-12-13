from __future__ import division

from datetime import datetime
from subprocess import check_call

from characteristic import attributes
from pexif import JpegFile

@attributes(["epoch", "gallery"])
class SigalIntegration(object):
    def __init__(self):
        if not self.gallery.isdir():
            raise ValueError("Sigal gallery path does not exist.")

    def add_image(self, image, share):
        all_photos = self.gallery.child(b"photos-all")
        image_path = all_photos.child(image.name)
        if image_path.exists():
            raise ValueError("Photo already exists.")

        image_path.setContent(image.value)

        if share:
            self.add_to_album(image_path)
            build = self.generate_sigal()
            self.upload(build)

    def add_to_album(self, image_path):
        jpeg = JpegFile.fromFile(image_path.path)
        exif = jpeg.exif.get_primary()
        # 2014:04:23 16:07:06\x00
        timestamp = datetime.strptime(exif[306], "%Y:%M:%D %H:%M:%S")
        age = timestamp - self.epoch
        weeks = age.total_seconds() / (60 * 60 * 24 * 7)
        # Zero-fill the week into two columns
        albums = self.gallery.child(b"albums")
        album = albums.child(u"week-{:02}".format(int(weeks)))
        image_path.linkTo(album.child(image_path.basename()))


    def generate_sigal(self):
        working_directory = self.gallery.child(b"sigal")
        check_call(["sigal", "build"], cwd=working_directory.path)
        return working_directory.child(b"_build")


    def upload(self, directory):
        check_call(["s3cmd", "sync", directory.path, self.bucket])
