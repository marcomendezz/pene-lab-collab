# Tareas para Jarvis — Prioridad Alta

**Contexto:** Marco y Gonzalo van a tener un cliente juntos. Necesitamos el workspace de colaboración al 100%.

**Última actualización:** 2026-03-12 22:00 CST por Hermes

## Tareas Pendientes (en orden de prioridad)

### 1. ✅ Revisa los cambios de seguridad
- Hermes parcheó XSS en index.html, canvas.html
- CSP headers añadidos
- Realtime server hardened (rate limiting, input sanitization, localhost bind, origin check)
- **Commit:** `4350e90` — revisa y valida

### 2. ✅ Revisa el Dashboard v3
- Hermes rediseñó index.html completamente — Command Center theme
- **Commit:** `bd2c964`
- Si quieres ajustar colores/layout, hazlo

### 3. ✅ Revisa la Oficina Virtual Isométrica
- Nueva página: `docs/office.html`
- Agentes se mueven, speech bubbles, war room, desks, activity feed
- **Commit:** `cd57cd7`
- **TODO:** Agregar animaciones de caminar, mejorar sprites

### 4. 🔴 Configurar VS Code Live Share + SSH (PRIORIDAD CLIENTE)
- Marco y Gonzalo necesitan codear juntos en VSCode
- Plan: Live Share para los humanos + SSH tunnel para que los bots editen en real-time
- Hermes va a configurar el SSH server en la PC de Marco
- **Jarvis:** Configura lo equivalente en la PC de Gonzalo
- **Meta:** Los 4 (2 humanos + 2 bots) trabajando en el mismo codebase simultáneamente

### 5. 🟡 Crear estructura de projects/
- `projects/` folder ya existe en el repo
- Necesitamos definir con Marco y Gonzalo qué proyecto del cliente van a hacer
- Template de proyecto listo para arrancar

### 6. 🟡 Implementar agents-status.json
- Archivo JSON que ambos bots escriben con su status actual
- La oficina virtual (office.html) lo lee para mover los agentes automáticamente
- Formato propuesto:
```json
{
  "hermes": {"status": "working", "task": "Security hardening", "lastSeen": "2026-03-12T22:00:00"},
  "jarvis": {"status": "working", "task": "Dashboard updates", "lastSeen": "2026-03-12T22:00:00"}
}
```

## Resumen de lo que Hermes hizo hoy
1. Seguridad: XSS fix, CSP, rate limiting, input sanitization
2. Dashboard v3: Rediseño completo, dark theme, Command Center
3. Oficina virtual isométrica: office.html con agentes animados
4. Investigación: Lume HQ style virtual office implementation
5. Plan de colaboración VSCode para el equipo

## Comunicación
- Responde en chat.md cuando leas esto
- Si tienes preguntas, escríbelas ahí
- Marco y Gonzalo están en el grupo de Telegram "Pene Lab"
