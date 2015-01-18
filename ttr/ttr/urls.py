# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ttr.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^index/', 'ttr_app.views.index'),
    url(r'^login/', 'ttr_app.views.login'),

    url(r'^estructura/$', 'ttr_app.views.estructura'),
    url(r'^estructura/json/(?P<node>\w+)(/(?P<node_id>\d{1,5}))?$', 'ttr_app.views.estructura_json'),
    url(r'^estructura/json/$', 'ttr_app.views.estructura_json'),



    url(r'^asignatura/nuevo$','ttr_app.views.newAsignature'),
    url(r'^asignatura/agregar$','ttr_app.views.registrarAsignatura'),                       
    url(r'^asignatura/ver$','ttr_app.views.verAsignaturas'),
    url(r'^asignatura/borrar$','ttr_app.views.eliminarAsignatura'),
    url(r'^asignatura/consultar/?$','ttr_app.views.consultarAsignatura'),
    url(r'^asignatura/consultar/modificar/?$','ttr_app.views.editarAsignatura'),

    url(r'^departamento/nuevo$','ttr_app.views.newDepartamento'),
    url(r'^departamento/agregar$','ttr_app.views.registrarDepartamento'),
    url(r'^departamento/ver$','ttr_app.views.verDepartamentos'),
    url(r'^departamento/borrar','ttr_app.views.eliminarDepartamento'),
    url(r'^departamento/consultar/?$','ttr_app.views.consultarDepartamento'),
    url(r'^departamento/consultar/modificar/?$','ttr_app.views.editarDepartamento'),


    url(r'^academia/nuevo$','ttr_app.views.newAcademia'),
    url(r'^academia/agregar$','ttr_app.views.registrarAcademia'),
    url(r'^academia/ver$','ttr_app.views.verAcademias'),
    url(r'^academia/borrar$','ttr_app.views.eliminarAcademia'),
    url(r'^academia/consultar/?$','ttr_app.views.consultarAcademia'),
    url(r'^academia/consultar/modificar/?$','ttr_app.views.editarAcademia'),
   
    # url(r'^instrumentos/', ''),
    # url(r'^instrumento/', ''),
    # url(r'^instrumento/agregar', ''),
    url(r'^instrumento/rubrica/agregar$', 'ttr_app.views_rubrica.agregar'),
    # url(r'^instrumento/listacotejo/agregar', ''),
    # url(r'^instrumento/listaobservacion/agregar', ''),
    # url(r'^instrumento/borrar', ''),

    url(r'^usuario/ver$', 'ttr_app.views.visualizarUsuario'),
    url(r'^usuario/nuevo$', 'ttr_app.views.newUser'),
    url(r'^usuario/agregar$', 'ttr_app.views.registrarUsuario'),
    url(r'^usuario/borrar$', 'ttr_app.views.eliminarUsuario'),
    url(r'^usuario/consultar/?$','ttr_app.views.consultarUsuario'),
    url(r'^usuario/consultar/modificar/?$','ttr_app.views.editarUsuario')
  
)
