from django.db import models

class Reference(models.Model):
    crawled_uri = models.URLField(max_length=400)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    url_id = models.AutoField(primary_key=True)

    def __str__(self):
        return self.crawled_uri