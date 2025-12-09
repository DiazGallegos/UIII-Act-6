from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Equipo, Jugador, Partido, Entrenador, Estadio, Arbitro
from datetime import datetime

# ======================
# VISTA INICIO
# ======================

def inicio_futbol(request):
    total_equipos = Equipo.objects.count()
    total_jugadores = Jugador.objects.count()
    total_partidos = Partido.objects.count()
    total_entrenadores = Entrenador.objects.count()
    total_estadios = Estadio.objects.count()
    total_arbitros = Arbitro.objects.count()
    
    context = {
        'total_equipos': total_equipos,
        'total_jugadores': total_jugadores,
        'total_partidos': total_partidos,
        'total_entrenadores': total_entrenadores,
        'total_estadios': total_estadios,
        'total_arbitros': total_arbitros,
    }
    return render(request, 'inicio.html', context)

# ======================
# EQUIPOS
# ======================

def agregar_equipo(request):
    if request.method == 'POST':
        print("📝 [EQUIPO] Datos recibidos:", dict(request.POST))
        print("📸 [EQUIPO] Archivos recibidos:", dict(request.FILES))
        
        try:
            equipo = Equipo(
                nombre=request.POST['nombre'],
                ciudad=request.POST['ciudad'],
                pais=request.POST['pais'],
                fundacion=request.POST['fundacion'],
                colores=request.POST['colores'],
                presidente=request.POST.get('presidente', '')
            )
            
            # ¡IMPORTANTE! Primero guardar para tener ID
            equipo.save()
            print("✅ [EQUIPO] Equipo guardado con ID:", equipo.id)
            
            # Luego asignar imagen si existe
            if 'imagen' in request.FILES:
                equipo.imagen = request.FILES['imagen']
                equipo.save()  # Guardar de nuevo con la imagen
                print("✅ [EQUIPO] Imagen guardada:", equipo.imagen.name)
                print("✅ [EQUIPO] URL de imagen:", equipo.imagen.url if equipo.imagen else "No hay")
            
            messages.success(request, f'✅ Equipo {equipo.nombre} creado exitosamente!')
            messages.info(request, f'📷 Imagen: {"Sí" if equipo.imagen else "No"}')
            return redirect('ver_equipos')
            
        except Exception as e:
            print("❌ [EQUIPO] Error:", str(e))
            messages.error(request, f'❌ Error al crear equipo: {str(e)}')
    
    return render(request, 'equipo/agregar_equipo.html')

def ver_equipos(request):
    equipos = Equipo.objects.all()
    
    # Debug: mostrar info de cada equipo
    for equipo in equipos:
        print(f"🔍 [VER EQUIPOS] {equipo.nombre}: Imagen={equipo.imagen}, URL={equipo.imagen.url if equipo.imagen else 'No tiene'}")
        if equipo.imagen:
            messages.info(request, f'📷 {equipo.nombre}: {equipo.imagen.url}')
    
    return render(request, 'equipo/ver_equipos.html', {'equipos': equipos})

def actualizar_equipo(request, id):
    equipo = get_object_or_404(Equipo, id=id)
    return render(request, 'equipo/actualizar_equipo.html', {'equipo': equipo})

def realizar_actualizacion_equipo(request, id):
    equipo = get_object_or_404(Equipo, id=id)
    
    if request.method == 'POST':
        print("📝 [ACTUALIZAR EQUIPO] Datos:", dict(request.POST))
        print("📸 [ACTUALIZAR EQUIPO] Archivos:", dict(request.FILES))
        
        equipo.nombre = request.POST.get('nombre')
        equipo.ciudad = request.POST.get('ciudad')
        equipo.pais = request.POST.get('pais')
        equipo.fundacion = request.POST.get('fundacion')
        equipo.colores = request.POST.get('colores')
        equipo.presidente = request.POST.get('presidente')
        
        if 'imagen' in request.FILES:
            print("✅ [ACTUALIZAR EQUIPO] Nueva imagen:", request.FILES['imagen'].name)
            equipo.imagen = request.FILES['imagen']
        
        equipo.save()
        messages.success(request, f'✅ Equipo {equipo.nombre} actualizado.')
        return redirect('ver_equipos')
    
    return redirect('actualizar_equipo', id=id)

