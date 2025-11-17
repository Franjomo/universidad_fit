# ⚡ Solución Rápida: Error al Cerrar Sesión

## Problema
Error: `permission denied for table django_session` al intentar cerrar sesión.

## Solución Rápida (2 minutos)

### Paso 1: Usar SQLite temporalmente

Edita tu archivo `.env` y **comenta o elimina** la línea de `DATABASE_URL`:

```env
SECRET_KEY=tu-secret-key
# DATABASE_URL=postgresql://...  <-- Comenta esta línea
MONGO_URL=mongodb://localhost:27017/fitness
```

O simplemente elimina/renombra la línea `DATABASE_URL`.

### Paso 2: Ejecutar migraciones

```powershell
python manage.py migrate
```

### Paso 3: Recrear usuarios

```powershell
python crear_usuarios.py
```

### Paso 4: Probar de nuevo

1. Inicia el servidor: `python manage.py runserver`
2. Inicia sesión con cualquier usuario
3. Cierra sesión - debería funcionar ahora

---

## Solución Permanente (PostgreSQL)

Si necesitas usar PostgreSQL, otorga permisos:

```sql
-- Conectarse como postgres
psql -U postgres -d tu_base_datos

-- Ejecutar estos comandos
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO tu_usuario;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO tu_usuario;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO tu_usuario;
```

Reemplaza `tu_usuario` con el usuario de tu `DATABASE_URL`.

---

## ¿Por qué pasa esto?

PostgreSQL requiere permisos explícitos para cada tabla. El usuario de tu `DATABASE_URL` no tiene permisos en las tablas de Django (como `django_session`).

SQLite no tiene este problema, por eso es más fácil para desarrollo.

