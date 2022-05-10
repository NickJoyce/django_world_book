from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseNotFound
from .models import Author, Book, Genre, Language, Status, BookInstance
from .forms import AuthorsForm

from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy


def index(request):
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    data = dict(num_books = Book.objects.all().count(),
                num_instances = BookInstance.objects.all().count(),
                num_instances_available = BookInstance.objects.filter(status__name='На складе').count(),
                num_authors = Author.objects.all().count(),
                num_visits = request.session['num_visits'])

    return render(request, 'index.html', data)

def authors_add(request):
    data = dict(author = Author.objects.all(),
                form = AuthorsForm()
    )
    return render(request, 'catalog/authors_add.html', data)

def create_author(request):
    if request.method == 'POST':
        author = Author()
        author.first_name = request.POST.get('first_name')
        author.last_name = request.POST.get('last_name')
        author.date_of_birth = request.POST.get('date_of_birth')
        author.date_of_death = request.POST.get('date_of_death')
        author.save()
        return redirect(authors_add)

def delete_author(request, id):
    try:
        author = Author.objects.get(id=id)
        author.delete()
        return redirect(authors_add)
    except Author.DoesNotExist:
        return HttpResponseNotFound('<h2>Файл не найден</h2>')

def edit_author(request, id):
    author = Author.objects.get(id=id)
    if request.method == 'POST':
        author.first_name = request.POST.get('first_name')
        author.last_name = request.POST.get('last_name')
        author.date_of_birth = request.POST.get('date_of_birth')
        author.date_of_death = request.POST.get('date_of_death')
        author.save()
        return redirect(authors_add)
    else:
        author.date_of_birth = str(author.date_of_birth)
        author.date_of_death = str(author.date_of_death)
        data = dict(author = author)
        return render(request, 'edit_author.html', data)


class BookCreate(CreateView):
    model = Book
    fields = '__all__'
    success_url = reverse_lazy('books')

class BookUpdate(UpdateView):
    model = Book
    fields = '__all__'
    success_url = reverse_lazy('books')

class BookDelete(DeleteView):
    model = Book
    success_url = reverse_lazy('books')





class BookListView(ListView):
    model = Book
    paginate_by = 4

class BookDetailView(DetailView):
    model = Book

class AuthorListView(ListView):
    model = Author
    paginate_by = 4

class AuthorDetailView(DetailView):
    model = Author

class LoanedBooksByUserListView(LoginRequiredMixin, ListView):
    """
    Универсальный класс представления списка книг,
    находящихся в заказе у текущего пользователя
    """
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):

        return BookInstance.objects.filter(
               borrower=self.request.user).filter(status__name='В заказе').order_by('due_back')

