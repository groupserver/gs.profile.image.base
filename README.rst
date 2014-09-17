=========================
``gs.profile.image.base``
=========================
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Profile images for GroupServer Users
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:Author: `Michael JasonSmith`_,
:Contact: Michael JasonSmith <mpj17@onlinegroups.net>
:Date: 2013-03-13
:Organization: `GroupServer.org`_
:Copyright: This document is licensed under a
  `Creative Commons Attribution-Share Alike 3.0 New Zealand License`_
  by `OnlineGroups.Net`_.


Introduction
============

This product supplies the code for displaying scaled profile images. The
core scaling is provided by ``gs.image``, while this product provides

* A `content provider`_ to provide a high-level API, 
* A view_ to display the image at different sizes, 
* A class_ to map a user to an image, and 
* The `missing image`_ resource that is shown if the image cannot be found.

Content Provider
================

The ``groupserver.UserImage`` content provider is used by almost all the
code that needs to display a profile image::

  <div tal:define="user view/userInstanceToShow"
       tal:replace="structure provider:groupserver.UserImage" />

It returns a ``<div>`` element (with the ``userimage`` and ``photo``
classes) that contains an ``<img>`` element. The ``src`` attribute of the
``<img>`` element points to the `view`_, if the user has a profile image,
or the `missing image`_ resource. The size of the image defaults to 50×70
pixels [#units]_ with the ``width`` and ``height`` attributes of the
``<img>`` element set. However, if the longest length of the image is less
that 40 pixels then a `data URI`_ is used to embed the profile image in the
page, rather than using a normal URL.


Two optional arguments can be passed to the content provider to change the
size: ``width`` and ``height``. While the size of the image will be changed,
the aspect ratio of the image is preserved (see View_ below)::

  <div tal:define="user view/userInstanceToShow;
                   width string:14; height string:18;"
       tal:replace="structure provider:groupserver.UserImage" />

View
====

The view ``/p/{userId}/gs-profile-image`` is a view that returns the image
for the user. The ``gs-profile-image`` view provides an **API** for viewing
the profile image at different sizes [#api]_. Two optional arguments can be
passed as part of a path, to set the width and the height of the image.

* Not providing any arguments displays the **original** image that the
  participant uploaded: <http://groupserver.org/p/mpj17/gs-profile-image>.

* If only one argument is provided, the **width** is set and the height
  will be calculated, keeping the same aspect ratio as the original
  image. A new image will be returned that is scaled as requested. For
  example, setting the width to 100px:
  <http://groupserver.org/p/mpj17/gs-profile-image/100>.

* The **height** is specified after the width. The image will be scaled so
  neither the width nor the height will be exceeded. However, the *aspect
  ratio* will be preserved, so one dimension may be smaller than requested
  [#resize]_. For example, ensuring that the width does not exceed 100px,
  and the height is smaller than to 125px:
  <http://groupserver.org/p/mpj17/gs-profile-image/100/125>.

The scaling of the image is carried out by the ``UserImage`` class_.  If
the participant lacks an image then the viewer is redirected to the
`missing image`_ resource instead.

Class
=====

The class ``gs.profile.image.base.UserImage`` is a subclass of
``gs.image.GSImage``. It differs in the constructor, which takes a
``context`` and a user-info, rather than a file. 

The ``context`` and user-info are used to construct a *glob* for the file
[#glob]_, looking in the ``groupserver.user.image`` data-directory (usually
found beneath ``var/instance/groupserver.data`` in the GroupServer
directory). A glob is used so different file types, with different
extensions, can be used.

If the file cannot be found then an ``IOError`` is thrown. The error has
the following properties set.

``errno``:
  The error number is set to ``errno.ENOENT``.

``filename``:
  The *glob* that was used to try and find the file.

If the file is found then it is opened and passed to the constructor for
``GSImage``.

Missing Image
=============

The resource ``/++resource++gs-profile-image-base-missing.jpg`` is the
*missing profile image* image.

Resources
=========

- Code repository: https://source.iopen.net/groupserver/gs.profile.image.base
- Questions and comments to http://groupserver.org/groups/development
- Report bugs at https://redmine.iopen.net/projects/groupserver

.. _GroupServer: http://groupserver.org/
.. _GroupServer.org: http://groupserver.org/
.. _OnlineGroups.Net: https://onlinegroups.net/
.. _Michael JasonSmith: http://groupserver.org/p/mpj17/
.. _Creative Commons Attribution-Share Alike 3.0 New Zealand License:
   http://creativecommons.org/licenses/by-sa/3.0/nz/

.. [#units] 50×70 pixels is 2.5×3.5 units in the standard `GroupServer
            CSS`_.
.. _GroupServer CSS: https://source.iopen.net/groupserver/gs.content.css

.. _data URI: http://tools.ietf.org/html/rfc2397
.. [#api] The API is the same as the images supported by
          ``Products.XWFFileLibrary2``.

.. [#resize] See ``gs.image`` for details on resizing
             <https://source.iopen.net/groupserver/gs.image>

.. [#glob] See `the glob module`_.
.. _the glob module: http://docs.python.org/2.7/library/glob.html
