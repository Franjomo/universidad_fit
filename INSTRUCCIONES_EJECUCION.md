# 🚀 Instrucciones para Ejecutar la Aplicación

## ⚡ Inicio Rápido (3 pasos)

### 1. Verifica que tienes el archivo `.env`
Si no lo tienes, crea uno en la raíz del proyecto (donde está `manage.py`) con:
```env
SECRET_KEY=tu-secret-key-aqui
DATABASE_URL=postgresql://usuario:contraseña@localhost:5432/nombre_db
MONGO_URL=mongodb://localhost:27017/fitness
```
**Nota:** Si no tienes PostgreSQL/MongoDB configurados, puedes omitir esas líneas. El proyecto usará SQLite por defecto.

Ver más detalles en `CREAR_ENV.md`

### 2. Abre PowerShell o CMD en la carpeta del proyecto
```powershell
cd "C:\Users\jeanc\Desktop\universidad\SID\SID 2\prroyecto final\universidad_fit"
```

### 3. Ejecuta el servidor
```powershell
python manage.py runserver
```

### 4. Abre tu navegador
```
http://127.0.0.1:8000/
```

**¡Eso es todo!** Si hay errores, sigue leyendo las soluciones abajo.

---

## 📋 Pasos Detallados

### Paso 1: Verificar Python
```powershell
python --version
```
Debe mostrar Python 3.x. Si no funciona, prueba con `python3` o `py`.

### Paso 2: Navegar al proyecto
```powershell
cd "C:\Users\jeanc\Desktop\universidad\SID\SID 2\prroyecto final\universidad_fit"
```

### Paso 3: Verificar que existe manage.py
```powershell
dir manage.py
```

### Paso 4: Ejecutar migraciones (si es la primera vez)
```powershell
python manage.py migrate
```

### Paso 5: Crear un usuario de prueba (opcional)
```powershell
python manage.py shell
```
Luego en el shell de Python:
```python
from accounts.models import User
user = User.objects.create_user(username='test', password='test123', role='STUDENT')
exit()
```

### Paso 6: Ejecutar el servidor
```powershell
python manage.py runserver
```

Deberías ver algo como:
```
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

### Paso 7: Abrir en el navegador
Abre tu navegador y ve a: **http://127.0.0.1:8000/**

---

## 🔧 Solución de Problemas Comunes

### ❌ Error: "DATABASE_URL no encontrado"
**Solución:** El proyecto ahora usa SQLite por defecto si no hay `.env`. Esto está bien para desarrollo.

Si quieres usar PostgreSQL, crea un archivo `.env` en la raíz del proyecto:
```
DATABASE_URL=postgresql://usuario:contraseña@localhost:5432/nombre_db
SECRET_KEY=tu-secret-key-aqui
MONGO_URL=mongodb://localhost:27017/fitness
```

### ❌ Error: "No module named 'django'"
**Solución:** Instala Django:
```powershell
pip install django
```

O instala todas las dependencias:
```powershell
pip install -r requirements.txt
```

### ❌ Error: "TemplateDoesNotExist"
**Solución:** Verifica que existan las carpetas:
- `templates/`
- `templates/base.html`
- `templates/accounts/login.html`
- `templates/core/home.html`

### ❌ Error: "Static files not found"
**Solución:** En desarrollo, Django debería servir los archivos estáticos automáticamente. Si no funciona:
```powershell
python manage.py collectstatic --noinput
```

### ❌ Error: "ModuleNotFoundError"
**Solución:** Asegúrate de estar en el directorio correcto y que todas las apps estén en `INSTALLED_APPS` en `settings.py`.

### ❌ Error: "Port 8000 already in use"
**Solución:** Usa otro puerto:
```powershell
python manage.py runserver 8001
```

---

## 🎯 URLs Disponibles

Una vez que el servidor esté corriendo:

- **🏠 Página de inicio**: http://127.0.0.1:8000/
- **🔐 Login**: http://127.0.0.1:8000/accounts/login/
- **📊 Dashboard**: http://127.0.0.1:8000/fitness/dashboard/ (requiere login)
- **💪 Rutinas**: http://127.0.0.1:8000/fitness/routines/
- **🏋️ Ejercicios**: http://127.0.0.1:8000/fitness/exercises/
- **📈 Progreso**: http://127.0.0.1:8000/fitness/progress/
- **📊 Reportes**: http://127.0.0.1:8000/fitness/reports/
- **⚙️ Admin Django**: http://127.0.0.1:8000/admin/

---

## 🔐 Crear Usuario para Probar

### Opción 1: Desde el shell de Django
```powershell
python manage.py shell
```
```python
from accounts.models import User

# Crear estudiante
user = User.objects.create_user(
    username='estudiante1',
    password='test123',
    role='STUDENT'
)
print(f"Usuario creado: {user.username}")

# Crear administrador
admin = User.objects.create_user(
    username='admin1',
    password='admin123',
    role='ADMIN',
    is_staff=True
)
print(f"Admin creado: {admin.username}")

exit()
```

### Opción 2: Desde el admin de Django
1. Crea un superusuario:
   ```powershell
   python manage.py createsuperuser
   ```
2. Ve a http://127.0.0.1:8000/admin/
3. Inicia sesión y crea usuarios desde ahí

---

## 📝 Comandos Útiles

### Verificar configuración
```powershell
python manage.py check
```

### Ver todas las URLs
```powershell
python manage.py show_urls
```
(Requiere instalar: `pip install django-extensions`)

### Limpiar cache
```powershell
python manage.py clear_cache
```

### Ver errores detallados
Si hay errores, Django los mostrará en la consola. También puedes verlos en el navegador si `DEBUG = True` en `settings.py`.

---

## 🚨 Si Nada Funciona

1. **Verifica que estás en la carpeta correcta:**
   ```powershell
   pwd
   # Debe mostrar: ...\universidad_fit
   ```

2. **Verifica que Python funciona:**
   ```powershell
   python --version
   ```

3. **Verifica que Django está instalado:**
   ```powershell
   python -c "import django; print(django.get_version())"
   ```

4. **Reinstala dependencias:**
   ```powershell
   pip install -r requirements.txt --upgrade
   ```

5. **Verifica la configuración:**
   ```powershell
   python manage.py check
   ```

---

## ✅ Checklist de Verificación

Antes de ejecutar, verifica:

- [ ] Estás en la carpeta `universidad_fit`
- [ ] Python está instalado y funciona
- [ ] Django está instalado
- [ ] Existe el archivo `manage.py`
- [ ] Existe la carpeta `templates/`
- [ ] Existe la carpeta `static/`
- [ ] Has ejecutado `python manage.py migrate` al menos una vez
- [ ] Tienes un usuario creado para probar el login

---

## 🎉 ¡Listo!

Si seguiste estos pasos, tu aplicación debería estar funcionando. 

**Para detener el servidor:** Presiona `Ctrl + C` en la terminal.

**¿Tienes algún error específico?** Copia el mensaje de error completo y busca en la sección "Solución de Problemas" arriba.
