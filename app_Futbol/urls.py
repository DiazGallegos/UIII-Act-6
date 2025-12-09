from django.urls import path
from . import views

urlpatterns = [
    # PÁGINA PRINCIPAL
    path('', views.inicio_futbol, name='inicio_futbol'),
    
    # EQUIPOS
    path('equipos/', views.ver_equipos, name='ver_equipos'),
    path('equipos/agregar/', views.agregar_equipo, name='agregar_equipo'),
    path('equipos/actualizar/<int:id>/', views.actualizar_equipo, name='actualizar_equipo'),
    path('equipos/realizar_actualizacion/<int:id>/', views.realizar_actualizacion_equipo, name='realizar_actualizacion_equipo'),
    path('equipos/borrar/<int:id>/', views.borrar_equipo, name='borrar_equipo'),
    path('equipos/realizar_borrado/<int:id>/', views.realizar_borrado_equipo, name='realizar_borrado_equipo'),
    
    # JUGADORES
    path('jugadores/', views.ver_jugadores, name='ver_jugadores'),
    path('jugadores/agregar/', views.agregar_jugador, name='agregar_jugador'),
    path('jugadores/actualizar/<int:id>/', views.actualizar_jugador, name='actualizar_jugador'),
    path('jugadores/realizar_actualizacion/<int:id>/', views.realizar_actualizacion_jugador, name='realizar_actualizacion_jugador'),
    path('jugadores/borrar/<int:id>/', views.borrar_jugador, name='borrar_jugador'),
    path('jugadores/realizar_borrado/<int:id>/', views.realizar_borrado_jugador, name='realizar_borrado_jugador'),
    
    # PARTIDOS
    path('partidos/', views.ver_partidos, name='ver_partidos'),
    path('partidos/agregar/', views.agregar_partido, name='agregar_partido'),
    path('partidos/actualizar/<int:id>/', views.actualizar_partido, name='actualizar_partido'),
    path('partidos/realizar_actualizacion/<int:id>/', views.realizar_actualizacion_partido, name='realizar_actualizacion_partido'),
    path('partidos/borrar/<int:id>/', views.borrar_partido, name='borrar_partido'),
    path('partidos/realizar_borrado/<int:id>/', views.realizar_borrado_partido, name='realizar_borrado_partido'),
    
    # ENTRENADORES
    path('entrenadores/', views.ver_entrenadores, name='ver_entrenadores'),
    path('entrenadores/agregar/', views.agregar_entrenador, name='agregar_entrenador'),
    path('entrenadores/actualizar/<int:id>/', views.actualizar_entrenador, name='actualizar_entrenador'),
    path('entrenadores/realizar_actualizacion/<int:id>/', views.realizar_actualizacion_entrenador, name='realizar_actualizacion_entrenador'),
    path('entrenadores/borrar/<int:id>/', views.borrar_entrenador, name='borrar_entrenador'),
    path('entrenadores/realizar_borrado/<int:id>/', views.realizar_borrado_entrenador, name='realizar_borrado_entrenador'),
    
    # ESTADIOS
    path('estadios/', views.ver_estadios, name='ver_estadios'),
    path('estadios/agregar/', views.agregar_estadio, name='agregar_estadio'),
    path('estadios/actualizar/<int:id>/', views.actualizar_estadio, name='actualizar_estadio'),
    path('estadios/realizar_actualizacion/<int:id>/', views.realizar_actualizacion_estadio, name='realizar_actualizacion_estadio'),
    path('estadios/borrar/<int:id>/', views.borrar_estadio, name='borrar_estadio'),
    path('estadios/realizar_borrado/<int:id>/', views.realizar_borrado_estadio, name='realizar_borrado_estadio'),
    
    # ÁRBITROS
    path('arbitros/', views.ver_arbitros, name='ver_arbitros'),
    path('arbitros/agregar/', views.agregar_arbitro, name='agregar_arbitro'),
    path('arbitros/actualizar/<int:id>/', views.actualizar_arbitro, name='actualizar_arbitro'),
    path('arbitros/realizar_actualizacion/<int:id>/', views.realizar_actualizacion_arbitro, name='realizar_actualizacion_arbitro'),
    path('arbitros/borrar/<int:id>/', views.borrar_arbitro, name='borrar_arbitro'),
    path('arbitros/realizar_borrado/<int:id>/', views.realizar_borrado_arbitro, name='realizar_borrado_arbitro'),
]