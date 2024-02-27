from hands_framework.templator import render


class Index:
    def __call__(self, request):
        return '200 OK', render('index.html', date=request.get('date', None))


class About:
    def __call__(self, request):
        return '200 OK', 'about'
    
class Contacts:
    def __call__(self, request):
        return '200 OK', render('contacts.html', data=request.get('date', None), key=request.get('key', None))
    
class Basket:
    def __call__(self, request):
        return '200 OK', render('basket.html', data=request.get('date', None), key=request.get('key', None))
