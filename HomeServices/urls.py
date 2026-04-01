"""
URL configuration for HomeServices project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""


from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from marketplace.views import *



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', homefn, name='home'),
    path('services/', servicefn, name='services'),
    path('about/', aboutfn, name='about'),
    path('contact/', contactfn, name='contact'),
    path('quote/', quotefn, name='quote'),
    path('serviceview/<int:pid>/', viewservicefn, name='serviceview'),
    path('categoryview/<int:cid>/', categoryviewfn, name='categoryview'),
    path('login/', login_fn, name='login'),
    path('signup/', register_fn, name='signup'),
    path('logout/', logout_fn, name='logout'),
    
    path('addservices/', addservices_fn, name='addservices'),
    path('editservice/<int:pid>/', editservices_fn, name='editservice'),
    path('deleteservice/<int:pid>/', delete_servicefn, name='deleteservice'),
    path('profile/', profilefn, name='profile'),
    path('addprofile/', addprofilefn, name='addprofile'),
    path('add_to_cart/<int:pid>/', add_to_cartfn, name='add_to_cart'),
    path('view_cart/', view_cartfn, name='view_cart'),
    path("delete_cart_item/<int:cid>/",delete_cart_itemfn, name="delete_cart_item"),
    path('cart/update/<int:cid>/', update_cart_qty, name='update_cart_qty'),
    path('ourservapi/', ourservapifn, name='ourservapi'),
    path('addservapi/', addservapifn, name='addservapi'),
    path("viewservapi/<int:pid>/", viewservapifn, name="viewservapi"),
    path('editservapi/<int:pid>/',editservapifn, name='editservapi'),
    path("deleteservapi/<int:pid>/", deleteservapifn, name="deleteservapi"),
    path('buy_now/<int:cid>/', buy_nowfn, name='buy_now'),
    path('chatfn/', chatfn, name='chatfn'),
    path('search/', searchfn, name='search'),


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