def borrar_equipo(request, id):
    equipo = get_object_or_404(Equipo, id=id)
    return render(request, 'equipo/borrar_equipo.html', {'equipo': equipo})

def realizar_borrado_equipo(request, id):
    equipo = get_object_or_404(Equipo, id=id)
    nombre = equipo.nombre
    equipo.delete()
    messages.success(request, f'✅ Equipo {nombre} eliminado.')
    return redirect('ver_equipos')

# ======================
# JUGADORES
# ======================

def agregar_jugador(request):
    if request.method == 'POST':
        print("📝 [JUGADOR] Datos recibidos:", dict(request.POST))
        print("📸 [JUGADOR] Archivos recibidos:", dict(request.FILES))
        
        try:
            equipo = get_object_or_404(Equipo, id=request.POST.get('equipo'))
            
            jugador = Jugador(
                nombre=request.POST.get('nombre'),
                apellido=request.POST.get('apellido'),
                fecha_nacimiento=request.POST.get('fecha_nacimiento'),
                nacionalidad=request.POST.get('nacionalidad'),
                posicion=request.POST.get('posicion'),
                numero_camiseta=request.POST.get('numero_camiseta'),
                equipo=equipo
            )
            
            # Guardar primero para tener ID
            jugador.save()
            print("✅ [JUGADOR] Jugador guardado con ID:", jugador.id)
            
            if 'foto' in request.FILES:
                jugador.foto = request.FILES['foto']
                jugador.save()  # Guardar de nuevo con foto
                print("✅ [JUGADOR] Foto guardada:", jugador.foto.name)
                print("✅ [JUGADOR] URL foto:", jugador.foto.url if jugador.foto else "No hay")
            
            messages.success(request, f'✅ Jugador {jugador.nombre} creado.')
            return redirect('ver_jugadores')
            
        except Exception as e:
            print("❌ [JUGADOR] Error:", str(e))
            messages.error(request, f'❌ Error: {str(e)}')
    
    equipos = Equipo.objects.all()
    return render(request, 'jugador/agregar_jugador.html', {'equipos': equipos})

def ver_jugadores(request):
    jugadores = Jugador.objects.all()
    return render(request, 'jugador/ver_jugadores.html', {'jugadores': jugadores})

def actualizar_jugador(request, id):
    jugador = get_object_or_404(Jugador, id=id)
    equipos = Equipo.objects.all()
    return render(request, 'jugador/actualizar_jugador.html', {'jugador': jugador, 'equipos': equipos})

def realizar_actualizacion_jugador(request, id):
    jugador = get_object_or_404(Jugador, id=id)
    
    if request.method == 'POST':
        jugador.nombre = request.POST.get('nombre')
        jugador.apellido = request.POST.get('apellido')
        jugador.fecha_nacimiento = request.POST.get('fecha_nacimiento')
        jugador.nacionalidad = request.POST.get('nacionalidad')
        jugador.posicion = request.POST.get('posicion')
        jugador.numero_camiseta = request.POST.get('numero_camiseta')
        
        equipo_id = request.POST.get('equipo')
        if equipo_id:
            jugador.equipo = get_object_or_404(Equipo, id=equipo_id)
        
        if 'foto' in request.FILES:
            jugador.foto = request.FILES['foto']
        
        jugador.save()
        messages.success(request, f'✅ Jugador {jugador.nombre} actualizado.')
        return redirect('ver_jugadores')
    
    return redirect('actualizar_jugador', id=id)

def borrar_jugador(request, id):
    jugador = get_object_or_404(Jugador, id=id)
    return render(request, 'jugador/borrar_jugador.html', {'jugador': jugador})

