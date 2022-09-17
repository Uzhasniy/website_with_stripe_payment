from django.contrib import admin
from django.urls import path
from app import views
from app.views import (
    CreateCheckoutSessionView,
    ShoppingCartCheckoutSession,
    # ProductLandingPageView,
    # Testmyass,
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.main, name='main'),
    path('about', views.about, name='about'),
    path('success', views.success, name='success'),
    path('cancel', views.cancel, name='cancel'),
    path('api', views.api, name='api'),
    path('shopping_cart', views.shopping_cart, name='shopping_cart'),
    path("create/", views.create),
    path('add_cart/<int:id>/', views.add_cart, name='add_cart'),
    path("edit/<int:id>/", views.edit),
    path("delete/<int:id>/", views.delete),
    path("shop_delete/<int:id>/", views.shop_delete),
    path("item/<int:id>/", views.item),
    path('items_show', views.items_show, name='items_show'),
    path('create-checkout-session', CreateCheckoutSessionView.as_view(), name='create-checkout-session'),
    path('shopping_cart_checkout-session', ShoppingCartCheckoutSession.as_view(), name='shopping_cart_checkout-session'),
]

