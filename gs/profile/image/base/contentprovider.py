# -*- coding: utf-8 -*-
from base64 import b64encode
from zope.cachedescriptors.property import Lazy
from zope.contentprovider.interfaces import UpdateNotCalled
from zope.pagetemplate.pagetemplatefile import PageTemplateFile
from Products.CustomUserFolder.interfaces import IGSUserInfo
from Products.CustomUserFolder.userinfo import GSAnonymousUserInfo
from gs.viewlet.contentprovider import SiteContentProvider
from userimage import UserImage


class UserImageContentProvider(SiteContentProvider):

    def __init__(self, context, request, view):
        super(UserImageContentProvider, self).__init__(context, request, view)
        self.updated = False

    def update(self):
        self.updated = True
        self.pageTemplate = PageTemplateFile(self.pageTemplateFileName)
        self.finalSize = self.get_final_size()
        self.finalWidth = self.finalSize[0]
        self.finalHeight = self.finalSize[1]
        self.imageUrl = self.get_image_url()

    def render(self):
        if not self.updated:
            raise UpdateNotCalled
        return self.pageTemplate(view=self)

    def get_final_size(self):
        if self.showMissingImage:
            retval = [int(d) for d in (self.width, self.height)]
        elif self.resizeNeeded:
            retval = self.smallImage.getImageSize()
        else:
            retval = self.userImage.getImageSize()
        return retval

    @Lazy
    def showMissingImage(self):
        try:
            retval = self.userInfo.anonymous or (self.userImage.file is None)
        except IOError:
            retval = True
        return retval

    @Lazy
    def resizeNeeded(self):
        return ((int(self.width) < self.userImage.width) or
                    (int(self.height) < self.userImage.height))

    @Lazy
    def smallImage(self):
        if self.resizeNeeded:
            retval = self.userImage.get_resized(int(self.width),
                                                    int(self.height))
        else:
            retval = self.userImage
        return retval

    @Lazy
    def userImage(self):
        return UserImage(self.context, self.userInfo)

    @Lazy
    def userInfo(self):
        try:
            retval = IGSUserInfo(self.user)
        except TypeError:
            retval = GSAnonymousUserInfo()
        return retval

    def get_image_url(self):
        retval = self.missingImage  # From the interface
        try:
            if not self.showMissingImage:
                if self.smallImage.getSize() < 1023:
                    retval = self.embedded_profile_image()
                elif self.resizeNeeded:
                    retval = self.resize_link()
                else:
                    retval = self.profile_image_link()
        except IOError:
            pass  # Use the missingImage
        return retval

    def profile_image_link(self):
        r = '{profile}/gs-profile-image'
        return r.format(profile=self.userInfo.url)

    def resize_link(self):
        r = '{profileLink}/{width}/{height}'
        return r.format(profileLink=self.profile_image_link(),
                            width=self.width, height=self.height)

    def embedded_profile_image(self):
        d = b64encode(self.smallImage.data)
        r = 'data:{mediatype};base64,{data}'
        return r.format(mediatype=self.smallImage.contentType, data=d)

    @Lazy
    def userImageShow(self):
        retval = (self.showImageRegardlessOfUserSetting or
                    getattr(self.user, 'showImage', False))
        assert type(retval) == bool
        return retval
