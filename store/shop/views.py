from django.shortcuts import render, get_object_or_404
from .models import Category, Book
from django.urls import reverse_lazy
from django.core.paginator import Paginator,EmptyPage,InvalidPage
from .forms import BookForm
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic import ListView, DetailView
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User, Group


# Create your views here.

def book_detail(request, category_id, book_id):
    
    try:
        book = Book.objects.get(category_id=category_id, id=book_id)
    except Exception as e:
        raise e

    return render(request, 'shop/book.html', {'book':book})



def allBookCat(request, category_id=None):


    managerCheck = False

    if request.user.groups.filter(name="Manager").exists() == True:
        managerCheck = True
        
    c_page = None
    books = None
    if category_id != None:
        c_page = get_object_or_404(Category, id=category_id)
        books = Book.objects.filter(category=c_page, availible=True) 
    else:
        books = Book.objects.all().filter(availible=True)
    
    print(books[0].category_id)
    print(books[0].category.pk)
    
    paginator = Paginator(books,6)
    try:
        page = int(request.GET.get('page','1'))
    except:
        page = 1
    try:
        books = paginator.page(page)
    except (EmptyPage,InvalidPage):
        books = paginator.page(paginator.num_pages)



    return render(request, 'shop/category.html', {'category':c_page,'books':books, 'managerCheck':managerCheck})



def managerCreateView(request):
    
    books = Book.objects.all().filter(availible=True)

    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('')

    else:
        form = BookForm()

    return render(request, 'shop/book_new.html', {'form':form})

class ManagerCreateView(CreateView):
    model = Book
    fields = '__all__'
    template_name = "shop/book_new.html"


class BookListView(ListView):
    model = Book
    template_name = 'shop/book_list.html'


class BookUpdateView(UpdateView):
    model = Book
    fields='__all__'
    template_name = 'shop/book_edit.html'

def bookUpdateView(request, category_id, book_id):
    book = Book.objects.get(category_id=category_id, id=book_id)

    
    form = BookForm(request.POST or None, request.FILES or None , instance = book)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect('/')

    return render(request, 'shop/book_edit.html', {'form':form})



def bookDeleteView(request, category_id, book_id):
    book = Book.objects.get(category_id=category_id, id=book_id)

    
    if request.method =="POST":
        book.delete()
        return HttpResponseRedirect('/')

    return render(request, 'shop/book_delete.html', {'book':book})



    

class BookDeleteView(DeleteView):
    model = Book
    fields='__all__'
    template_name = 'shop/book_delete.html'
    success_url = reverse_lazy('book_list')