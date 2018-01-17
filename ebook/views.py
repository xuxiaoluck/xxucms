from django.http import HttpResponse
from django.shortcuts import render_to_response

def index(request):
    '''进行书籍首页'''
    return render_to_response('ebindex.html',{})


def addbooks(request):
    '''增加书籍'''
    return render_to_response('addbooks.html',{})




