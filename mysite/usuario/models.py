from django.db import models
from django.contrib.auth.models import( AbstractBaseUser, BaseUserManager)

# Create your models here.

#actions dictionary
class ACTION_TYPE():
    Comprar = 'C'
    Eliminar_usuario = 'X'
    Editar_usuario = 'E'
    Crear_usuario = 'A'
    Eliminar_producto = 'L'
    Editar_producto = 'S'
    Crear_producto = 'B'
    choice= (
        (Comprar, 'Compra de productos'),
        (Eliminar_usuario, 'ELiminar usuario'),
        (Editar_usuario, 'Editar usuario'),
        (Crear_usuario, 'Crear usuario'),
        (Eliminar_producto, 'ELiminar producto'),
        (Editar_producto, 'Editar producto'),
        (Crear_producto, 'Crear producto')
        
    )
    
class userManager(BaseUserManager):
    def create_user(self,email,password=None, is_active=True, is_staff=False, is_admin=False):
        if not email:
            raise ValueError("EL usuario debe tener un correo electronico")
        if not password:
            raise ValueError("El usuario debe tener una contrasena")
        user_obj = self.model(
            email = self.normalize_email(email)
        )
        user_obj.set_password(password)
        user_obj.staff = is_staff
        user_obj.admin= is_admin
        user_obj.active=is_active
        user_obj.save(using=self._db)

        return user_obj
    
    def create_staffuser(self, email, password=None):
        user = self.create_user(
            email,
            password=password,
            is_staff=True
        )
        return user
    
    def create_superuser(self, email, password=None):
        user = self.create_user(
            email=email,
            password=password,
            is_staff=True,
            is_admin=True
        )

        return user



class tipo_usuario (models.Model):
    nombre = models.CharField(max_length=255)
    def __str__(self):
        return self.nombre



class usuario (AbstractBaseUser):
    nombre = models.CharField(max_length=255)
    apellido = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    tipo = models.ForeignKey(tipo_usuario, on_delete=models.CASCADE,null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(null=True, blank=True)

    is_active=models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)

    wallet = models.DecimalField(decimal_places=2,max_length=5, max_digits = 5,default = 0.00)

    
    #REQUIRED_FIELD = ['correo']

    USERNAME_FIELD = 'email'

    objects = userManager()

    def __str__(self):
        return self.email
    
    def get_full_name(self):
        return self.nombre +' '+ self.apellido

    def get_short_name(self):
        return self.nombre

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        if self.is_admin:
            return True
        return self.staff
        
    @property
    def is_admin(self):
        return self.admin 


class user_logs (models.Model):
    usuario = models.ForeignKey(usuario, on_delete=models.CASCADE)
    acciones = models.CharField(max_length = 1, choices = ACTION_TYPE.choice)
    action_date = models.DateTimeField(auto_now_add=True)