def realizar_borrado_jugador(request, id):
    jugador = get_object_or_404(Jugador, id=id)
    nombre = f"{jugador.nombre} {jugador.apellido}"
    jugador.delete()
    messages.success(request, f'✅ Jugador {nombre} eliminado.')
    return redirect('ver_jugadores')

# ======================
# ESTADIOS
# ======================

def agregar_estadio(request):
    if request.method == 'POST':
        print("📝 [ESTADIO] Datos recibidos:", dict(request.POST))
        print("📸 [ESTADIO] Archivos recibidos:", dict(request.FILES))
        
        try:
            estadio = Estadio(
                nombre=request.POST.get('nombre'),
                ciudad=request.POST.get('ciudad'),
                capacidad=request.POST.get('capacidad'),
                año_inauguracion=request.POST.get('año_inauguracion'),
                direccion=request.POST.get('direccion')
            )
            
            # Guardar primero
            estadio.save()
            print("✅ [ESTADIO] Estadio guardado con ID:", estadio.id)
            
            equipo_id = request.POST.get('equipo_local')
            if equipo_id:
                estadio.equipo_local = get_object_or_404(Equipo, id=equipo_id)
            
            if 'foto' in request.FILES:
                estadio.foto = request.FILES['foto']
                estadio.save()  # Guardar de nuevo con foto
                print("✅ [ESTADIO] Foto guardada:", estadio.foto.name)
                print("✅ [ESTADIO] URL foto:", estadio.foto.url if estadio.foto else "No hay")
            else:
                estadio.save()
            
            messages.success(request, f'✅ Estadio {estadio.nombre} creado.')
            return redirect('ver_estadios')
            
        except Exception as e:
            print("❌ [ESTADIO] Error:", str(e))
            messages.error(request, f'❌ Error: {str(e)}')
    
    equipos = Equipo.objects.all()
    return render(request, 'estadio/agregar_estadio.html', {'equipos': equipos})

def ver_estadios(request):
    estadios = Estadio.objects.all()
    return render(request, 'estadio/ver_estadios.html', {'estadios': estadios})

def actualizar_estadio(request, id):
    estadio = get_object_or_404(Estadio, id=id)
    equipos = Equipo.objects.all()
    return render(request, 'estadio/actualizar_estadio.html', {'estadio': estadio, 'equipos': equipos})

def realizar_actualizacion_estadio(request, id):
    estadio = get_object_or_404(Estadio, id=id)
    
    if request.method == 'POST':
        estadio.nombre = request.POST.get('nombre')
        estadio.ciudad = request.POST.get('ciudad')
        estadio.capacidad = request.POST.get('capacidad')
        estadio.año_inauguracion = request.POST.get('año_inauguracion')
        estadio.direccion = request.POST.get('direccion')
        
        equipo_id = request.POST.get('equipo_local')
        if equipo_id:
            estadio.equipo_local = get_object_or_404(Equipo, id=equipo_id)
        else:
            estadio.equipo_local = None
        
        if 'foto' in request.FILES:
            estadio.foto = request.FILES['foto']
        
        estadio.save()
        messages.success(request, f'✅ Estadio {estadio.nombre} actualizado.')
        return redirect('ver_estadios')
    
    return redirect('actualizar_estadio', id=id)

def borrar_estadio(request, id):
    estadio = get_object_or_404(Estadio, id=id)
    return render(request, 'estadio/borrar_estadio.html', {'estadio': estadio})

def realizar_borrado_estadio(request, id):
    estadio = get_object_or_404(Estadio, id=id)
    nombre = estadio.nombre
    estadio.delete()
    messages.success(request, f'✅ Estadio {nombre} eliminado.')
    return redirect('ver_estadios')

# ======================
# ENTRENADORES
# ======================

