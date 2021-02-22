from os import error
from re import search
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from dns.tsig import Key
from pymongo import MongoClient
from bson import ObjectId


def index(request):
    return render(request, 'news.html')


def query(request):
    search = request.GET.get('search')
    no = request.GET.get('no')
    cat = request.GET.get('cat')
    if not cat:
        cat = search
    search1 = search+'.*'
    print(cat)
    print(search)
    client = MongoClient(
        'mongodb+srv://kni9ht:iamHunter@cr47.ycngh.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
    db = client.get_database('exel')
    record = db.csv_data
    tags = list(record.find_one({}))
    # This code search for the phrase in the database
    for tag in tags:
        results = record.find_one({tag: cat})
        key = tag
        if results:
            break
    # This code search for the partial phrase in the database
    for tag in tags:
        result = record.find_one({tag: {"$regex": search1, "$options": 'i'}})
        key1 = tag
        if result:
            break
    result_of_search = record.find_one(
        {"$or":   [{key: cat},   {key1: {"$regex": search1, "$options": 'i'}}]})
    if not result_of_search:
        state = "Sorry the result is not found ..!"
    else:
        state = 0
    if request.method == "GET":
        return render(request, 'news.html', {'data': result_of_search, 'state': state})
    else:
        return redirect(request.META['HTTP_REFERER'])
