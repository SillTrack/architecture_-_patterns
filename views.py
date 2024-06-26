from hands_framework.templator import render
from patterns.creational_patterns import Engine, MapperRegistry

from patterns.structural_patterns import AppRoute, Debug
from patterns.behavioral_patterns import EmailNotifier, SmsNotifier, \
    ListView, CreateView, BaseSerializer

from patterns.architectural_system_pattern_unit_of_work import UnitOfWork

site = Engine()
email_notifier = EmailNotifier()
sms_notifier = SmsNotifier()
UnitOfWork.new_current()
UnitOfWork.get_current().set_mapper_registry(MapperRegistry)



routes = {}


# контроллер 404
class NotFound404:
    def __call__(self, request):
        return '404 WHAT', '404 PAGE Not Found'
    
@AppRoute(routes=routes, url='/')
class Index:
    def __call__(self, request):
        return '200 OK', render('index.html', date=request.get('date', None), objects_list=site.categories )

@AppRoute(routes=routes, url='/about/')
class About:
    def __call__(self, request):
        return '200 OK', 'about'

@AppRoute(routes=routes, url='/contacts/')
class Contacts:
    def __call__(self, request):
        return '200 OK', render('contacts.html', data=request.get('date', None), key=request.get('key', None))

@AppRoute(routes=routes, url='/basket/')
class Basket:
    def __call__(self, request):
        return '200 OK', render('basket.html', data=request.get('date', None), key=request.get('key', None))


# контроллер - список продуктов
@AppRoute(routes=routes, url='/product-list/')
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
@AppRoute(routes=routes, url='/create-product/')
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

                product = site.create_product('usual', name, category)

                product.observers.append(sms_notifier)
                product.observers.append(email_notifier)
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
@AppRoute(routes=routes, url='/create-category/')
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
@AppRoute(routes=routes, url='/category-list/')
class CategoryList:
    def __call__(self, request):
        # logger.log('Список категорий')
        return '200 OK', render('category_list.html',
                                objects_list=site.categories)
    



@AppRoute(routes=routes, url='/customer-list/')
class StudentListView(ListView):
    template_name = 'customer_list.html'

    def get_queryset(self):
        mapper = MapperRegistry.get_current_mapper('customer')
        return mapper.all()


@AppRoute(routes=routes, url='/create-customer/')
class UserCreateView(CreateView):
    template_name = 'create_customer.html'

    def create_obj(self, data: dict):
        name = data['name']
        name = site.decode_value(name)
        new_obj = site.create_user('customer', name)
        site.customers.append(new_obj)
        new_obj.mark_new()
        UnitOfWork.get_current().commit()

@AppRoute(routes=routes, url='/add-favoroutes/')
class AddStudentByCourseCreateView(CreateView):
    template_name = 'add_favoroutes.html'

    def get_context_data(self):
        context = super().get_context_data()
        context['products'] = site.products
        context['customers'] = site.customers
        return context

    def create_obj(self, data: dict):

        print(data)
        product_name = data['product_name']
        product_name = site.decode_value(product_name)
        product = site.get_product(product_name)
        customer_name = data['customer_name']
        customer_name = site.decode_value(customer_name)
        customer = site.get_customer(customer_name)
        product.add_customer(customer)

