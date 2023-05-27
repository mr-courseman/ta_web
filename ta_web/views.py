import io
import json
import xlsxwriter

from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator
from django.core.serializers import serialize
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView

from ta_web.decorators import *
from ta_web.forms import *
from ta_web.filters import *


def error_404_view(request, exception):
    return render(request, 'ta_web/ta_web_errors/404.html')


def error_500_view(request):
    return render(request, 'ta_web/ta_web_errors/500.html')


def get_user_role(request):
    tmp = request.user.groups.all()
    if tmp:
        return str(tmp[0])
    else:
        return 'Guest'


def get_xlsx(request, qset, columns, ws_name):
    output = io.BytesIO()

    filename = f'current-{ws_name}.xlsx'
    workbook = xlsxwriter.Workbook(output, {'in_memory': True, 'default_date_format': 'yyyy/mm/dd',
                                            'time_format': 'hh:mm', 'remove_timezone': True})
    worksheet = workbook.add_worksheet(ws_name)

    row_num = 0
    for col_num in range(len(columns)):
        worksheet.write(row_num, col_num, columns[col_num])

    rows = qset.order_by(columns[0]).values_list(*columns)

    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            worksheet.write(row_num, col_num, row[col_num])

    workbook.close()
    output.seek(0)

    response = HttpResponse(output.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename={filename}'

    output.close()

    return response


def get_json(request, items_list, filename):
    serialized_items = serialize('json', items_list)
    print(serialized_items)

    with open(filename, 'w') as f:
        jsoned = json.loads(serialized_items)
        json.dump(jsoned, f, indent=2, ensure_ascii=False)

    response = HttpResponse(serialized_items, content_type='application/json')
    response['Content-Disposition'] = f'attachment; filename={filename}'

    return response


@login_required()
def get_entities_xlsx(request, etype):
    role = get_user_role(request)
    columns = None
    entities = None
    placeholder = None

    if role == 'Admin':
        if etype == 'managers':
            entities = Personal.objects.filter(groups__name='Manager').order_by('id')
            columns = ['username', 'email', 'phone', 'last_name', 'first_name', 'patronymic']
            placeholder = 'Менеджеры'
        elif etype == 'sellers':
            entities = Personal.objects.filter(groups__name='Seller').order_by('id')
            columns = ['username', 'email', 'phone', 'last_name', 'first_name', 'patronymic']
            placeholder = 'Продавцы'
        elif etype == 'tours':
            entities = Tour.objects.all().order_by('id')
            columns = [f.name for f in Tour._meta.get_fields()]
            placeholder = 'Туры'
        elif etype == 'movements':
            entities = Movement.objects.all().order_by('id')
            columns = [f.name for f in Movement._meta.get_fields()]
            placeholder = 'Путешествия'
        elif etype == 'clients':
            entities = Client.objects.order_by('id')
            columns = ['username', 'email', 'phone', 'last_name', 'first_name', 'patronymic', 'birthday', 'passport']
            placeholder = 'Клиенты'
        elif etype == 'contracts':
            entities = Contract.objects.all().order_by('time')
            columns = [f.name for f in Contract._meta.get_fields()]
            placeholder = 'Контракты'
        else:
            raise Http404
    elif role == 'Manager':
        if etype == 'sellers':
            entities = Personal.objects.filter(groups__name='Seller').order_by('id')
            columns = ['username', 'email', 'phone', 'last_name', 'first_name', 'patronymic']
            placeholder = 'Продавцы'
        elif etype == 'tours':
            entities = Tour.objects.all().order_by('id')
            columns = [f.name for f in Tour._meta.get_fields()]
            placeholder = 'Туры'
        elif etype == 'movements':
            entities = Movement.objects.all().order_by('id')
            columns = [f.name for f in Movement._meta.get_fields()]
            placeholder = 'Путешествия'
        else:
            raise Http404
    elif role == 'Seller':
        if etype == 'clients':
            entities = Client.objects.order_by('id')
            columns = ['username', 'email', 'phone', 'last_name', 'first_name', 'patronymic', 'birthday', 'passport']
            placeholder = 'Клиенты'
        elif etype == 'tours':
            entities = Tour.objects.all().order_by('cost')
            columns = [f.name for f in Tour._meta.get_fields()]
            placeholder = 'Туры'
        elif etype == 'contracts':
            entities = Contract.objects.filter(seller=request.user).order_by('time')
            columns = [f.name for f in Contract._meta.get_fields()]
            placeholder = 'Контракты'
        else:
            raise Http404

    return get_xlsx(request, entities, columns, ws_name=placeholder)


@login_required()
@allowed_roles(['Admin'])
def get_entities_json(request, etype):
    entities_list = None
    filename = None

    if etype == 'managers':
        entities_list = Personal.objects.filter(groups__name='Manager').order_by('id')
        filename = 'Менеджеры'
    elif etype == 'sellers':
        entities_list = Personal.objects.filter(groups__name='Seller').order_by('id')
        filename = 'Продавцы'
    elif etype == 'tours':
        entities_list = Tour.objects.all().order_by('id')
        filename = 'Туры'
    elif etype == 'clients':
        entities_list = Client.objects.order_by('id')
        filename = 'Клиенты'
    elif etype == 'contracts':
        entities_list = Contract.objects.order_by('-time')
        filename = 'Контракты'
    elif etype == 'movements':
        entities_list = Movement.objects.order_by('-d_time')
        filename = 'Путешествия'
    else:
        raise Http404

    return get_json(request, entities_list, filename)


def index(request):
    context = {
        'role': get_user_role(request),
    }

    return render(request, 'ta_web/index.html', context=context)


def about(request):
    return render(request, 'ta_web/about.html')


def feedback(request):
    return render(request, 'ta_web/feedback.html')


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'ta_web/ta_web_auth_stuff/registration.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save()
        user.groups.add(Group.objects.get(name='Client'))
        login(self.request, user)
        return redirect('home')


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'ta_web/ta_web_auth_stuff/login.html'
    redirect_authenticated_user = reverse_lazy('home')

    def get_success_url(self):
        return reverse_lazy('home')


@login_required
def logout_user(request):
    logout(request)
    return redirect('home')


class Profile(View):
    @staticmethod
    @login_required
    def get(request):
        context = {
            'role': get_user_role(request),
            'form': None,
        }
        if context['role'] != 'Client':
            context['form'] = PersonalForm(instance=Personal.objects.get(id=request.user.pk))
        else:
            context['form'] = get_client_form(Client.objects.get(id=request.user.pk))

        return render(request, 'ta_web/ta_web_auth_stuff/profile.html', context=context)


class ProfileUpdate(View):
    @staticmethod
    @login_required
    @allowed_roles(['Admin', 'Manager', 'Seller'])
    def get(request):
        context = {
            'form': PersonalForm(instance=Personal.objects.get(id=request.user.pk))
        }
        return render(request, 'ta_web/ta_web_auth_stuff/profile_update.html', context=context)

    @staticmethod
    @login_required
    @allowed_roles(['Admin', 'Manager', 'Seller'])
    def post(request):
        context = {
            'form': PersonalForm(request.POST, instance=Personal.objects.get(id=request.user.pk))
        }

        if context['form'].is_valid():
            context['form'].save()
            return redirect('profile')
        else:
            return render(request, 'ta_web/ta_web_auth_stuff/profile_update.html', context=context)


@login_required
@allowed_roles(['Client'])
def profile_delete(request):
    Client.objects.get(id=request.user.pk).delete()
    return redirect('home')


# if etype == 'passports':
#     entities = Passport.objects.all().order_by('id')
#     # filter_ = Filter(request.GET, queryset=entities)
# elif etype == 'clients':
#     entities = Client.objects.all().order_by('id')
#     # filter_ = Filter(request.GET, queryset=entities)
# elif etype == 'personals':
#     entities_ = Personal.objects.all().order_by('id')
#     # filter_ = Filter(request.GET, queryset=entities)
# elif etype == 'places':
#     entities = Place.objects.all().order_by('id')
#     # filter_ = Filter(request.GET, queryset=entities)
# elif etype == 'movements':
#     entities = Movement.objects.all().order_by('id')
#     # filter_ = Filter(request.GET, queryset=entities)
# elif etype == 'tours':
#     entities = Tour.objects.all().order_by('id')
#     # filter_ = Filter(request.GET, queryset=entities)
# elif etype == 'contracts':
#     entities = Contract.objects.all().order_by('id')
#     # filter_ = Filter(request.GET, queryset=entities)
# else:
#     raise Http404


def pagination(queryset, pgs, pgn, role, filter_=None):
    paginator = Paginator(queryset, per_page=pgs)
    page_obj = None
    page_number = None

    if not pgn:
        page_number = 1
    else:
        page_number = pgn

    page_obj = paginator.get_page(page_number)
    page_obj.adjusted_elided_pages = paginator.get_elided_page_range(page_number)

    return {
        'page_obj': page_obj,
        'filter_': filter_,
        'role': role,
    }


class ClientsList(View):
    @staticmethod
    @login_required
    @allowed_roles(['Admin', 'Seller'])
    def get(request):
        context_ = pagination(
            queryset=Client.objects.order_by('id'),
            pgs=5,
            pgn=request.GET.get('page', None),
            role=get_user_role(request),
            filter_=None  # ClientsFilter(request.GET, queryset=clients),
        )

        return render(request, 'ta_web/ta_web_models_list/clients.html', context=context_)


class SellersList(View):
    @staticmethod
    @login_required
    @allowed_roles(['Admin', 'Manager'])
    def get(request):
        context_ = pagination(
            queryset=Personal.objects.filter(groups__name='Seller').order_by('id'),
            pgs=5,
            pgn=request.GET.get('page', None),
            role=get_user_role(request),
            filter_=None  # SellersFilter(request.GET, queryset=sellers)
        )

        return render(request, 'ta_web/ta_web_models_list/sellers.html', context=context_)


class ToursList(View):
    @staticmethod
    @login_required
    def get(request):
        context_ = pagination(
            queryset=Tour.objects.order_by('movement__d_time'),
            pgs=3,
            pgn=request.GET.get('page', None),
            role=get_user_role(request),
            filter_=None  # ToursFilter(request.GET, queryset=tours)
        )

        return render(request, f'ta_web/ta_web_models_list/tours.html', context=context_)


class MovementsList(View):
    @staticmethod
    @login_required
    @allowed_roles(['Admin', 'Manager'])
    def get(request):
        context_ = pagination(
            queryset=Movement.objects.order_by('id'),
            pgs=3,
            pgn=request.GET.get('page', None),
            role=get_user_role(request),
            filter_=None  # MovementsFilter(request.GET, queryset=movements)
        )

        return render(request, f'ta_web/ta_web_models_list/movements.html', context=context_)


class ContractsList(View):
    @staticmethod
    @login_required
    @allowed_roles(['Admin', 'Seller'])
    def get(request):
        context_ = pagination(
            queryset=Contract.objects.order_by('-id'),
            pgs=3,
            pgn=request.GET.get('page', None),
            role=get_user_role(request),
            filter_=None  # ContractsFilter(request.GET, queryset=contracts)
        )

        return render(request, f'ta_web/ta_web_models_list/contracts.html', context=context_)


class ClientToursList(View):
    @staticmethod
    @login_required
    @allowed_roles(['Client'])
    def get(request):
        contracts = Contract.objects.filter(client=request.user.pk).order_by('tour__movement__d_city')
        tours = []
        for contract in contracts:
            tours.append(contract.tour)

        context_ = pagination(
            queryset=tours,
            pgs=3,
            pgn=request.GET.get('page', None),
            role=get_user_role(request),
            filter_=None  # ToursFilter(request.GET, queryset=tours)
        )

        return render(request, f'ta_web/ta_web_models_list/tours.html', context=context_)


class ClientMovementsList(View):
    @staticmethod
    @login_required
    @allowed_roles(['Client'])
    def get(request):
        contracts = Contract.objects.filter(client=request.user.pk).order_by('tour__movement__d_city')
        movements = []
        for contract in contracts:
            movements.append(contract.tour.movement)

        context_ = pagination(
            queryset=movements,
            pgs=3,
            pgn=request.GET.get('page', None),
            role=get_user_role(request),
            filter_=None  # MovementsFilter(request.GET, queryset=movements)
        )

        return render(request, f'ta_web/ta_web_models_list/movements.html', context=context_)


class ClientShow(View):
    @staticmethod
    @login_required
    @allowed_roles(['Admin', 'Seller'])
    def get(request, pk):
        context_ = {
            'id': pk,
            'form': get_client_form(Client.objects.get(id=pk)),
            'placeholder': 'Клиента',
            'role': get_user_role(request)
        }

        return render(request, 'ta_web/ta_web_models_show/client.html', context=context_)


class SellerShow(View):
    @staticmethod
    @login_required
    @allowed_roles(['Admin', 'Manager'])
    def get(request, pk):
        context_ = {
            'id': pk,
            'form': PersonalForm(instance=Personal.objects.get(id=pk)),
            'placeholder': 'Продавца',
            'role': get_user_role(request)
        }
        return render(request, 'ta_web/ta_web_models_show/seller.html', context=context_)


class TourShow(View):
    @staticmethod
    @login_required
    def get(request, pk):
        context_ = {
            'id': pk,
            'form': get_tour_form(Tour.objects.get(id=pk)),
            'placeholder': 'Тура',
            'role': get_user_role(request)
        }

        return render(request, 'ta_web/ta_web_models_show/tour.html', context=context_)


class MovementShow(View):
    @staticmethod
    @login_required
    @allowed_roles(['Admin', 'Manager', 'Client'])
    def get(request, pk):
        context_ = {
            'id': pk,
            'form': MovementForm(instance=Movement.objects.get(id=pk)),
            'placeholder': 'Путешествия',
            'role': get_user_role(request)
        }

        return render(request, 'ta_web/ta_web_models_show/movement.html', context=context_)


class ContractShow(View):
    @staticmethod
    @login_required
    @allowed_roles(['Admin', 'Seller'])
    def get(request, pk):
        context_ = {
            'id': pk,
            'form': ContractForm(instance=Contract.objects.get(id=pk)),
            'placeholder': 'Контракта',
            'role': get_user_role(request)
        }

        return render(request, 'ta_web/ta_web_models_show/movement.html', context=context_)


class ClientTourShow(View):
    @staticmethod
    @login_required
    @allowed_roles(['Client'])
    def get(request, pk):
        context_ = {
            'id': pk,
            'form': TourForm(Contract.objects.filter(client=request.user.pk, tour=pk)[0].tour),
            'placeholder': 'Тура',
            'role': get_user_role(request)
        }

        return render(request, 'ta_web/ta_web_models_show/tour.html', context=context_)


class ClientMovementShow(View):
    @staticmethod
    @login_required
    @allowed_roles(['Client'])
    def get(request, pk):
        context_ = {
            'id': pk,
            'form': MovementForm(Contract.objects.filter(client=request.user.pk, tour=pk)[0].tour.movement),
            'placeholder': 'Путешествия',
            'role': get_user_role(request)
        }

        return render(request, 'ta_web/ta_web_models_show/movement.html', context=context_)


class ClientAdd(View):
    @staticmethod
    @login_required
    @allowed_roles(['Admin', 'Seller'])
    def get(request):
        context_ = {
            'form': RegisterUserForm(),
            'placeholder': 'Клиента',
        }

        return render(request, 'ta_web/ta_web_models_add/client_add.html', context=context_)

    @staticmethod
    @login_required
    @allowed_roles(['Admin', 'Seller'])
    def post(request):
        context_ = {
            'form': RegisterUserForm(request.POST),
            'placeholder': 'Клиента',
        }
        context_['form'].full_clean()

        if context_['form'].is_valid():
            person = context_['form'].save()
            person.groups.add(Group.objects.get(name='Client'))
            return redirect('home')
        else:
            return render(request, 'ta_web/ta_web_models_add/client_add.html', context=context_)


class SellerAdd(View):
    @staticmethod
    @login_required
    @allowed_roles(['Admin', 'Manager'])
    def get(request):
        context_ = {
            'form': RegisterPersonalForm(),
            'placeholder': 'Продавца',
        }

        return render(request, 'ta_web/ta_web_models_add/seller_add.html', context=context_)

    @staticmethod
    @login_required
    @allowed_roles(['Admin', 'Manager'])
    def post(request):
        context_ = {
            'form': RegisterPersonalForm(request.POST),
            'placeholder': 'Продавца',
        }
        context_['form'].full_clean()

        if context_['form'].is_valid():
            person = context_['form'].save()
            person.groups.add(Group.objects.get(name='Seller'))
            return redirect('home')
        else:
            return render(request, 'ta_web/ta_web_models_add/seller_add.html', context=context_)


class TourAdd(View):
    @staticmethod
    @login_required
    @allowed_roles(['Admin', 'Manager'])
    def get(request):
        context_ = {
            'form': TourForm(),
            'placeholder': 'Тура',
        }

        return render(request, 'ta_web/ta_web_models_add/tour_add.html', context=context_)

    @staticmethod
    @login_required
    @allowed_roles(['Admin', 'Manager'])
    def post(request):
        context_ = {
            'form': TourForm(request.POST),
            'placeholder': 'Тура',
        }

        if context_['form'].is_valid():
            context_['form'].save()
            return redirect('home')
        else:
            return render(request, 'ta_web/ta_web_models_add/tour_add.html', context=context_)


class ContractAdd(View):
    @staticmethod
    @login_required
    @allowed_roles(['Admin', 'Seller'])
    def get(request):
        context_ = {
            'form': ContractForm(),
            'placeholder': 'Контракта',
        }

        return render(request, 'ta_web/ta_web_models_add/contract_add.html', context=context_)

    @staticmethod
    @login_required
    @allowed_roles(['Admin', 'Seller'])
    def post(request):
        context_ = {
            'form': ContractForm(request.POST),
            'placeholder': 'Контракта',
        }
        context_['form'].full_clean()

        if context_['form'].is_valid():
            context_['form'].save()
            return redirect('home')
        else:
            return render(request, 'ta_web/ta_web_models_add/contract_add.html', context=context_)


class MovementAdd(View):
    @staticmethod
    @login_required
    @allowed_roles(['Admin', 'Manager'])
    def get(request):
        context_ = {
            'form': MovementForm(),
            'placeholder': 'Путешествия',
        }

        return render(request, 'ta_web/ta_web_models_add/movement_add.html', context=context_)

    @staticmethod
    @login_required
    @allowed_roles(['Admin', 'Manager'])
    def post(request):
        context_ = {
            'form': MovementForm(request.POST),
            'placeholder': 'Путешествия',
        }

        if context_['form'].is_valid():
            context_['form'].save()
            return redirect('home')
        else:
            return render(request, 'ta_web/ta_web_models_add/movement_add.html', context=context_)


class ClientUpdate(View):
    @staticmethod
    @login_required
    @allowed_roles(['Admin', 'Seller'])
    def get(request, pk):
        context_ = {
            'form': get_client_form(Client.objects.get(id=pk)),
            'id': pk,
            'role': get_user_role(request),
            'placeholder': 'Клиента',
        }
        return render(request, 'ta_web/ta_web_models_update/client_update.html', context=context_)

    @staticmethod
    @login_required
    @allowed_roles(['Admin', 'Seller'])
    def post(request, pk):
        context_ = {
            'form': ClientForm(request.POST, instance=Client.objects.get(id=pk)),
            'id': pk,
            'role': get_user_role(request),
            'placeholder': 'Клиента',
        }

        if context_['form'].is_valid():
            context_['form'].save()
            return redirect('client', pk)
        else:
            return render(request, 'ta_web/ta_web_models_update/client_update.html', context=context_)


class SellerUpdate(View):
    @staticmethod
    @login_required
    @allowed_roles(['Admin', 'Manager'])
    def get(request, pk):
        context_ = {
            'form': PersonalForm(instance=Personal.objects.get(id=pk)),
            'id': pk,
            'role': get_user_role(request),
            'placeholder': 'Продавца',
        }
        return render(request, 'ta_web/ta_web_models_update/seller_update.html', context=context_)

    @staticmethod
    @login_required
    @allowed_roles(['Admin', 'Manager'])
    def post(request, pk):
        context_ = {
            'form': PersonalForm(request.POST, instance=Personal.objects.get(id=pk)),
            'id': pk,
            'role': get_user_role(request),
            'placeholder': 'Продавца',
        }

        if context_['form'].is_valid():
            context_['form'].save()
            return redirect('seller', pk)
        else:
            return render(request, 'ta_web/ta_web_models_update/seller_update.html', context=context_)


class TourUpdate(View):
    @staticmethod
    @login_required
    @allowed_roles(['Admin', 'Manager'])
    def get(request, pk):
        context_ = {
            'form': get_tour_form(Tour.objects.get(id=pk)),
            'id': pk,
            'role': get_user_role(request),
            'placeholder': 'Тура',
        }
        return render(request, 'ta_web/ta_web_models_update/tour_update.html', context=context_)

    @staticmethod
    @login_required
    @allowed_roles(['Admin', 'Manager'])
    def post(request, pk):
        context_ = {
            'form': TourForm(request.POST, instance=Tour.objects.get(id=pk)),
            'id': pk,
            'role': get_user_role(request),
            'placeholder': 'Тура',
        }

        if context_['form'].is_valid():
            context_['form'].save()
            return redirect('tour', pk)
        else:
            return render(request, 'ta_web/ta_web_models_update/tour_update.html', context=context_)


class ContractUpdate(View):
    @staticmethod
    @login_required
    @allowed_roles(['Admin', 'Seller'])
    def get(request, pk):
        context_ = {
            'form': ContractForm(instance=Contract.objects.get(id=pk)),
            'id': pk,
            'role': get_user_role(request),
            'placeholder': 'Контракта',
        }
        return render(request, 'ta_web/ta_web_models_update/contract_update.html', context=context_)

    @staticmethod
    @login_required
    @allowed_roles(['Admin', 'Seller'])
    def post(request, pk):
        context_ = {
            'form': ContractForm(request.POST, instance=Contract.objects.get(id=pk)),
            'id': pk,
            'role': get_user_role(request),
            'placeholder': 'Контракта',
        }

        if context_['form'].is_valid():
            context_['form'].save()
            return redirect('tour', pk)
        else:
            return render(request, 'ta_web/ta_web_models_update/contract_update.html', context=context_)


class MovementUpdate(View):
    @staticmethod
    @login_required
    @allowed_roles(['Admin', 'Manager'])
    def get(request, pk):
        context_ = {
            'form': MovementForm(instance=Movement.objects.get(id=pk)),
            'id': pk,
            'role': get_user_role(request),
            'placeholder': 'Путешествия',
        }
        return render(request, 'ta_web/ta_web_models_update/movement_update.html', context=context_)

    @staticmethod
    @login_required
    @allowed_roles(['Admin', 'Manager'])
    def post(request, pk):
        context_ = {
            'form': MovementForm(request.POST, instance=Movement.objects.get(id=pk)),
            'id': pk,
            'role': get_user_role(request),
            'placeholder': 'Путешествия',
        }

        if context_['form'].is_valid():
            context_['form'].save()
            return redirect('movement', pk)
        else:
            return render(request, 'ta_web/ta_web_models_update/movement_update.html', context=context_)


class ClientDelete(View):
    @staticmethod
    @login_required
    @allowed_roles(['Admin', 'Seller'])
    def get(request, pk):
        Passport.objects.get(client=pk).delete()
        Client.objects.get(id=pk).delete()

        return redirect('clients')


class SellerDelete(View):
    @staticmethod
    @login_required
    @allowed_roles(['Admin', 'Manager'])
    def get(request, pk):
        Personal.objects.get(id=pk).delete()

        return redirect('sellers')


class TourDelete(View):
    @staticmethod
    @login_required
    @allowed_roles(['Admin', 'Manager'])
    def get(request, pk):
        Tour.objects.get(id=pk).delete()

        return redirect('tours')


class MovementDelete(View):
    @staticmethod
    @login_required
    @allowed_roles(['Admin', 'Manager'])
    def get(request, pk):
        Tour.objects.get(movement=id).delete()
        Movement.objects.get(id=pk).delete()

        return redirect('movements')


class ContractDelete(View):
    @staticmethod
    @login_required
    @allowed_roles(['Admin', 'Seller'])
    def get(request, pk):
        Contract.objects.get(id=pk).delete()

        return redirect('contracts')


class ManagersList(View):
    @staticmethod
    @login_required
    @allowed_roles(['Admin'])
    def get(request):
        context_ = pagination(
            queryset=Personal.objects.filter(groups__name='Manager').order_by('id'),
            pgs=5,
            pgn=request.GET.get('page', None),
            role=get_user_role(request),
            filter_=None  # MovementsFilter(request.GET, queryset=movements)
        )

        return render(request, f'ta_web/ta_web_models_list/managers.html', context=context_)


class ManagerShow(View):
    @staticmethod
    @login_required
    @allowed_roles(['Admin'])
    def get(request, pk):
        context_ = {
            'id': pk,
            'form': PersonalForm(instance=Personal.objects.get(id=pk)),
            'placeholder': 'Менеджера',
            'role': get_user_role(request)
        }

        return render(request, 'ta_web/ta_web_models_show/manager.html', context=context_)


class ManagerAdd(View):
    @staticmethod
    @login_required
    @allowed_roles(['Admin'])
    def get(request):
        context_ = {
            'form': RegisterPersonalForm(),
            'placeholder': 'Менеджера',
        }

        return render(request, 'ta_web/ta_web_models_add/manager_add.html', context=context_)

    @staticmethod
    @login_required
    @allowed_roles(['Admin'])
    def post(request):
        context_ = {
            'form': RegisterPersonalForm(request.POST),
            'placeholder': 'Менеджера',
        }
        context_['form'].full_clean()

        if context_['form'].is_valid():
            person = context_['form'].save()
            person.groups.add(Group.objects.get(name='Manager'))
            return redirect('home')
        else:
            return render(request, 'ta_web/ta_web_models_add/manager_add.html', context=context_)


class ManagerUpdate(View):
    @staticmethod
    @login_required
    @allowed_roles(['Admin'])
    def get(request, pk):
        context_ = {
            'form': PersonalForm(instance=Personal.objects.get(id=pk)),
            'id': pk,
            'role': get_user_role(request),
            'placeholder': 'Менеджера',
        }
        return render(request, 'ta_web/ta_web_models_update/manager_update.html', context=context_)

    @staticmethod
    @login_required
    @allowed_roles(['Admin'])
    def post(request, pk):
        context_ = {
            'form': PersonalForm(request.POST, instance=Personal.objects.get(id=pk)),
            'id': pk,
            'role': get_user_role(request),
            'placeholder': 'Менеджера',
        }

        if context_['form'].is_valid():
            context_['form'].save()
            return redirect('manager', pk)
        else:
            return render(request, 'ta_web/ta_web_models_update/manager_update.html', context=context_)


class ManagerDelete(View):
    @staticmethod
    @login_required
    @allowed_roles(['Admin'])
    def get(request, pk):
        Personal.objects.get(id=pk).delete()

        return redirect('managers')

# @periodic_task(run_every=crontab(minute='*/5'))
# def delete_old_movements_and_realtions():
#     d = timezone.now() - datetime.timedelta(hours=24)
#     #get expired orders
#     orders = CustomerOrder.objects.filter(timestamp__lt=d)
#     #delete them
#     orders.delete()
