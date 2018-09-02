# coding: utf-8
from common.utils import render_to


@render_to('fmv/index.html')
def index(request):
    return {}
