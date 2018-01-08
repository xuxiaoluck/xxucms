from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render_to_response


def index(request):
    """打开hiddendange首页"""
    return render_to_response('hdindex.html',{})






