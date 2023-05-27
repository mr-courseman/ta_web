from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='home'),
    path('about/', about, name='about'),
    path('feedback/', feedback, name='feedback'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),

    path('profile/', Profile.as_view(), name='profile'),
    path('profile/update/', ProfileUpdate.as_view(), name='profile_update'),
    path('profile/delete/', profile_delete, name='profile_delete'),

    path('clients/', ClientsList.as_view(), name='clients'),
    path('client/<int:pk>', ClientShow.as_view(), name='client'),
    path('client/add', ClientAdd.as_view(), name='client_add'),
    path('client/<int:pk>/update', ClientUpdate.as_view(), name='client_update'),
    path('client/<int:pk>/delete', ClientDelete.as_view(), name='client_delete'),

    path('sellers/', SellersList.as_view(), name='sellers'),
    path('seller/<int:pk>', SellerShow.as_view(), name='seller'),
    path('seller/add', SellerAdd.as_view(), name='seller_add'),
    path('seller/<int:pk>/update', SellerUpdate.as_view(), name='seller_update'),
    path('seller/<int:pk>/delete', SellerDelete.as_view(), name='seller_delete'),

    path('tours/', ToursList.as_view(), name='tours'),
    path('tour/<int:pk>', TourShow.as_view(), name='tour'),
    path('tour/add', TourAdd.as_view(), name='tour_add'),
    path('tour/<int:pk>/update', TourUpdate.as_view(), name='tour_update'),
    path('tour/<int:pk>/delete', TourDelete.as_view(), name='tour_delete'),

    path('movements/', MovementsList.as_view(), name='movements'),
    path('movement/<int:pk>', MovementShow.as_view(), name='movement'),
    path('movement/add', MovementAdd.as_view(), name='movement_add'),
    path('movement/<int:pk>/update', MovementUpdate.as_view(), name='movement_update'),
    path('movement/<int:pk>/delete', MovementDelete.as_view(), name='movement_delete'),

    path('contracts/', ContractsList.as_view(), name='contracts'),
    path('contract/<int:pk>', ContractShow.as_view(), name='contract'),
    path('contract/add', ContractAdd.as_view(), name='contract_add'),
    path('contract/<int:pk>/update', ContractUpdate.as_view(), name='contract_update'),
    path('contract/<int:pk>/delete', ContractDelete.as_view(), name='contract_delete'),

    path('my_tours/', ClientToursList.as_view(), name='my_tours'),
    path('my_tour/<int:pk>', ClientTourShow.as_view(), name='my_tour'),

    path('my_movements/', ClientMovementsList.as_view(), name='my_movements'),
    path('my_movement/<int:pk>', ClientMovementShow.as_view(), name='my_movement'),

    path('managers/', ManagersList.as_view(), name='managers'),
    path('manager/<int:pk>', ManagerShow.as_view(), name='manager'),
    path('manager/add', ManagerAdd.as_view(), name='manager_add'),
    path('manager/<int:pk>/update', ManagerUpdate.as_view(), name='manager_update'),
    path('manager/<int:pk>/delete', ManagerDelete.as_view(), name='manager_delete'),

    path('export-<str:etype>-xlsx', get_entities_xlsx, name='entities_xlsx'),
    path('export-<str:etype>-json', get_entities_json, name='entities_json'),
]

handler404 = error_404_view
handler500 = error_500_view
