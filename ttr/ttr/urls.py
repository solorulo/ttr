# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.views.generic.base import RedirectView

from django.contrib import admin
from django.contrib.auth import views as auth_views
admin.autodiscover()

urlpatterns = patterns('',

    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', RedirectView.as_view(url='/index', permanent=True)),
    url(r'^index/?$', 'ttr_app.views.index'),
    url(r'^indexInter/?$', 'ttr_app.views.indexInter'),
    url(r'^login/?$', 'ttr_app.views.login'),
    url(r'^logout/?$', 'ttr_app.views.logout'),

    url(r'^buscar/?$', 'ttr_app.views_buscar.buscar'),

    url(r'^portal/?$' ,'ttr_app.views.portal'),

    url(r'^superior/?$', 'ttr_app.views.superior'),
    url(r'^medioSuperior/?$', 'ttr_app.views.mediosuperior'),

    url(r'^estructura/?$', 'ttr_app.views.estructura'),
    url(r'^estructura/json/(?P<node>\w+)(/(?P<node_id>\d{1,5}))?$', 'ttr_app.views.estructura_json'),
    url(r'^estructura/json/$', 'ttr_app.views.estructura_json'),

    url(r'^asignatura/nuevo/?$','ttr_app.views.newAsignature'),
    url(r'^asignatura/agregar/?$','ttr_app.views.registrarAsignatura'),                       
    url(r'^asignatura/ver/?$','ttr_app.views.verAsignaturas'),
    url(r'^asignatura/borrar/?$','ttr_app.views.eliminarAsignatura'),
    url(r'^asignatura/consultar/?$','ttr_app.views.consultarAsignatura'),
    url(r'^asignatura/consultar/modificar/?$','ttr_app.views.editarAsignatura'),
    url(r'^asignatura/agregardocente/?$','ttr_app.views.agregarDocente'),
    url(r'^asignatura/quitardocente/?$','ttr_app.views.quitarDocente'),

    url(r'^departamento/nuevo/?$','ttr_app.views.newDepartamento'),
    url(r'^departamento/agregar/?$','ttr_app.views.registrarDepartamento'),
    url(r'^departamento/ver/?$','ttr_app.views.verDepartamentos'),
    url(r'^departamento/borrar/?$','ttr_app.views.eliminarDepartamento'),
    url(r'^departamento/consultar/?$','ttr_app.views.consultarDepartamento'),
    url(r'^departamento/consultar/modificar/?$','ttr_app.views.editarDepartamento'),

    url(r'^academia/nuevo/?$','ttr_app.views.newAcademia'),
    url(r'^academia/agregar/?$','ttr_app.views.registrarAcademia'),
    url(r'^academia/ver/?$','ttr_app.views.verAcademias'),
    url(r'^academia/borrar/?$','ttr_app.views.eliminarAcademia'),
    url(r'^academia/consultar/?$','ttr_app.views.consultarAcademia'),
    url(r'^academia/consultar/modificar/?$','ttr_app.views.editarAcademia'),

    # url(r'^instrumentos/', ''),
    url(r'^instrumento/$', 'ttr_app.views_instrumento.instrumento'),
    # url(r'^instrumento/agregar', ''),
    url(r'^instrumentos/buscar/$', 'ttr_app.views_buscar_instr.buscar'),
    url(r'^instrumentos/buscar/mostrar$', 'ttr_app.views_buscar_instr.buscar_insts'),
    # url(r'^pdf/', 'ttr_app.views_buscar_instr.some_view'),

    url(r'^instrumento/rubrica/agregar/?$', 'ttr_app.views_inst_rubrica.agregar'),
    url(r'^instrumento/rubrica/editar/?$', 'ttr_app.views_inst_rubrica.editar'),
    url(r'^instrumento/rubrica/ver/?$', 'ttr_app.views_inst_rubrica.ver'),

    url(r'^instrumento/listacotejo/agregar/?$', 'ttr_app.views_inst_cotejo.agregar'),
    url(r'^instrumento/listacotejo/editar/?$', 'ttr_app.views_inst_cotejo.editar'),
    url(r'^instrumento/listacotejo/ver/?$', 'ttr_app.views_inst_cotejo.ver'),

    url(r'^instrumento/listaobs/agregar/?$', 'ttr_app.views_inst_observacion.agregar'),
    url(r'^instrumento/listaobs/editar/?$', 'ttr_app.views_inst_observacion.editar'),
    url(r'^instrumento/listaobs/ver/?$', 'ttr_app.views_inst_observacion.ver'),

    url(r'^instrumento/comentario/?$', 'ttr_app.views_comments.comment'),
    url(r'^instrumento/comentarios/?$', 'ttr_app.views_comments.get_comments'),


    # url(r'^instrumento/borrar', ''),


    url(r'^usuario/nuevo/?$', 'ttr_app.views.newUser'),
    url(r'^usuario/agregar/?$', 'ttr_app.views.registrarUsuario'),
    url(r'^usuario/borrar/?$', 'ttr_app.views.eliminarUsuario'),
    url(r'^usuario/consultar/?$','ttr_app.views.consultarUsuario'),
    url(r'^usuario/consultar/modificar/?$','ttr_app.views.editarUsuario'),

    url(r'^usuario/recuperarcontrasena/?$','ttr_app.views_enviar_email.enviar_correo'),

    url(r'^usuario/perfil/?$','ttr_app.views.miperfil'),
    url(r'^usuario/perfil/cambiarPrivacidad/?$','ttr_app.views.cambiarPrivacidad'),


    # Reseteo de password TODO verificar si van a funcionar
    # url(r'^forgot_password/$',auth_views.password_reset,name='forgot_password1'),
    # url(r'^forgot_password/done/$',auth_views.password_reset_done,name='forgot_password2'),
    # url(r'^forgot_password/confirm/(?P<uidb64>[-\w]+)/(?P<token>[-\w]+)/$',auth_views.password_reset_confirm,name='forgot_password3'),
    # url(r'^forgot_password/complete/$',auth_views.password_reset_complete,name='forgot_password4'),

)
