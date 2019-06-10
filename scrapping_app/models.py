from django.db import models
   
   
class ProductItem(models.Model):
    product = models.ForeignKey("ProductTag", on_delete=models.CASCADE)
    field = models.CharField(max_length=50)
    value = models.CharField(max_length=500)
    tag_name = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return "{} {}".format(self.field, self.value)
    

class ProductTag(models.Model):
    name = models.CharField(max_length=500, default="Product_")

    def bulk_insert(self, **kwargs):
        for key, value in kwargs.items():
            ProductItem.objects.create(
                product=self,
                field=key,
                value=value.split("|")[0],
                tag_name=value.split("|")[1] if len(value.split("|")) > 1 else None
            )
        return True

    def product_tags(self):
        return self.productitem_set.all()
   
    def __str__(self):
        return "{}".format(self.name)

    

    
    
