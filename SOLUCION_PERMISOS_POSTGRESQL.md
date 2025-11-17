# 🔧 Solución: Error de Permisos en PostgreSQL

## Problema
```
permission denied for table django_session
```

Este error ocurre porque el usuario de PostgreSQL no tiene permisos para acceder a las tablas de Django.

## Soluciones

### Opción 1: Otorgar Permisos en PostgreSQL (Recomendado)

Conecta a PostgreSQL como superusuario y ejecuta:

```sql
-- Conectarse como superusuario (postgres)
psql -U postgres -d nombre_de_tu_base_datos

-- Otorgar todos los permisos al usuario
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO tu_usuario;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO tu_usuario;

-- Para tablas futuras
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO tu_usuario;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO tu_usuario;
```

**Reemplaza:**
- `nombre_de_tu_base_datos` con el nombre de tu base de datos
- `tu_usuario` con el usuario que estás usando en `DATABASE_URL`

### Opción 2: Usar SQLite Temporalmente (Más Fácil)

Si no necesitas PostgreSQL ahora, puedes usar SQLite temporalmente:

1. **Comenta o elimina la línea DATABASE_URL en tu `.env`:**
   ```env
   # DATABASE_URL=postgresql://usuario:contraseña@localhost:5432/nombre_db
   ```

2. **O edita `settings.py` para forzar SQLite:**
   ```python
   # Forzar SQLite para desarrollo
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.sqlite3',
           'NAME': BASE_DIR / 'db.sqlite3',
       }
   }
   ```

3. **Ejecuta migraciones:**
   ```powershell
   python manage.py migrate
   ```

4. **Vuelve a crear los usuarios:**
   ```powershell
   python crear_usuarios.py
   ```

### Opción 3: Usar el Usuario postgres

Si tienes acceso al usuario `postgres`, cambia tu `DATABASE_URL`:

```env
DATABASE_URL=postgresql://postgres:tu_password@localhost:5432/nombre_db
```

### Opción 4: Crear un Usuario con Permisos Completos

```sql
-- Conectarse como postgres
psql -U postgres

-- Crear usuario
CREATE USER tu_usuario WITH PASSWORD 'tu_password';

-- Crear base de datos
CREATE DATABASE nombre_db OWNER tu_usuario;

-- Conceder todos los privilegios
GRANT ALL PRIVILEGES ON DATABASE nombre_db TO tu_usuario;

-- Conectarse a la base de datos
\c nombre_db

-- Otorgar permisos en el esquema public
GRANT ALL ON SCHEMA public TO tu_usuario;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO tu_usuario;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO tu_usuario;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO tu_usuario;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO tu_usuario;
```

## Verificar Permisos

Para verificar qué permisos tiene tu usuario:

```sql
\du tu_usuario
\dp django_session
```

## Recomendación

Para desarrollo rápido, usa **Opción 2 (SQLite)**. Es más simple y no requiere configuración de permisos.

Para producción, usa **Opción 1** y configura correctamente los permisos en PostgreSQL.

