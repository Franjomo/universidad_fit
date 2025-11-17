# 📝 Cómo Crear el Archivo .env

## Pasos Rápidos

### 1. Crea el archivo `.env` en la raíz del proyecto
La raíz es la carpeta donde está `manage.py`:
```
universidad_fit/
├── manage.py
├── .env          ← Aquí debe estar este archivo
├── universidad_fit/
└── ...
```

### 2. Copia el contenido del archivo `.env.example`
O crea el archivo manualmente con este contenido mínimo:

```env
SECRET_KEY=tu-secret-key-aqui
DATABASE_URL=postgresql://usuario:contraseña@localhost:5432/nombre_db
MONGO_URL=mongodb://localhost:27017/fitness
```

### 3. Reemplaza los valores con tus datos reales

#### SECRET_KEY
Genera uno nuevo con este comando:
```powershell
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

O usa este valor temporal para desarrollo:
```
SECRET_KEY=django-insecure-dev-key-change-in-production-12345
```

#### DATABASE_URL
Formato: `postgresql://usuario:contraseña@host:puerto/nombre_base_datos`

Ejemplo:
```
DATABASE_URL=postgresql://postgres:mipassword@localhost:5432/universidad_fit
```

**Si no tienes PostgreSQL configurado**, simplemente NO pongas esta línea o déjala vacía. El proyecto usará SQLite automáticamente.

#### MONGO_URL
Formato: `mongodb://host:puerto/nombre_base_datos`

Ejemplo:
```
MONGO_URL=mongodb://localhost:27017/fitness
```

**Si no tienes MongoDB**, déjala vacía o comenta la línea con `#`.

## Ejemplo Completo de .env

```env
# Secret Key (genera uno nuevo para producción)
SECRET_KEY=django-insecure-dev-key-change-in-production-12345

# Base de datos PostgreSQL (opcional - si no está, usa SQLite)
DATABASE_URL=postgresql://postgres:password@localhost:5432/universidad_fit

# MongoDB para modelos de fitness (opcional)
MONGO_URL=mongodb://localhost:27017/fitness
```

## ⚠️ Importante

1. **NUNCA subas el archivo `.env` a Git** - Ya debería estar en `.gitignore`
2. **Usa valores diferentes para desarrollo y producción**
3. **Mantén el SECRET_KEY secreto** - Nunca lo compartas

## ✅ Verificar que Funciona

Después de crear el `.env`, verifica que todo esté bien:

```powershell
python manage.py check
```

Si no hay errores, ¡está todo configurado correctamente!

## 🚀 Siguiente Paso

Ahora puedes ejecutar el servidor:

```powershell
python manage.py runserver
```

