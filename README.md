# 🎓 Testify - CMS de Testimonios y Casos de Éxito

> Sistema CMS especializado en la gestión y publicación de testimonios para instituciones educativas y empresas del sector EdTech.

## 📋 Tabla de Contenidos

- [Acerca del Proyecto](#acerca-del-proyecto)
- [Características Principales](#caracteristicas-principales)
- [Arquitectura](#arquitectura)
- [Equipo](#equipo)

---

<a id="acerca-del-proyecto"></a>

## 🎯 Acerca del Proyecto

**Testify** es una plataforma CMS especializada que permite a instituciones educativas y empresas recopilar, organizar y publicar testimonios y casos de éxito de manera profesional y estructurada.

### Sector de Negocio

**EdTech** - Tecnología Educativa

### Necesidad del Cliente

Las instituciones y empresas con comunidades activas necesitan:

- Mostrar el impacto real de sus programas o productos
- Recopilar testimonios en múltiples formatos (texto, video, imagen)
- Contar con funciones de curaduría y moderación
- Analizar el engagement de los testimonios publicados

### Objetivo

Construir un sistema CMS que facilite la gestión integral del ciclo de vida de testimonios, desde su creación hasta su publicación y análisis de impacto.

---

<a id="caracteristicas-principales"></a>

## ✨ Características Principales

### Funcionalidades Core

- **📝 Gestión de Testimonios**

  - Creación y edición de testimonios con soporte multi-formato
  - Texto enriquecido, imágenes y videos
  - Editor intuitivo y responsive

- **🏷️ Clasificación y Organización**

  - Categorización por producto, evento, cliente o industria
  - Sistema de tags dinámico
  - Búsqueda inteligente y filtros avanzados

- **🔗 Integración Flexible**

  - API REST pública para integraciones
  - Embeds personalizables para sitios web externos
  - Webhooks para sincronización en tiempo real

- **✅ Moderación y Revisión**

  - Flujo de aprobación antes de publicación
  - Roles y permisos granulares
  - Historial de cambios y auditoría

- **📊 Analítica de Engagement**
  - Métricas de visualización y interacción
  - Dashboard de reportes
  - Exportación de datos

---

<a id="arquitectura"></a>

## 🏗️ Arquitectura

Testify es un CMS enfocado en la gestión y publicación de testimonios. El repositorio está organizado como monorepo; todo lo necesario para el desarrollo del backend está en [README.md](./Backend/README.md), la interfaz y documentacion del Frontend está en [README.md](./Frontend/README.md).

Puntos clave:

- Gestión y moderación de testimonios (texto, imagen, video).
- Seguridad y permisos: JWT + roles (admin/moderator/user).
- Persistencia: PostgreSQL.

### Commits Convencionales

Seguir [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` Nueva funcionalidad
- `fix:` Corrección de bug
- `docs:` Cambios en documentación
- `style:` Formato de código (sin cambios funcionales)
- `refactor:` Refactorización de código
- `test:` Agregar o modificar tests
- `chore:` Tareas de mantenimiento

**Ejemplos:**

```bash
feat: add video upload support to testimonials
fix: resolve authentication token expiration issue
docs: update API documentation for embed endpoints
refactor: optimize database queries in analytics service
```

---

<a id="equipo"></a>

## 👥 Equipo

**Equipo 40 - S11-25**

- Desarrolladores
- Project Manager
- Diseñadores

---

<div align="center">

**[⬆ Volver arriba](#-testify---cms-de-testimonios-y-casos-de-éxito)**

Hecho con ❤️ por el Equipo 40

</div>
