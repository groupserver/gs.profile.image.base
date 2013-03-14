# coding=utf-8
from base64 import b64encode
from zope.cachedescriptors.property import Lazy
from zope.contentprovider.interfaces import UpdateNotCalled
from zope.pagetemplate.pagetemplatefile import PageTemplateFile
from Products.CustomUserFolder.interfaces import IGSUserInfo
from gs.viewlet.contentprovider import SiteContentProvider
from userimage import UserImage


class UserImageContentProvider(SiteContentProvider):
    """GroupServer view of the user image
    """
    def __init__(self, context, request, view):
        super(UserImageContentProvider, self).__init__(context, request, view)
        self.__updated = False
        self.pageTemplate = None

    def update(self):
        self.__updated = True
        self.pageTemplate = PageTemplateFile(self.pageTemplateFileName)

    def render(self):
        if not self.__updated:
            raise UpdateNotCalled
        return self.pageTemplate(view=self)

    @Lazy
    def userInfo(self):
        retval = IGSUserInfo(self.user)
        return retval

    @Lazy
    def userImage(self):
        retval = UserImage(self.context, self.userInfo)
        return retval

    @Lazy
    def size(self):
        return [int(d) for d in (self.width, self.height)]

    @Lazy
    def userImageUrl(self):
        retval = self.missingImage  # From the interface
        try:
            if (not(self.userInfo.anonymous) and self.userImage.imagePath):
                if max(self.size) >= 40:
                    retval = self.profile_image_link()
                else:
                    retval = self.embedded_profile_image()
        except IOError:
            pass  # Use the missingImage
        return retval

    def profile_image_link(self):
        r = '{profile}/gs-profile-image/{width}/{height}'
        retval = r.format(profile=self.userInfo.url, width=self.width,
                            height=self.height)
        return retval

    def embedded_profile_image(self):
        smallImage = self.userImage.get_resized(self.width, self.height)
        d = b64encode(smallImage.data)
        r = 'data:{mediatype};base64,{data}'
        retval = r.format(mediatype=smallImage.contentType, data=d)
        return retval

    @Lazy
    def userImageShow(self):
        retval = (self.showImageRegardlessOfUserSetting or
                    getattr(self.user, 'showImage', False))
        assert type(retval) == bool
        return retval
