# -*- coding: utf-8 -*-
from errno import ENOENT
from glob import glob
import os.path
from gs.image import GSImage
from Products.XWFCore.XWFUtils import locateDataDirectory


class UserImage(GSImage):

    def __init__(self, context, userInfo):
        assert context
        self.context = context

        assert userInfo
        self.userInfo = userInfo

        self.file = get_file(context, userInfo)
        super(UserImage, self).__init__(self.file)


def get_file(context, userInfo):
    retval = None
    imagePath = get_image_path(context, userInfo)
    if imagePath:
        retval = file(imagePath, 'rb')
    return retval


def get_image_path(context, userInfo):
    # TODO: Cache
    # --=mpj17=-- Note to Future Coder: version numbers could be added to
    # the files: something like userId-YYYYMMDDHHMMSS.ext ?
    # '{0}-[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]'
    # '[0-9][0-9].*'.format(self.userInfo.id)
    filename = '{0}.*'.format(userInfo.id)
    imagePath = os.path.join(get_imageDir(context), filename)

    retval = None
    files = glob(imagePath)
    if files and os.path.isfile(files[0]):
        retval = files[0]
    else:
        m = 'Cannot open the profile image for {name} ({id})'
        msg = m.format(name=userInfo.name, id=userInfo.id)
        raise IOError(ENOENT, msg, imagePath)
    return retval


def get_imageDir(context):
    # TODO: Cache
    site_root = context.site_root()
    siteId = site_root.getId()
    retval = locateDataDirectory("groupserver.user.image", (siteId,))
    return retval
