from django.contrib.auth import login
from django.db.models import Q # django database filters
from django.shortcuts import redirect, render

from .forms import RegisterForm
from .models import Book, Category, Member


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
