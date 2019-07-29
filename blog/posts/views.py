from django.shortcuts import render
from django.http import HttpResponse, HttpRequest


def index(request: HttpRequest):
    """Returns posts' list"""
    return HttpResponse("Hello, world. You're at the polls index.")


def about(request: HttpRequest):
    """Returns author about page"""
    return HttpResponse('about')


def read(request: HttpRequest, post_id: int):
    """Shows selected post by its id"""
    return HttpResponse('read')


def comment_add(request: HttpRequest, post_id: int):
    """Adds new comment for a post"""
    return HttpResponse('comment_add')
