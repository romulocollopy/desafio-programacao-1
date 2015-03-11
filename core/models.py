from django.db import models

# Create your models here.


class UploadAction(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)

    @classmethod
    def upload_receipt(cls, UA):
        purchases = cls.objects.get(pk=UA.pk).purchase_set.all()
        return sum([i.item_receipt for i in purchases])

    def __str__(self):
        return 'Upload realizado em {}'.format(self.timestamp)

class Purchase(models.Model):
    uploadaction = models.ForeignKey(UploadAction)
    item_price = models.DecimalField(decimal_places=2, max_digits=14)
    merchant_address = models.CharField(max_length=255)
    purchase_count = models.PositiveSmallIntegerField()
    item_description = models.TextField()
    purchaser_name = models.CharField(max_length=255)
    merchant_name = models.CharField(max_length=255)

    @property
    def item_receipt(self):
        return self.item_price * self.purchase_count

    @classmethod
    def total_receipt(cls):
        return sum([i.item_receipt for i in cls.objects.all()])

    def __str__(self):
        return 'Purchaser: {}'.format(self.purchaser_name)
