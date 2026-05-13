from django.conf import settings
from django.db import models
from django.utils import timezone


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
    
    # property is a decorator that lets us use a method like an attribute
    # so even though available copies gets calculated every time instead of being stored
    # we can still write book.available_copies as if it were an attribute of book.
    @property

    def borrowed_copies(self):
        return self.borrowrecord_set.filter(return_date__isnull=True).count()

    # check available
    @property
    def available_copies(self):
        return self.quantity - self.borrowed_copies
    
class Member(models.Model):

    # django has built in user model that incudes username, password, email, first_name and last_name.
 
    # cascade so if we delete user(django class) then member profile is deleted aswell.
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.user.username

class BorrowRecord(models.Model):
  

    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    # making sure when member is deleted we delete their borrow record

    member = models.ForeignKey(Member, on_delete=models.CASCADE)

    # using local machine time to see when book was borrowed
    borrow_date = models.DateField(default=timezone.localdate)

    # need due date to implement fine system for late returns
    due_date = models.DateField()


    # return date is empty until book is returned
    return_date = models.DateField(null=True, blank=True)

    # book can be returned in 3 types of condition
    RETURN_CONDITION_CHOICES = [
        ("good", "Good"),
        ("damaged", "Damaged"),
        ("lost", "Lost"),
    ]
    return_condition = models.CharField(
        max_length=10,
        choices=RETURN_CONDITION_CHOICES,
        blank=True
    )

    def __str__(self):
        return f"{self.member} borrowed {self.book}"