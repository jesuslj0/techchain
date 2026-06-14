# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Proyecto

TechChain: red social enfocada a tecnología (estilo Instagram) construida con Django 5.1. Todo el contenido visible al usuario (templates, verbose_names, mensajes) está en español.

## Comandos

```bash
source venv/bin/activate              # venv local incluido en el repo (no versionado)
python manage.py runserver            # arranca con Daphne (ASGI), no con el runserver clásico
python manage.py test profiles        # tests (solo existen en profiles/tests/)
python manage.py test profiles.tests.test_models  # un módulo de test concreto
npm run build:css && npm run build:js # copia Bootstrap desde node_modules a static/
```

Requisitos para arrancar:
- **`.env` obligatorio** en la raíz: `base.py` lee `ZOHO_MAIL_SERVICE` y `ZOHO_MAIL_PASSWORD` con `os.environ[...]` (sin default), así que sin `.env` falla cualquier comando de manage.py. Variables: `SECRET_KEY`, `ZOHO_MAIL_*`, `DB_*`, `SENTRY_DSN`, `SOCIAL_AUTH_GOOGLE_CLIENT_ID/SECRET`.
- **Redis en `127.0.0.1:6379`** para el chat (channels-redis). El resto de la app funciona sin él.

## Settings y entornos

`techchain/settings/` dividido en `base.py` / `development.py` / `production.py`. `manage.py` apunta por defecto a `techchain.settings.development` (SQLite, DEBUG=True). Producción usa PostgreSQL, HTTPS forzado y configuración de SimpleJWT; se selecciona vía `DJANGO_SETTINGS_MODULE=techchain.settings.production`.

Ramas git: `develop` → `main` → `production`, con dos remotes (`origin` y `production`).

## Arquitectura

Apps Django: `techchain` (core), `profiles`, `posts`, `chat`, `notifications`, `api`.

**La app `techchain` centraliza lo transversal**, no solo la configuración:
- `techchain/templates/` — TODOS los templates del proyecto viven aquí (organizados por app: `posts/`, `profiles/`, `chat/`, `reels/`...), no en cada app.
- `techchain/forms/` — todos los formularios (un archivo por form), usados por las vistas de las demás apps.
- `techchain/views.py` — vistas generales: home, explore, login/logout/register, contacto, legal.
- `techchain/middleware/profile_completion.py` — redirige a todo usuario autenticado sin `bio` hacia `profiles:update` (excluye `/accounts/`, configurable con `PROFILE_EXCLUDE_URLS`). Tenlo en cuenta al probar flujos con usuarios nuevos.
- `techchain/context_processors/user_profile_context.py`, `templatetags/custom_filters.py`, `email/register_email.py`.

**Usuarios**: modelo custom `profiles.User` (`AbstractUser` + campo `uuid`). Las URLs públicas identifican al usuario por `uuid`, no por pk ni username. Un signal `post_save` en `profiles/signals.py` crea el `UserProfile` y envía el email de bienvenida al crear cada User (relevante en tests: crear un User dispara un envío de email real por SMTP). Los follows usan el modelo intermedio `Follow` (`UserProfile.followers`, asimétrico).

**Autenticación doble**: vistas clásicas propias (`/login/`, `/register/`) conviven con django-allauth (`/accounts/`, login por email con verificación obligatoria + Google OAuth). La API REST (`/api/`) usa DRF + SimpleJWT con throttling para registro.

**Contenido** (`posts`): `Post` (imagen + `RichTextField` de django-prose + tags de catálogo cerrado `Tag.TagChoices`), `Comment`, y `Reel` (vídeo) con sus `ReelComment`/`ReelLike`. Los likes de posts, comentarios y reels se hacen vía endpoints AJAX (`like_post_ajax`, etc.).

**Chat en tiempo real**: Channels + Daphne + Redis. `ChatRoom` (pk = uuid string, con subclase `GroupChatRoom` por herencia multi-tabla) y `Message`. WebSocket en `ws/chat/<room_id>/` gestionado por `chat/consumers.py` (`ChatConsumer`, async, con helpers `database_sync_to_async`). El routing está en `chat/routing.py` y se monta en `techchain/asgi.py`.

**Notificaciones**: se crean con `notifications.utils.create_notification(profile, type, post, message, link)`; tipos en `Notification.Type` (like, comment, post, follow, message).

**Frontend**: server-side rendering con templates Django + Bootstrap 5 (crispy-forms con pack bootstrap5). Bootstrap se sirve desde `static/` tras copiarlo de `node_modules` con los scripts de npm; no hay bundler.

**Sistema de diseño**: decisión tomada de **seguir con Bootstrap 5.3 (no migrar a Tailwind)** y construir un design system con CSS custom encima. `static/css/theme.css` es la fuente única de tokens (`:root` + `html.dark-mode`): color de acento, tipografía, espaciado, radios y sombras, además del **override de variables nativas de Bootstrap** (`--bs-primary`, `--bs-border-radius`, etc.) para que botones/inputs/cards hereden el estilo sin tocar cada página. Los componentes base (`.btn`, `.form-control`, títulos, cards) se definen una sola vez en `theme.css`; las hojas por-página (`login.css`, `register.css`...) deben consumir los tokens, no hardcodear valores. Al editar `theme.css` sube el cache-bust `?v=` en los layouts (`layout_basic/list/profile.html`).

# Comentarios y documentación

## Regla general

- Escribe el mínimo número de comentarios posible.
- Prioriza código legible, nombres descriptivos y funciones pequeñas antes que comentarios.
- Si algo puede entenderse leyendo el código, no lo comentes.

## Backend (Python, Django, APIs, servicios)

- Permitir comentarios únicamente para:
  - Algoritmos complejos.
  - Reglas de negocio no evidentes.
  - Optimizaciones de rendimiento.
  - Integraciones externas con comportamiento peculiar.
  - Soluciones a bugs o limitaciones conocidas.

- No comentar:
  - Variables.
  - Funciones obvias.
  - Consultas simples.
  - Validaciones evidentes.
  - Flujo normal de ejecución.

## Frontend (JavaScript / TypeScript)

- Evitar comentarios salvo cuando exista lógica compleja, estados difíciles de seguir o transformaciones de datos no evidentes.
- No comentar manipulación simple del DOM, eventos o llamadas estándar.

## Templates (Django, HTML)

- No añadir comentarios por defecto.
- Solo comentar bloques con lógica compleja o dependencias importantes.
- Nunca comentar estructura visual evidente.

## CSS / Tailwind

- Mantener comentarios al mínimo.
- Se permiten únicamente comentarios de agrupación para secciones grandes.

Ejemplo permitido:

/* Hero */
/* Navbar */
/* Footer */
/* Contact Form */

- No comentar propiedades individuales.
- No comentar reglas CSS evidentes.
- No añadir comentarios decorativos.

## Comentarios prohibidos

Evitar patrones como:

# Obtener usuario
# Crear objeto
# Actualizar datos
# Procesar respuesta
# Renderizar componente
# Estilos del botón
# Contenedor principal
# Sección de contenido

## Preferencia final

Cuando dudes entre comentar o no comentar, no comentes.