#!/usr/bin/env python

import sys, os, gtk, appindicator

CHECK_FREQUENCY = 60 # seconds
MAILDIRS = [ "/home/brad/Maildir/" ]
DEBUG_LEVEL = 0

class mailIndicator:
   def __init__(self):
      self.ind = appindicator.Indicator ("debian-doc-menu",
              "indicator-messages",
              appindicator.CATEGORY_APPLICATION_STATUS)
      self.ind.set_status (appindicator.STATUS_ACTIVE)
      self.ind.set_attention_icon ("new-messages-red")

      self.buildMenus()

      self.ind.set_menu(self.menu)

   def buildMenus(self):
      self.menu = gtk.Menu()

      self.mutt_item = gtk.MenuItem("Launch Mutt")
      self.mutt_item.connect("activate", self.launch_mutt)
      self.mutt_item.show()
      self.menu.append(self.mutt_item)

      self.maildir_item = gtk.MenuItem("Configure Maildir(s)")
      self.maildir_item.connect("activate", self.maildir_clicked)
      self.maildir_item.show()
      self.menu.append(self.maildir_item)

      self.quit_item = gtk.MenuItem("Quit")
      self.quit_item.connect("activate", self.quit_clicked)
      self.quit_item.show()
      self.menu.append(self.quit_item)

   def run(self):
      self.check_mailbox()
      gtk.timeout_add(CHECK_FREQUENCY * 1000, self.check_mailbox)
      gtk.main()

   def maildir_clicked(self, widget,data=None):
      # stub
      m = gtk.MessageDialog(None, gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_INFO, gtk.BUTTONS_CLOSE, "STUB")
      m.run()
      m.destroy()

   def quit_clicked(self, widget,data=None):
      sys.exit(0)

   def launch_mutt(self, widget,data=None):
      os.system("gnome-terminal -e mutt &")

   def check_mailbox(self):
      DEBUG("Checking Maildirs")
      newmail = False
      for maildir in MAILDIRS:
         newmail = (newmail or (len( os.listdir(maildir + "new") ) > 0))

      if newmail == True:
         self.ind.set_status (appindicator.STATUS_ATTENTION)
         DEBUG("new mail detected.", 2)
      else:
         self.ind.set_status (appindicator.STATUS_ACTIVE)
         DEBUG( "no new mail detected.", 2)
      return True

def DEBUG(message, level = 1):
   if DEBUG_LEVEL >= level:
      print message

if __name__ == "__main__":
   indicator = mailIndicator()
   indicator.run()
