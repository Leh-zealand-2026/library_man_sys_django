from django.db import models



class Category(models.Model):
    # books can be searched by category so we make sure to use "unique=True"
    # so we dont create different category with the same name, we use this for anything that has to be unique.
    name = models.CharField(max_length=100, unique=True)

    # django puts s at the end of models so category becomes categorys, but we can define it ourself.
    class Meta:
        verbose_name_plural = "Categories"

    # make sure we show string name
    def __str__(self):
        return self.name


class Book(models.Model):

    title = models.CharField(max_length=200)

    author = models.CharField(max_length=150)

    isbn = models.CharField(max_length=13, unique=True)


    publisher = models.CharField(max_length=150)

    # PositiveIntegerField to make sure we cant own negative number of books.
    # default=1 so we always have 1 book unless we change it.
    quantity = models.PositiveIntegerField(default=1)


    # Books can fit into many categories, for example fantasy and also action
    # so we define relationship as many to many.

    categories = models.ManyToManyField(Category)

    def __str__(self):
        return f"{self.title} by {self.author}"