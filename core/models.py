from django.db import models
from django.db.models import Avg


class UploadAction(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)

    @classmethod
    def upload_average_receipt(cls):
        pr = Purchase.total_receipt()
        return pr/cls.objects.count()

    @property
    def upload_receipt(self):
        purchases = self.purchase_set.all().select_related('purchase')
        return sum([i.item_receipt for i in purchases])

    @property
    def items_count(self):
        return self.purchase_set.count()

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

    @classmethod
    def average_item_price(cls):
        return cls.objects.all().aggregate(Avg('item_price'))['item_price__avg']

    def __str__(self):
        return 'Purchaser: {}'.format(self.purchaser_name)
