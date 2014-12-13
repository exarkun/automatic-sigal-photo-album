from __future__ import division

from datetime import datetime
from subprocess import check_call
from re import compile

from characteristic import attributes
from pexif import JpegFile

date_expression = compile("(\d{6,8})")

@attributes(["epoch", "gallery", "bucket"])
class SigalIntegration(object):
    def __init__(self):
        if not self.gallery.isdir():
            raise ValueError("Sigal gallery path does not exist.")

    def add_image(self, filename, image, share):
        all_photos = self.gallery.child(b"photos-all")
        image_path = all_photos.child(filename)
        if image_path.exists():
            raise ValueError("Photo already exists.")

        image_path.setContent(image)

        if share:
            self.add_to_album(image_path)
            build = self.generate_sigal()
            self.upload(build)


    def get_timestamp(self, image_path):
        jpeg = JpegFile.fromFile(image_path.path)
        exif = jpeg.exif.get_primary()
        # 2014:04:23 16:07:06\x00
        if exif[306]:
            return datetime.strptime(exif[306], "%Y:%m:%d %H:%M:%S")

        # Sigh.  From some stupid camera.  Hopefully there's some
        # information in the filename.
        match = date_expression.search(image_path.basename())
        if match is not None:
            data = match.group(0)
            year = "%Y"
            size = 4
            offset = 0
            if len(data) == 6:
                year = "%y"
                size = 2
                offset = 2000
            if 2014 <= int(data[:size]) + offset <= 2100:
                # 2101 could be January 21st I guess
                return datetime.strptime(data, year + "%m%d")
            elif 2014 <= int(data[-size:]) + offset <= 2100:
                return datetime.strptime(data, "%m%d" + year)

        return None


    def add_to_album(self, image_path):
        timestamp = self.get_timestamp(image_path)
        if timestamp is None:
            raise ValueError("Cannot determine timestamp of image.")

        age = timestamp - self.epoch
        weeks = age.total_seconds() / (60 * 60 * 24 * 7)
        # Zero-fill the week into two columns
        albums = self.gallery.child(b"albums")
        album = albums.child(u"week-{:02}".format(int(weeks)))
        if not album.isdir():
            album.makedirs()
        image_path.linkTo(album.child(image_path.basename()))


    def generate_sigal(self):
        working_directory = self.gallery.child(b"sigal")
        check_call(["sigal", "build"], cwd=working_directory.path)
        return working_directory.child(b"_build")


    def upload(self, directory):
        check_call([
                "s3cmd", "--config", self.gallery.child(b"s3cfg").path,
                "sync", directory.path, self.bucket,
        ])
