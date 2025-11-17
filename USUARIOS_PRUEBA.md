# 🔐 Usuarios de Prueba - Universidad Fit

## Credenciales de Acceso

Usa estas credenciales para iniciar sesión en la aplicación:

### 👨‍💼 Administradores

| Usuario | Contraseña | Rol | Descripción |
|---------|------------|-----|-------------|
| `admin1` | `admin123` | ADMIN | Administrador principal |
| `admin` | `admin123` | ADMIN | Administrador |

**Acceso:** Panel de administración completo

---

### 👨‍🎓 Estudiantes

| Usuario | Contraseña | Rol | Descripción |
|---------|------------|-----|-------------|
| `estudiante1` | `estudiante123` | STUDENT | Juan Pérez |
| `estudiante2` | `estudiante123` | STUDENT | María García |
| `test` | `test123` | STUDENT | Test Usuario |

**Acceso:** Dashboard de estudiante, rutinas, ejercicios, progreso, reportes

---

### 👨‍🏫 Empleados / Entrenadores

| Usuario | Contraseña | Rol | Descripción |
|---------|------------|-----|-------------|
| `empleado1` | `empleado123` | EMPLOYEE | Carlos López |
| `entrenador1` | `entrenador123` | EMPLOYEE | Ana Martínez |

**Acceso:** Dashboard de entrenador, gestión de usuarios asignados

---

## 🚀 Cómo Usar

1. **Inicia el servidor:**
   ```powershell
   python manage.py runserver
   ```

2. **Abre tu navegador:**
   ```
   http://127.0.0.1:8000/accounts/login/
   ```

3. **Ingresa las credenciales** de cualquiera de los usuarios de arriba

4. **¡Listo!** Serás redirigido según tu rol:
   - **STUDENT/EMPLOYEE** → Dashboard de estudiante
   - **ADMIN** → Panel de administración

---

## 📝 Crear Más Usuarios

Si necesitas crear más usuarios, ejecuta:

```powershell
python crear_usuarios.py
```

Este script intentará crear usuarios adicionales usando los datos existentes en tu base de datos.

---

## ⚠️ Notas Importantes

- **Estas son credenciales de prueba** - Cámbialas en producción
- **Los usuarios ADMIN** tienen acceso completo al sistema
- **Los usuarios STUDENT** pueden crear rutinas, ejercicios y registrar progreso
- **Los usuarios EMPLOYEE** pueden funcionar como entrenadores

---

## 🔄 Restablecer Usuarios

Si necesitas eliminar y recrear los usuarios:

```powershell
python manage.py shell
```

```python
from accounts.models import User
User.objects.filter(username__in=['admin1', 'admin', 'estudiante1', 'estudiante2', 'test', 'empleado1', 'entrenador1']).delete()
exit()
```

Luego ejecuta nuevamente:
```powershell
python crear_usuarios.py
```

---

**Última actualización:** Usuarios creados exitosamente ✅

