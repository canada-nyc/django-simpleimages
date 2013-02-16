from django.db import models


class URLChangeRecord(models.Model):
    old_url = models.CharField(max_length=200, unique=True)
    new_url = models.CharField(max_length=200, blank=True, null=True)
    deleted = models.BooleanField(default=False)
    date_changed = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        if not self.deleted:
            return u'{} ---> {}'.format(self.old_url, self.new_url)
        return self.old_url