def agregar_entrenador(request):
    if request.method == 'POST':
        print("📝 [ENTRENADOR] Datos recibidos:", dict(request.POST))
        print("📸 [ENTRENADOR] Archivos recibidos:", dict(request.FILES))
        
        try:
            entrenador = Entrenador(
                nombre=request.POST.get('nombre'),
                apellido=request.POST.get('apellido'),
                fecha_nacimiento=request.POST.get('fecha_nacimiento'),
                nacionalidad=request.POST.get('nacionalidad'),
                licencia=request.POST.get('licencia'),
                fecha_inicio_contrato=request.POST.get('fecha_inicio_contrato'),
                fecha_fin_contrato=request.POST.get('fecha_fin_contrato')
            )
            
            # Guardar primero
            entrenador.save()
            print("✅ [ENTRENADOR] Entrenador guardado con ID:", entrenador.id)
            
            equipo_id = request.POST.get('equipo')
            if equipo_id:
                entrenador.equipo = get_object_or_404(Equipo, id=equipo_id)
            
            if 'foto' in request.FILES:
                entrenador.foto = request.FILES['foto']
                entrenador.save()  # Guardar de nuevo con foto
                print("✅ [ENTRENADOR] Foto guardada:", entrenador.foto.name)
            else:
                entrenador.save()
            
            messages.success(request, f'✅ Entrenador {entrenador.nombre} creado.')
            return redirect('ver_entrenadores')
            
        except Exception as e:
            print("❌ [ENTRENADOR] Error:", str(e))
            messages.error(request, f'❌ Error: {str(e)}')
    
    equipos = Equipo.objects.all()
    return render(request, 'entrenador/agregar_entrenador.html', {'equipos': equipos})

def ver_entrenadores(request):
    entrenadores = Entrenador.objects.all()
    return render(request, 'entrenador/ver_entrenadores.html', {'entrenadores': entrenadores})

def actualizar_entrenador(request, id):
    entrenador = get_object_or_404(Entrenador, id=id)
    equipos = Equipo.objects.all()
    return render(request, 'entrenador/actualizar_entrenador.html', {'entrenador': entrenador, 'equipos': equipos})

def realizar_actualizacion_entrenador(request, id):
    entrenador = get_object_or_404(Entrenador, id=id)
    
    if request.method == 'POST':
        entrenador.nombre = request.POST.get('nombre')
        entrenador.apellido = request.POST.get('apellido')
        entrenador.fecha_nacimiento = request.POST.get('fecha_nacimiento')
        entrenador.nacionalidad = request.POST.get('nacionalidad')
        entrenador.licencia = request.POST.get('licencia')
        entrenador.fecha_inicio_contrato = request.POST.get('fecha_inicio_contrato')
        entrenador.fecha_fin_contrato = request.POST.get('fecha_fin_contrato')
        
        equipo_id = request.POST.get('equipo')
        if equipo_id:
            entrenador.equipo = get_object_or_404(Equipo, id=equipo_id)
        else:
            entrenador.equipo = None
        
        if 'foto' in request.FILES:
            entrenador.foto = request.FILES['foto']
        
        entrenador.save()
        messages.success(request, f'✅ Entrenador {entrenador.nombre} actualizado.')
        return redirect('ver_entrenadores')
    
    return redirect('actualizar_entrenador', id=id)

def borrar_entrenador(request, id):
    entrenador = get_object_or_404(Entrenador, id=id)
    return render(request, 'entrenador/borrar_entrenador.html', {'entrenador': entrenador})

def realizar_borrado_entrenador(request, id):
    entrenador = get_object_or_404(Entrenador, id=id)
    nombre = f"{entrenador.nombre} {entrenador.apellido}"
    entrenador.delete()
    messages.success(request, f'✅ Entrenador {nombre} eliminado.')
    return redirect('ver_entrenadores')

# ======================
# ÁRBITROS
# ======================

