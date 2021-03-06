import os
from django.db import models
from django.conf import settings

FTP_DEFAULT_UID = getattr(settings, "FTP_DEFAULT_UID", 1000)
FTP_DEFAULT_GID = getattr(settings, "FTP_DEFAULT_GID", 1000)
FTP_DEFAULT_HOMEDIR_BASE = getattr(settings, "FTP_DEFAULT_HOMEDIR_BASE", "/home")
FTP_DEFAULT_SHELL = getattr(settings, "FTP_DEFAULT_SHELL", "/bin/false")

class FTPUser(models.Model):
    """
    Model to handle FTP-Users

    see: http://www.proftpd.org/docs/directives/linked/config_ref_SQLAuthTypes.html
    and: http://www.proftpd.org/docs/directives/linked/config_ref_SQLUserInfo.html
    """

    username = models.CharField(max_length=255, unique=True, db_index=True)
    password = models.CharField(max_length=255, db_index=True)

    ## unix user info
    uid = models.IntegerField(default=FTP_DEFAULT_UID)
    gid = models.IntegerField(default=FTP_DEFAULT_GID)

    homedir = models.CharField(max_length=255, blank=True, help_text=u"Default: %s" % os.path.join(FTP_DEFAULT_HOMEDIR_BASE, "username"))
    shell = models.CharField(max_length=255, default=FTP_DEFAULT_SHELL)

    #optional comment
    comment = models.CharField(max_length=255, null=True, blank=True)

    active = models.BooleanField(default=True, db_index=True)
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'ftp_users'
        verbose_name = 'FTP user'

    def save(self, *args, **kwargs):
        if not self.homedir:
            self.homedir = os.path.join(FTP_DEFAULT_HOMEDIR_BASE, self.username)
        super(FTPUser, self).save(*args, **kwargs)

