#!/usr/bin/env python

import sys, os, gtk, indicate, pynotify

# This utility monitors maildirs and emits a notification when new messages arrive.
# It sits in ubuntu's messaging menu.

# How frequently to check for new messages, in seconds
CHECK_FREQUENCY = 60

# Hash of maildirs in "FriendlyName : PathWithTrailingSlash" format
MAILDIRS = {    "Inbox"     : "/home/chris/.maildir-chrisirwin/INBOX/",
                "KWLug"     :"/home/chris/.maildir-chrisirwin/Lists/Groups/KWLug/"
                }

# Indicator entry requires a desktop. It uses it for name & icon.
# As this will be passed to an external process, the file must be an absolute path.
MUA_DESKTOP_FILE = os.path.abspath(os.path.dirname(sys.argv[0])) + "/mutt.desktop"

# Workaround for Ubuntu bug#378783: "xdg-open *.desktop opens text editor"
# https://bugs.launchpad.net/ubuntu/+source/xdg-utils/+bug/378783
# Due to this bug, trying to xdg-open the MUA_DESKTOP_FILE will instead open it
# in a text editor. We *could* parse the EXEC line, but would miss TERMINAL=true,
# and possibly other things.
MUA_LAUNCH_COMMAND="/usr/bin/guake &"

# Title for notification bubbles
NOTIFY_TITLE="Maildir Indicator"

# Output some messages to console.
DEBUG_LEVEL = 0


class mailIndicator:
    def __init__(self):

        # Register with indicator applet
        DEBUG("Registering with Indicator Applet")
        self.indicator = indicate.indicate_server_ref_default()
        self.indicator.set_type("message.mail")
        self.indicator.set_desktop_file(MUA_DESKTOP_FILE)
        self.indicator.connect("server-display", self.indicator_clicked)
        self.indicators = {}

        # Register with notification system
        if pynotify.init( ("Maildir Indicator") ):
            DEBUG("Registered with Notification system")
            self.notify = True
        else:
            DEBUG("Failed Registeration with Notification system")
            self.notify = False

        # Build list of maildir indicators
        self.buildMenus()

    def buildMenus(self):
        DEBUG("Building maildir indicator list")
        # Loop through the maildirs configured above
        for name, path in MAILDIRS.iteritems():
            DEBUG("Adding maildir '" + name + "'")
            # Create mailbox indicator
            new_indicator = indicate.Indicator()
            new_indicator.set_property("name", name)
            new_indicator.set_property("count", "0")
            new_indicator.label = name
            new_indicator.connect("user-display", self.maildir_clicked)

            # Always show it
            new_indicator.show()

            # Save it for later
            self.indicators[name] = new_indicator

    def run(self):
        # This is the main loop
        self.check_mailbox()
        gtk.timeout_add(CHECK_FREQUENCY * 1000, self.check_mailbox)
        gtk.main()

    def maildir_clicked(self, widget, data=None):
        # Not sure how to do this nicely.
        # no-op it for now.
        return True

    def indicator_clicked(self, widget,data=None):
        # Run MUA_LAUNCH_COMMAND
        os.system(MUA_LAUNCH_COMMAND)

    def check_mailbox(self):
        DEBUG("Begin Mail Check")

        noticecount = 0

        # Check mailboxes for new mail
        for name, path in MAILDIRS.iteritems():
            attention = "false"
            try:
                # Get a count of "new" mail.
                # TODO: Should check for unseen mail in cur
                count = len( os.listdir(path + "new") )
                oldcount = self.indicators[name].get_property("count")

                # If there are more messages than previously, then we need to notify about it
                if ( count > int(oldcount) ):
                    noticecount += count
                    attention = "true"
            except:
                # If there was an error, set error
                count = "error"

            DEBUG("checking '" + name + "': " + str(count) + " new messages detected", 2)


            # Indicate number of new messages
            self.indicators[name].set_property("count", str(count))
            # Set draw-attention if there is more than 0
            self.indicators[name].set_property("draw-attention", attention);

        if ( noticecount > 0 ):
            self.sendnotify(str(noticecount) + " new email messages.")

        return True

    def sendnotify(self, message):
        if not self.notify:
            DEBUG("Bypassing notification")
            return True

        DEBUG("Sending notification")
        n = pynotify.Notification(NOTIFY_TITLE, message, "notification-message-email")
        n.show()

        return n

def DEBUG(message, level = 1):
   if DEBUG_LEVEL >= level:
      print message

if __name__ == "__main__":
   indicator = mailIndicator()
   indicator.run()
