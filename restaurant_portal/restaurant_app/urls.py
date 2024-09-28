from django.urls import path, include
from restaurant_app import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'routerGetEmployees', views.getEmployeesViewSet, basename='router-get-employees')
router.register(r'routerModelViewSetUpdateEmployees', views.updateEmployeesModelViewSet, basename='router-modelviewset-update-employees')
router.register(r'routerModelViewSetCombinedEmployees', views.combinedModelViewSet, basename='router-modelviewset-combined-employees')


employeeDetailsList = views.getEmployeesViewSet.as_view(
    {
        'get': 'list',
        'post': 'create',
    }
)

updateEmployeeDetailsList = views.getEmployeesViewSet.as_view(
    {
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy'
    }
)

urlpatterns = [
    path('getEmployees/', views.get_employees, name='get-employees'),
    path('updateEmployees/<int:pk>/', views.update_employees, name='update-employees'),
    path('apiViewGetEmployees/', views.getEmployeesAPIViewSet.as_view(), name='apiview-get-employees'),
    path('apiViewUpdateEmployees/<int:pk>/', views.updateEmployeesAPIViewSet.as_view(), name='apiview-update-employees'),
    path('viewSetEmployeeDetails/', employeeDetailsList, name='viewset-employee-details'),
    path('viewSetEmployeeDetails/<int:pk>/', updateEmployeeDetailsList, name='viewset-update-employee-details'),
    path('', include(router.urls)),
]
