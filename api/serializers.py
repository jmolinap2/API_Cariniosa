from asyncio import exceptions
from collections import defaultdict
from rest_framework import serializers
from django.contrib.auth import authenticate, login
from drf import settings
from django.contrib.auth import get_user_model
from .models import ProfessionalImage, User, Servicio,Profesional,Ciudad,Provincia,Pais ,ProfesionalServicio

#Registro de servicios
class ServicioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Servicio
        fields = '__all__'

class ProfesionalServicioRelacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfesionalServicio
        fields = '__all__'


#relacionar servicios con profesionales
class ProfesionalServicioSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfesionalServicio
        fields = '__all__'
#Login
        

#api\serializers.py
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(max_length=128, write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)

            if user:
                if not user.is_active:
                    raise serializers.ValidationError("Este usuario está desactivado.")

                return user
            else:
                raise serializers.ValidationError("Credenciales inválidas.")
        else:
            raise serializers.ValidationError("Se requiere un nombre de usuario y contraseña.")

# Usuario profesional, registro
class ProfessionalImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfessionalImage
        fields ='__all__'
        
#Registro de usuarios
class UserSerializer(serializers.ModelSerializer):
    professional_images = ProfessionalImageSerializer(many=True, read_only=True)
    password = serializers.CharField(write_only=True)  # Campo de contraseña solo para escritura
    class Meta:
        model = User
        fields ='__all__'
        read_only_fields = ('date_joined','last_login')

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        age = validated_data.pop('age', None)
        descripcion = validated_data.pop('descripcion', None)
        email = validated_data.pop('email', None)
        first_name = validated_data.pop('first_name', None)
        last_name = validated_data.pop('last_name', None)
        numero_celular = validated_data.pop('numero_celular', None)
        username = validated_data.pop('username', None)
        user = User(username=username, descripcion=descripcion,
                    email=email, first_name=first_name,
                    last_name=last_name, age=age,numero_celular=numero_celular ) #no debo poner lo demas datos de user?
        user.save() #no, eso es por default
        user.set_password(password)
        user.save() # como se hace para entrar en este modo? eso de debuguear f8, como pongo siguiente paso?

        # Obtener datos de grupos y manejar posibles errores
        groups_data = validated_data.pop('groups', None)
        if groups_data:
            try:
                # Usa groups.set() para asignar grupos correctamente
                user.groups.set(groups_data)
            except exceptions.ObjectDoesNotExist:
                # Maneja cualquier excepción potencial aquí, p.ej., registra o devuelve una respuesta de error
                ...

        return user
         
class ProfesionalSerializer(serializers.ModelSerializer):
    user = UserSerializer()  # Anidamos el UserSerializer aquí
    professional_images = ProfessionalImageSerializer(many=True, read_only=True)  # Agregamos las imágenes profesionales

    class Meta:
        model = Profesional
        fields = '__all__'
    def get_professional_images(self, obj):
        professional_images = obj.user.professional_images.all()
        return ProfessionalImageSerializer(professional_images, many=True).data
    def create(self, validated_data):
        user_data = validated_data.pop('user')
        password = user_data.pop('password', None)  # Extraer la contraseña del usuario
        user = User.objects.create_user(**user_data, password=password)
        professional = Profesional.objects.create(user=user, **validated_data)
        return professional
    

 
        
class UserProfesionalSerializer(serializers.ModelSerializer):
    user = UserSerializer()  # Anidar el UserSerializer aquí

    class Meta:
        model = Profesional
        fields = '__all__'

#ubicacion
class CiudadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ciudad
        fields = ['id', 'nombre', 'provincia']


class PaisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pais
        fields = ['id', 'nombre']


class ProvinciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Provincia
        fields = ['id', 'nombre', 'pais']