def agregar_arbitro(request):
    if request.method == 'POST':
        print("📝 [ÁRBITRO] Datos recibidos:", dict(request.POST))
        print("📸 [ÁRBITRO] Archivos recibidos:", dict(request.FILES))
        
        try:
            arbitro = Arbitro(
                nombre=request.POST.get('nombre'),
                apellido=request.POST.get('apellido'),
                fecha_nacimiento=request.POST.get('fecha_nacimiento'),
                nacionalidad=request.POST.get('nacionalidad'),
                tipo=request.POST.get('tipo'),
                experiencia_años=request.POST.get('experiencia_años', 0),
                federacion=request.POST.get('federacion')
            )
            
            # Guardar primero
            arbitro.save()
            print("✅ [ÁRBITRO] Árbitro guardado con ID:", arbitro.id)
            
            if 'foto' in request.FILES:
                arbitro.foto = request.FILES['foto']
                arbitro.save()  # Guardar de nuevo con foto
                print("✅ [ÁRBITRO] Foto guardada:", arbitro.foto.name)
            else:
                arbitro.save()
            
            messages.success(request, f'✅ Árbitro {arbitro.nombre} creado.')
            return redirect('ver_arbitros')
            
        except Exception as e:
            print("❌ [ÁRBITRO] Error:", str(e))
            messages.error(request, f'❌ Error: {str(e)}')
    
    return render(request, 'arbitro/agregar_arbitro.html')

def ver_arbitros(request):
    arbitros = Arbitro.objects.all()
    return render(request, 'arbitro/ver_arbitros.html', {'arbitros': arbitros})

def actualizar_arbitro(request, id):
    arbitro = get_object_or_404(Arbitro, id=id)
    return render(request, 'arbitro/actualizar_arbitro.html', {'arbitro': arbitro})

def realizar_actualizacion_arbitro(request, id):
    arbitro = get_object_or_404(Arbitro, id=id)
    
    if request.method == 'POST':
        arbitro.nombre = request.POST.get('nombre')
        arbitro.apellido = request.POST.get('apellido')
        arbitro.fecha_nacimiento = request.POST.get('fecha_nacimiento')
        arbitro.nacionalidad = request.POST.get('nacionalidad')
        arbitro.tipo = request.POST.get('tipo')
        arbitro.experiencia_años = request.POST.get('experiencia_años', 0)
        arbitro.federacion = request.POST.get('federacion')
        
        if 'foto' in request.FILES:
            arbitro.foto = request.FILES['foto']
        
        arbitro.save()
        messages.success(request, f'✅ Árbitro {arbitro.nombre} actualizado.')
        return redirect('ver_arbitros')
    
    return redirect('actualizar_arbitro', id=id)

def borrar_arbitro(request, id):
    arbitro = get_object_or_404(Arbitro, id=id)
    return render(request, 'arbitro/borrar_arbitro.html', {'arbitro': arbitro})

def realizar_borrado_arbitro(request, id):
    arbitro = get_object_or_404(Arbitro, id=id)
    nombre = f"{arbitro.nombre} {arbitro.apellido}"
    arbitro.delete()
    messages.success(request, f'✅ Árbitro {nombre} eliminado.')
    return redirect('ver_arbitros')

# ======================
# PARTIDOS - ¡CORREGIDO!
# ======================

