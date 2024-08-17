from django.db import models


class CategoryProduct(models.Model):
    name = models.CharField(max_length=100)
    img = models.ImageField(upload_to="images/category/")

    def __str__(self):
        return self.name

