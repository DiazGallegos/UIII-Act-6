from django.db import models

# ======================
# MODELOS SIMPLIFICADOS
# ======================

class Equipo(models.Model):
    nombre = models.CharField(max_length=100)
    ciudad = models.CharField(max_length=100)
    pais = models.CharField(max_length=100)
    fundacion = models.DateField()
    colores = models.CharField(max_length=100)
    presidente = models.CharField(max_length=100, blank=True, null=True)
    imagen = models.ImageField(upload_to='equipos/', blank=True, null=True)  # ¡SIMPLIFICADO!
    
    def __str__(self):
        return self.nombre
    
    @property
    def imagen_url(self):
        if self.imagen and hasattr(self.imagen, 'url'):
            return self.imagen.url
        return '/static/images/default_team.png'

class Jugador(models.Model):
    POSICIONES = [
        ('POR', 'Portero'),
        ('DEF', 'Defensa'),
        ('MED', 'Mediocampista'),
        ('DEL', 'Delantero'),
    ]
    
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField()
    nacionalidad = models.CharField(max_length=100)
    posicion = models.CharField(max_length=3, choices=POSICIONES)
    numero_camiseta = models.PositiveIntegerField()
    equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE, related_name="jugadores")
    foto = models.ImageField(upload_to='jugadores/', blank=True, null=True)  # ¡SIMPLIFICADO!
    
    def __str__(self):
        return f"{self.nombre} {self.apellido}"
    
    @property
    def foto_url(self):
        if self.foto and hasattr(self.foto, 'url'):
            return self.foto.url
        return '/static/images/default_player.png'

class Estadio(models.Model):
    nombre = models.CharField(max_length=100)
    ciudad = models.CharField(max_length=100)
    capacidad = models.PositiveIntegerField()
    año_inauguracion = models.PositiveIntegerField()
    direccion = models.TextField(blank=True, null=True)
    foto = models.ImageField(upload_to='estadios/', blank=True, null=True)  # ¡SIMPLIFICADO!
    
    equipo_local = models.OneToOneField(
        Equipo,
        on_delete=models.SET_NULL,
        related_name="sede_oficial",
        blank=True,
        null=True
    )
    
    def __str__(self):
        return f"{self.nombre} ({self.ciudad})"
    
    @property
    def foto_url(self):
        if self.foto and hasattr(self.foto, 'url'):
            return self.foto.url
        return '/static/images/default_stadium.png'

class Partido(models.Model):
    ESTADOS = [
        ('PEN', 'Pendiente'),
        ('JUG', 'Jugándose'),
        ('FIN', 'Finalizado'),
        ('SUS', 'Suspendido'),
    ]
    
    fecha = models.DateTimeField()
    estadio = models.ForeignKey(Estadio, on_delete=models.SET_NULL, null=True, related_name="partidos")
    equipo_local = models.ForeignKey(Equipo, on_delete=models.CASCADE, related_name="partidos_local")
    equipo_visitante = models.ForeignKey(Equipo, on_delete=models.CASCADE, related_name="partidos_visitante")
    goles_local = models.PositiveIntegerField(default=0)
    goles_visitante = models.PositiveIntegerField(default=0)
    estado = models.CharField(max_length=3, choices=ESTADOS, default='PEN')
    asistencia = models.PositiveIntegerField(default=0, blank=True, null=True)
    foto = models.ImageField(upload_to='partidos/', blank=True, null=True)  # ¡SIMPLIFICADO!
    
    def __str__(self):
        return f"{self.equipo_local} vs {self.equipo_visitante}"
    
    @property
    def foto_url(self):
        if self.foto and hasattr(self.foto, 'url'):
            return self.foto.url
        return '/static/images/default_match.png'

class Entrenador(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField()
    nacionalidad = models.CharField(max_length=100)
    licencia = models.CharField(max_length=50, blank=True, null=True)
    fecha_inicio_contrato = models.DateField()
    fecha_fin_contrato = models.DateField(blank=True, null=True)
    foto = models.ImageField(upload_to='entrenadores/', blank=True, null=True)  # ¡SIMPLIFICADO!
    
    equipo = models.OneToOneField(
        Equipo, 
        on_delete=models.SET_NULL, 
        related_name="director_tecnico",
        blank=True, 
        null=True
    )
    
    def __str__(self):
        return f"{self.nombre} {self.apellido}"
    
    @property
    def foto_url(self):
        if self.foto and hasattr(self.foto, 'url'):
            return self.foto.url
        return '/static/images/default_coach.png'

class Arbitro(models.Model):
    TIPOS_ARBITRO = [
        ('PRIN', 'Árbitro Principal'),
        ('ASIS', 'Árbitro Asistente'),
        ('CUAR', 'Cuarto Árbitro'),
        ('VAR', 'Árbitro VAR'),
    ]
    
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField()
    nacionalidad = models.CharField(max_length=100)
    tipo = models.CharField(max_length=4, choices=TIPOS_ARBITRO, default='PRIN')
    experiencia_años = models.PositiveIntegerField(default=0)
    federacion = models.CharField(max_length=100, blank=True, null=True)
    foto = models.ImageField(upload_to='arbitros/', blank=True, null=True)  # ¡SIMPLIFICADO!
    
    def __str__(self):
        return f"{self.nombre} {self.apellido} ({self.get_tipo_display()})"
    
    @property
    def foto_url(self):
        if self.foto and hasattr(self.foto, 'url'):
            return self.foto.url
        return '/static/images/default_referee.png'