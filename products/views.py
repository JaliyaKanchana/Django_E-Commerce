from django.core import paginator
from django.db.models import query
import products
from django.shortcuts import render, redirect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

# Create your views here.

from . models import Product
from . forms import ProductFrom




def ShowAllProducts(request):
    products = Product.objects.filter(is_published=True).order_by('-price')

    page_num = request.GET.get("page")

    paginator = Paginator(products, 3)

    try:
        products = paginator.page(page_num)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)


    number_of_products = Product.objects.all().count()
    print('Number of Products',number_of_products)

    context = {
        'products' : products
    }

    return render(request, 'showProducts.html', context)

def productDetail(request, pk):

    eachproduct = Product.objects.get(id=pk)
    

    context = {

        'eachproduct' : eachproduct

    }
    return render(request, 'productDetail.html', context)



def addProduct(request):
        form = ProductFrom()

        if request.method == 'POST':
            form = ProductFrom(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect('showProducts')
        else:
            form = ProductFrom()

        context ={
            "form":form
        }

        return render(request, 'addProduct.html', context)


def updateProduct(request,pk):
        product = Product.objects.get(id=pk)

        form = ProductFrom(instance=product)

        if request.method == 'POST':
            form = ProductFrom(request.POST, request.FILES, instance=product)
            if form.is_valid():
                form.save()
                return redirect('showProducts')

        context ={
            "form":form
        }

        return render(request, 'updateProduct.html', context)

def deleteProduct(request, pk):
    product =Product.objects.get(id=pk)
    product.delete()
    return redirect('showProducts')


def searchBar(request):
    if request.method == 'GET':
        query = request.GET.get('query')
        if query:
            products = Product.objects.filter(name__icontains=query)
            return render(request, 'searchbar.html', {'products': products})
        else:
            print("No information to show")
            return request(request, 'searchbar.html',{})

