# 🔄 Cambiar a SQLite (Solución Rápida)

## Pasos para Cambiar a SQLite

### Paso 1: Editar el archivo `.env`

Abre el archivo `.env` en la raíz del proyecto y **comenta o elimina** la línea `DATABASE_URL`:

**ANTES:**
```env
SECRET_KEY=tu-secret-key
DATABASE_URL=postgresql://usuario:contraseña@localhost:5432/nombre_db
MONGO_URL=mongodb://localhost:27017/fitness
```

**DESPUÉS:**
```env
SECRET_KEY=tu-secret-key
# DATABASE_URL=postgresql://usuario:contraseña@localhost:5432/nombre_db
MONGO_URL=mongodb://localhost:27017/fitness
```

O simplemente elimina la línea `DATABASE_URL`.

### Paso 2: Detener el servidor

Si el servidor está corriendo, presiona `Ctrl + C` para detenerlo.

### Paso 3: Eliminar la base de datos SQLite anterior (si existe)

```powershell
# Eliminar el archivo db.sqlite3 si existe
del db.sqlite3
```

### Paso 4: Ejecutar migraciones

```powershell
python manage.py migrate
```

Esto creará todas las tablas en SQLite.

### Paso 5: Recrear los usuarios

```powershell
python crear_usuarios.py
```

### Paso 6: Reiniciar el servidor

```powershell
python manage.py runserver
```

### Paso 7: Probar

1. Inicia sesión con cualquier usuario
2. Intenta cerrar sesión - debería funcionar ahora ✅

---

## ¿Por qué funciona?

SQLite no requiere configuración de permisos como PostgreSQL. Es perfecto para desarrollo y pruebas.

---

## Volver a PostgreSQL después

Cuando quieras volver a PostgreSQL:

1. Descomenta `DATABASE_URL` en el `.env`
2. Otorga los permisos necesarios en PostgreSQL (ver `SOLUCION_PERMISOS_POSTGRESQL.md`)
3. Ejecuta `python manage.py migrate` nuevamente

