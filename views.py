from hands_framework.templator import render
from patterns.creational_patterns import Engine


site = Engine()




# контроллер 404
class NotFound404:
    def __call__(self, request):
        return '404 WHAT', '404 PAGE Not Found'
    

class Index:
    def __call__(self, request):
        return '200 OK', render('index.html', date=request.get('date', None), objects_list=site.categories )


class About:
    def __call__(self, request):
        return '200 OK', 'about'
    
class Contacts:
    def __call__(self, request):
        return '200 OK', render('contacts.html', data=request.get('date', None), key=request.get('key', None))
    
class Basket:
    def __call__(self, request):
        return '200 OK', render('basket.html', data=request.get('date', None), key=request.get('key', None))


# контроллер - список продуктов
class ProductsList:
    def __call__(self, request):
        # logger.log('Список курсов')
        try:
            category = site.find_category_by_id(
                int(request['request_params']['id']))
            return '200 OK', render('product_list.html',
                                    objects_list=category.products,
                                    name=category.name, id=category.id)
        except KeyError:
            return '200 OK', 'No products have been added yet'


# контроллер - создать продукт
class CreateProduct:
    category_id = -1

    def __call__(self, request):
        if request['method'] == 'POST':
            # метод пост
            data = request['data']

            name = data['name']
            name = site.decode_value(name)

            category = None
            if self.category_id != -1:
                category = site.find_category_by_id(int(self.category_id))

                product = site.create_product('record', name, category)
                site.products.append(product)

            return '200 OK', render('product_list.html',
                                    objects_list=category.products,
                                    name=category.name,
                                    id=category.id)

        else:
            try:
                self.category_id = int(request['request_params']['id'])
                category = site.find_category_by_id(int(self.category_id))

                return '200 OK', render('create_product.html',
                                        name=category.name,
                                        id=category.id)
            except KeyError:
                return '200 OK', 'No categories have been added yet'


# контроллер - создать категорию
class CreateCategory:
    def __call__(self, request):
        
        if request['method'] == 'POST':
            # метод пост

            data = request['data']

            name = data['name']
            name = site.decode_value(name)

            category_id = data.get('category_id')

            category = None
            if category_id:
                category = site.find_category_by_id(int(category_id))

            new_category = site.create_category(name, category)

            site.categories.append(new_category)

            return '200 OK', render('index.html', objects_list=site.categories)
        else:
            categories = site.categories
            return '200 OK', render('create_category.html',
                                    categories=categories)


# контроллер - список категорий
class CategoryList:
    def __call__(self, request):
        # logger.log('Список категорий')
        return '200 OK', render('category_list.html',
                                objects_list=site.categories)