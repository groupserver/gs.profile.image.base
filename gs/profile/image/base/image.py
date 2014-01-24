# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright © 2014 OnlineGroups.net and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
from __future__ import absolute_import
from zope.cachedescriptors.property import Lazy
from gs.profile.base.page import ProfilePage
from .userimage import UserImage


class Image(ProfilePage):

    def __init__(self, context, request):
        super(Image, self).__init__(context, request)
        self.traverse_subpath = []

    def publishTraverse(self, request, name):
        self.traverse_subpath.append(name)
        return self

    @Lazy
    def userImage(self):
        retval = UserImage(self.context, self.userInfo)
        return retval

    @Lazy
    def width(self):
        tsp = self.traverse_subpath
        if len(tsp) > 0:
            retval = int(tsp[0])
        else:
            retval = self.userImage.width
        return retval

    @Lazy
    def height(self):
        tsp = self.traverse_subpath
        if len(tsp) >= 2:
            retval = int(tsp[1])
        elif len(tsp) == 1:
            r = float(self.userImage.height) / float(self.userImage.width)
            retval = int((self.width * r) + 0.5)
        else:
            retval = self.userImage.height
        return retval

    @Lazy
    def image(self):
        if self.traverse_subpath:
            retval = self.userImage.get_resized(self.width, self.height,
                                                maintain_aspect=True,
                                                only_smaller=False)
        else:
            retval = self.userImage
        return retval

    def __call__(self):
        # TODO: Add the x-sendfile suff
        try:
            h = 'inline; filename={0}-{1}x{2}.jpg'
            hdr = h.format(self.userInfo.nickname, self.width, self.height)
            self.request.RESPONSE.setHeader('Content-Disposition', hdr)

            self.request.RESPONSE.setHeader('Cache-Control',
                                            'private; max-age=1200')

            self.request.RESPONSE.setHeader('Content-Type',
                                            self.image.contentType)

            self.request.RESPONSE.setHeader('Content-Length',
                                            self.image.getSize())
            retval = self.image.data
        except IOError:
            missingImage = '/++resource++gs-profile-image-base-missing.jpg'
            retval = self.request.RESPONSE.redirect(missingImage)
        return retval
