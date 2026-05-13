from django.contrib.auth import login
from django.db.models import Q # django database filters
from django.shortcuts import redirect, render, get_object_or_404

# for borrowed books
from datetime import timedelta
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.http import HttpResponseForbidden # dont allow user to borrow without member profile

from .forms import RegisterForm
from .models import Book, BorrowRecord, Category, Member


# https://docs.djangoproject.com/en/6.0/topics/auth/default/#built-in-auth-views

def home(request):

    return render(request, "books/home.html")


# member registration.
def register(request):
    # we created RegisterForm in forms.py
    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            
            user = form.save()
            Member.objects.create(user=user)

            login(request, user)
            return redirect("home")
    else:
        form = RegisterForm()

    return render(request, "books/register.html", {"form": form})

# browse and search books
def book_list(request):
    books = Book.objects.all()
    categories = Category.objects.all()

    search_query = request.GET.get("q")
    category_id = request.GET.get("category")
    # using django database filter
    if search_query:
        books = books.filter(
            Q(title__icontains=search_query) |
            Q(author__icontains=search_query) |
            Q(isbn__icontains=search_query)
        )

    if category_id:
        books = books.filter(categories__id=category_id)

    return render(request, "books/book_list.html", {
        "books": books,
        "categories": categories,
        "search_query": search_query,
        "selected_category": category_id,
    })

# the view for borrowing books
@login_required
def borrow_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    # check if user has a member account before letting them borrow
    try:
        member = request.user.member
    except Member.DoesNotExist:
        return HttpResponseForbidden("Only registered members can borrow books, please create member profile.")

    # check if book copies are available
    if book.available_copies > 0:
        BorrowRecord.objects.create(
            book=book,
            member=member,
            due_date=timezone.localdate() + timedelta(days=14)
        )

    return redirect("book_list")
