#!/usr/bin/env python

import sys, os, gtk, indicate, pynotify, rfc822, string, email.header, email.charset

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
MUA_LAUNCH_COMMAND="/usr/bin/gnome-terminal -e mutt &"

# Title for notification bubbles
NOTIFY_TITLE="Maildir Indicator"

# Output some messages to console.
DEBUG_LEVEL = 0

# Shorten long names or subjects to a maximum of:
MAX_HEADER_LENGTH = 20


class mailIndicator:
    notified_messages=[]

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
        new_messages = {} # { sender: [subject, subject, subject], ...} 

        # Check mailboxes for new mail
        for name, path in MAILDIRS.iteritems():
            attention = "false"
            try:
                # Get a count of "new" mail.
                # TODO: Should check for unseen mail in cur
                messages = os.listdir(path + "new")
                count = len( messages)
                oldcount = self.indicators[name].get_property("count")

                # get sender names and titles for new messages
                for message in messages:
                    if message not in self.notified_messages:
                        # build an rfc822 object to access email data
                        fh = open( os.path.join(path, "new", message) )
                        parsed_message = rfc822.Message(fh)
                        fh.close()
                        
                        sender = get_parsed_header(parsed_message, "From")
                        subject = get_parsed_header(parsed_message, "Subject")

                        if new_messages.has_key(sender):
                            new_messages[sender].append(subject)
                        else:
                            new_messages[sender] = [subject]


                    
                self.notified_messages = messages

                # If there are more messages than previously, then we need to notify about it
                if ( count > int(oldcount) ):
                    noticecount += count
                    attention = "true"
            except OSError:
                # If there was an error, set error
                count = "error"

            DEBUG("checking '" + name + "': " + str(count) + " new messages detected", 2)


            # Indicate number of new messages
            self.indicators[name].set_property("count", str(count))
            # Set draw-attention if there is more than 0
            self.indicators[name].set_property("draw-attention", attention);

        if ( noticecount > 0 ):
            # format our notification to
            # Sender Name: subject1, subject 2
            # Sender Name2: subject3, subject 4
            new_messages = map( 
                lambda x: 
                    "%s: %s" % (x, string.join(new_messages[x], ", ") ), 
                    new_messages.keys() )
            notify_text = str(noticecount) + " new email messages:\n" + \
                string.join(new_messages, "\n")

            DEBUG(notify_text)
            self.sendnotify(notify_text)

        return True

    def sendnotify(self, message):
        if not self.notify:
            DEBUG("Bypassing notification")
            return True

        DEBUG("Sending notification")
        n = pynotify.Notification(NOTIFY_TITLE, message, "notification-message-email")
        n.show()

        return n

def get_parsed_header(parsed_message, header_name):
    # I hate charsets!
    # parsed_message should be an rfc822 object. getheader returns a list
    # of (value, encoding) tuples. Should return header as decoded unicode 
    # string.
    header = parsed_message.getheader(header_name)
    header = email.header.decode_header(header)

    if  header[0][1] != None: # no charset specified
        header = unicode(header[0][0], header[0][1])
    else: # charset specified
        header = unicode(header[0][0])

    if header_name == "From": 
        # Remove email address and just give name
        header = header.split(" <", 1)[0]

    if len(header) > MAX_HEADER_LENGTH: 
        header = header[:MAX_HEADER_LENGTH-3] + "..."

    return header
       

def DEBUG(message, level = 1):
   if DEBUG_LEVEL >= level:
      print message

if __name__ == "__main__":
   indicator = mailIndicator()
   indicator.run()
