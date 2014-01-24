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
from __future__ import unicode_literals
from zope.contentprovider.interfaces import IContentProvider
from zope.schema import ASCIILine, Bool, Field, Int

# FIXME: use gs.config
MISSING_IMAGE_URL = '/++resource++gs-profile-image-base-missing.jpg'


class IGSUserImage(IContentProvider):
    """User Image"""
    pageTemplateFileName = ASCIILine(
        title="Page Template File Name",
        description='The name of the ZPT file that is used to render the '
                    'profile image.',
        required=False,
        default="browser/templates/userimage.pt".encode('ascii', 'ignore'))

    user = Field(
        title='User Instance',
        description='An instance of the CustomUser Class',
        required=True)

    showImageRegardlessOfUserSetting = Bool(
        title='Show Image Regardles of User Setting',
        description="Show the user's image, regardless of the value of "
                    "the showImage property. This should be used with "
                    "extreme caution, as it can violate the user's privacy.",
        required=False,
        default=False)

    width = Int(
        title='Width',
        description='The width of the image, in pixels.',
        required=False,
        default=50)  # FIXME: use gs.config

    height = Int(
        title='Height',
        description='The height of the image, in pixels.',
        required=False,
        default=70)  # FIXME: use gs.config

    missingImage = ASCIILine(
        title='Missing Image',
        description='The URL of the image to use for the missing-image '
                    'image.',
        required=False,
        default=MISSING_IMAGE_URL.encode('ascii', 'ignore'))
