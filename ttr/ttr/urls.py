# -*- coding: utf-8 -*-
from django.urls import re_path as url
from ttr_app import views as views, views_buscar as views_buscar, views_instrumento as views_instrumento, views_buscar_instr as views_buscar_instr, views_inst_rubrica as views_inst_rubrica
from ttr_app import views_inst_cotejo as views_inst_cotejo, views_inst_observacion as views_inst_observacion, views_comments as views_comments, views_enviar_email as views_enviar_email
#from django.conf.urls import include, url
from django.views.generic.base import RedirectView

from django.contrib import admin
from django.contrib.auth import views as auth_views
admin.autodiscover()

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^$', RedirectView.as_view(url='/index', permanent=True)),
    url(r'^index/?$', views.index),
    url(r'^indexInter/?$', views.indexInter),
    url(r'^login/?$', views.login),
    url(r'^logout/?$', views.logout),

    url(r'^buscar/?$', views_buscar.buscar),

    url(r'^portal/?$' ,views.portal),

    url(r'^superior/?$', views.superior),
    url(r'^medioSuperior/?$', views.mediosuperior),

    url(r'^estadisticas/?$', views.estadisticas),

    url(r'^estructura/?$', views.estructura),
    url(r'^estructura/json/(?P<node>\w+)(/(?P<node_id>\d{1,5}))?$', views.estructura_json),
    url(r'^estructura/json/$', views.estructura_json),

    url(r'^asignatura/nuevo/?$',views.newAsignature),
    url(r'^asignatura/agregar/?$',views.registrarAsignatura),
    url(r'^asignatura/ver/?$',views.verAsignaturas),
    url(r'^asignatura/borrar/?$',views.eliminarAsignatura),
    url(r'^asignatura/consultar/?$',views.consultarAsignatura),
    url(r'^asignatura/consultar/modificar/?$',views.editarAsignatura),
    url(r'^asignatura/agregardocente/?$',views.agregarDocente),
    url(r'^asignatura/quitardocente/?$',views.quitarDocente),

    url(r'^departamento/nuevo/?$',views.newDepartamento),
    url(r'^departamento/agregar/?$',views.registrarDepartamento),
    url(r'^departamento/ver/?$',views.verDepartamentos),
    url(r'^departamento/borrar/?$',views.eliminarDepartamento),
    url(r'^departamento/consultar/?$',views.consultarDepartamento),
    url(r'^departamento/consultar/modificar/?$',views.editarDepartamento),

    url(r'^academia/nuevo/?$',views.newAcademia),
    url(r'^academia/agregar/?$',views.registrarAcademia),
    url(r'^academia/ver/?$',views.verAcademias),
    url(r'^academia/borrar/?$',views.eliminarAcademia),
    url(r'^academia/consultar/?$',views.consultarAcademia),
    url(r'^academia/consultar/modificar/?$',views.editarAcademia),

    # url(r'^instrumentos/', ''),
    url(r'^instrumento/?$', views_instrumento.instrumento),
    # url(r'^instrumento/agregar', ''),
    url(r'^instrumentos/buscar/?$', views_buscar_instr.buscar),
    url(r'^instrumentos/buscar/mostrar/?$', views_buscar_instr.buscar_insts),
    # url(r'^pdf/', 'ttr_app.views_buscar_instr.some_view'),

    url(r'^instrumento/rating/?$', views_instrumento.rating),
    url(r'^instrumento/eliminar/?$', views_instrumento.eliminar),

    url(r'^instrumento/rubrica/agregar/?$', views_inst_rubrica.agregar),
    url(r'^instrumento/rubrica/editar/?$', views_inst_rubrica.editar),
    url(r'^instrumento/rubrica/ver/?$', views_inst_rubrica.ver),

    url(r'^instrumento/listacotejo/agregar/?$', views_inst_cotejo.agregar),
    url(r'^instrumento/listacotejo/editar/?$', views_inst_cotejo.editar),
    url(r'^instrumento/listacotejo/ver/?$', views_inst_cotejo.ver),

    url(r'^instrumento/listaobs/agregar/?$', views_inst_observacion.agregar),
    url(r'^instrumento/listaobs/editar/?$', views_inst_observacion.editar),
    url(r'^instrumento/listaobs/ver/?$', views_inst_observacion.ver),

    url(r'^instrumento/comentario/?$', views_comments.comment),
    url(r'^instrumento/comentarios/?$', views_comments.get_comments),


    # url(r'^instrumento/borrar', ''),


    url(r'^usuario/nuevo/?$', views.newUser),
    url(r'^usuario/agregar/?$', views.registrarUsuario),
    url(r'^usuario/borrar/?$', views.eliminarUsuario),
    url(r'^usuario/consultar/?$',views.consultarUsuario),
    url(r'^usuario/consultar/modificar/?$',views.editarUsuario),

    url(r'^usuario/recuperarcontrasena/?$', views_enviar_email.enviar_correo),

    url(r'^usuario/perfil/?$',views.miperfil),
    url(r'^usuario/perfil/cambiarPrivacidad/?$',views.cambiarPrivacidad),


    # Reseteo de password TODO verificar si van a funcionar
    # url(r'^forgot_password/$',auth_views.password_reset,name='forgot_password1'),
    # url(r'^forgot_password/done/$',auth_views.password_reset_done,name='forgot_password2'),
    # url(r'^forgot_password/confirm/(?P<uidb64>[-\w]+)/(?P<token>[-\w]+)/$',auth_views.password_reset_confirm,name='forgot_password3'),
    # url(r'^forgot_password/complete/$',auth_views.password_reset_complete,name='forgot_password4'),

]