def agregar_partido(request):
    if request.method == 'POST':
        print("📝 [PARTIDO] Datos recibidos:", dict(request.POST))
        print("📸 [PARTIDO] Archivos recibidos:", dict(request.FILES))
        
        try:
            # Obtener los objetos relacionados primero
            equipo_local = get_object_or_404(Equipo, id=request.POST.get('equipo_local'))
            equipo_visitante = get_object_or_404(Equipo, id=request.POST.get('equipo_visitante'))
            
            # Obtener estadio si se seleccionó
            estadio_id = request.POST.get('estadio')
            estadio = None
            if estadio_id and estadio_id != '':
                estadio = get_object_or_404(Estadio, id=estadio_id)
            
            # Convertir la fecha de string a objeto datetime
            fecha_str = request.POST.get('fecha')
            fecha = datetime.strptime(fecha_str, '%Y-%m-%dT%H:%M')
            
            # Crear el partido CON todas las relaciones
            partido = Partido(
                fecha=fecha,
                equipo_local=equipo_local,
                equipo_visitante=equipo_visitante,
                goles_local=int(request.POST.get('goles_local', 0)),
                goles_visitante=int(request.POST.get('goles_visitante', 0)),
                estado=request.POST.get('estado', 'PEN'),
                asistencia=int(request.POST.get('asistencia', 0))
            )
            
            # Asignar estadio si existe
            if estadio:
                partido.estadio = estadio
            
            # Guardar el partido
            partido.save()
            print(f"✅ [PARTIDO] Partido guardado con ID: {partido.id}")
            print(f"✅ [PARTIDO] {equipo_local.nombre} vs {equipo_visitante.nombre}")
            
            # Guardar foto si existe
            if 'foto' in request.FILES:
                partido.foto = request.FILES['foto']
                partido.save()  # Guardar de nuevo con foto
                print(f"✅ [PARTIDO] Foto guardada: {partido.foto.name}")
            
            messages.success(request, f'✅ Partido creado: {equipo_local.nombre} vs {equipo_visitante.nombre}')
            return redirect('ver_partidos')
            
        except Exception as e:
            print(f"❌ [PARTIDO] Error: {str(e)}")
            messages.error(request, f'❌ Error al crear partido: {str(e)}')
    
    # GET request - mostrar formulario
    equipos = Equipo.objects.all()
    estadios = Estadio.objects.all()
    return render(request, 'partido/agregar_partido.html', {
        'equipos': equipos,
        'estadios': estadios
    })

def ver_partidos(request):
    partidos = Partido.objects.all().order_by('-fecha')
    return render(request, 'partido/ver_partidos.html', {'partidos': partidos})

def actualizar_partido(request, id):
    partido = get_object_or_404(Partido, id=id)
    equipos = Equipo.objects.all()
    estadios = Estadio.objects.all()
    
    return render(request, 'partido/actualizar_partido.html', {
        'partido': partido,
        'equipos': equipos,
        'estadios': estadios
    })

def realizar_actualizacion_partido(request, id):
    partido = get_object_or_404(Partido, id=id)
    
    if request.method == 'POST':
        try:
            # Convertir fecha
            fecha_str = request.POST.get('fecha')
            partido.fecha = datetime.strptime(fecha_str, '%Y-%m-%dT%H:%M')
            
            # Actualizar relaciones
            estadio_id = request.POST.get('estadio')
            if estadio_id and estadio_id != '':
                partido.estadio = get_object_or_404(Estadio, id=estadio_id)
            else:
                partido.estadio = None
            
            partido.equipo_local = get_object_or_404(Equipo, id=request.POST.get('equipo_local'))
            partido.equipo_visitante = get_object_or_404(Equipo, id=request.POST.get('equipo_visitante'))
            partido.goles_local = int(request.POST.get('goles_local', 0))
            partido.goles_visitante = int(request.POST.get('goles_visitante', 0))
            partido.estado = request.POST.get('estado', 'PEN')
            partido.asistencia = int(request.POST.get('asistencia', 0))
            
            if 'foto' in request.FILES:
                partido.foto = request.FILES['foto']
            
            partido.save()
            messages.success(request, f'✅ Partido actualizado: {partido.equipo_local} vs {partido.equipo_visitante}')
            return redirect('ver_partidos')
            
        except Exception as e:
            messages.error(request, f'❌ Error al actualizar: {str(e)}')
            return redirect('actualizar_partido', id=id)
    
    return redirect('actualizar_partido', id=id)

def borrar_partido(request, id):
    partido = get_object_or_404(Partido, id=id)
    return render(request, 'partido/borrar_partido.html', {'partido': partido})

def realizar_borrado_partido(request, id):
    partido = get_object_or_404(Partido, id=id)
    nombre_partido = f"{partido.equipo_local} vs {partido.equipo_visitante}"
    partido.delete()
    messages.success(request, f'✅ Partido eliminado: {nombre_partido}')
    return redirect('ver_partidos')