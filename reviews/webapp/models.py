from django.db import models
from django.contrib.auth import get_user_model


class Product(models.Model):
    CATEGORY_CHOICES = [('Smartphones', 'Smartphones'), ('Laptops', 'Laptops'), ('Appliances', 'Appliances')]
    name = models.CharField(max_length=30, blank=False, null=False, verbose_name="Name")
    category = models.CharField(max_length=20, blank=False, null=False, choices=CATEGORY_CHOICES,
                                verbose_name="Category")
    description = models.CharField(max_length=2000, verbose_name="Description")
    picture = models.ImageField(upload_to="pictures", verbose_name="Picture")

    def __str__(self):
        return f"{self.name} ({self.category})"

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"


class Review(models.Model):
    RATING_CHOICES = [('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')]
    author = models.ForeignKey(get_user_model(), on_delete=models.SET_DEFAULT, default=1, verbose_name="Author")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Product", related_name="reviews")
    text = models.CharField(max_length=1500, null=False, blank=False)
    rating = models.CharField(max_length=2, blank=False, null=False, choices=RATING_CHOICES, verbose_name="Rating")

    def __str__(self):
        return f"{self.product} ({self.author}, {self.rating})"

    class Meta:
        verbose_name = "Review"
        verbose_name_plural = "Reviews"
