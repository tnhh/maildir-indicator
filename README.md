A fork of Chris Irwin and Brad Mont's maildir indicator applet.

http://blog.chrisirwin.ca/update-for-maildir-indicator

https://gitorious.org/chrisirwin-utils/maildir-indicator/

The main changes are:

- to change the behaviour of what happens when you click on an item in
  the indicator. Previously clicks on the first item would launch the
  MUA, and clicks on a maildir would clear the "attention" setting.
  Now:
  - clicking on the first item ("Maildir indicator") clears the
    attention setting for all maildirs
  - clicking on a maildir launches the MUA with the "FOLDER"
    environment variable set. I use this to launch mutt in the
    correct maildir.  It also clears the attention flag for that
    maildir.
- the attention flag seems to be unreliable under Ubuntu 12.04. If you
  clear the flags using the "Clear" entry at the bottom of the menu,
  then the envelope never turns blue again. I haven't been able to
  work out why this is. So I add an asterisk to the end of each
  maildir containing new mail, as an extra indicator.
