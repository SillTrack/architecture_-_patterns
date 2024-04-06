from datetime import date
from views import Index, About, Basket, Contacts, CategoryList, CreateCategory
from views import ProductsList, CreateProduct


# front controller
def secret_front(request):
    request['date'] = date.today()


def other_front(request):
    request['key'] = 'key'


fronts = [secret_front, other_front]

routes = {
    '/': Index(),
    '/about/': About(),
    '/contacts/': Contacts(),
    '/basket/': Basket(),
    '/create-category/': CreateCategory(),
    '/category-list/': CategoryList(),
    '/create-product/': CreateProduct(),
    '/product-list/': ProductsList(),
}
