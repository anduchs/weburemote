weburemote
==========

This is a dirty hacky insecure solution to remote control my livingroom box:
- Supports vt-switching between VTs (1 to 4; i.e. Console, Firefox, XBML, GDM)
- Supports Trackpad-Emulation from WebInterface via Ajax calls
- Runs fine on Android 4.x and iPhone browsers

Install
-------
- Requires:
  - jquery (some 1.x and possibly up): http://jquery.org
  - jquery.event.move: https://github.com/stephband/jquery.event.move
  - python-uinput: https://github.com/tuomasjjrasanen/python-uinput
- Put all in the same folder and sudo start...

TODOs
-----
- Use thread-mixin for basehttpserver
- Support WebSockets (some code already as comments)
- Add some jQuery-Keyboard-support
- Add support for Tab+Drag and double-click

Contribute
----------
- Issues-Page
- Fork
- Design the Web-Page
- ...

WARNING
-------
This is completely insecure hacky non-sense. I'm not really proud of it, but
maybe someone feels inspired to make a clean version out of it.

