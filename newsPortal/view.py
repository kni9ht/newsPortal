from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls.conf import path
import pandas as pd
from pymongo import MongoClient
import json


def web(request):
    return render(request, 'index.html')


def load(request):
    return render(request, 'load.html')


def link(request):
    url = request.POST['link']
    path = path = 'https://drive.google.com/uc?export=download&id=' + \
        url.split('/')[-2]
    df = pd.read_csv(path)
    data = df.to_dict('records')
    client = MongoClient(
        "<Mongo client id>")
    db = client.get_database('<Database name>')
    record = db.<Collection name>
    record.insert_many(data, ordered=False)
    return redirect(request.META['HTTP_REFERER'])
