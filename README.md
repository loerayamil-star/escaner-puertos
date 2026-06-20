# Escáner de Puertos

Proyecto #5 de mi portafolio de Ingeniería en Computación — ruta DevSecOps.

Herramienta de escritorio para escanear puertos TCP en un host, con interfaz gráfica construida en Tkinter. Muestra en tiempo real qué puertos están abiertos, el servicio asociado, y el progreso del escaneo — sin congelar la ventana.

---

## Por qué lo hice

El escaneo de puertos es una de las técnicas base en seguridad ofensiva y defensiva. Construirlo desde cero, en lugar de solo usar `nmap`, me obligó a entender qué pasa por debajo: cómo funciona una conexión TCP, por qué los hilos son necesarios en interfaces gráficas, y cómo comunicar un hilo secundario con la UI de forma segura.

---

## Stack

| Tecnología | Uso |
|------------|-----|
| Python 3 | Lenguaje base |
| Tkinter + ttk | Interfaz gráfica (ventana, Treeview, Progressbar) |
| `socket` | Conexiones TCP para probar cada puerto |
| `threading` | Escaneo en hilo secundario para no congelar la UI |

---

## Interfaz

- **Campos de entrada:** host (default: `localhost`), puerto inicial y final
- **Botón de escaneo:** se deshabilita durante el escaneo para evitar ejecuciones simultáneas
- **Barra de progreso:** muestra el avance en tiempo real con porcentaje
- **Tabla de resultados (Treeview):** tres columnas — Puerto / Servicio / Estado

```
┌─────────────────────────────────────────┐
│  Host: [localhost    ]                  │
│  Puerto Inicial: [1  ]  Final: [1024]   │
│  [ Iniciar escaneo ]                    │
│  ████████████░░░░░░░░  Escaneando... 61%│
│                                         │
│  Puerto  │ Servicio  │ Estado           │
│  ─────────────────────────────          │
│  22      │ SSH       │ Abierto          │
│  80      │ HTTP      │ Abierto          │
│  443     │ HTTPS     │ Abierto          │
└─────────────────────────────────────────┘
```

---

## Cómo ejecutarlo

**Requisitos:** Python 3.8 o superior. No requiere dependencias externas.

```bash
git clone https://github.com/loerayamil-star/escaner-puertos.git
cd escaner-puertos
python3 escaner_puertos.py
```

---

## Conceptos técnicos que apliqué

**`connect_ex()` vs `connect()`**

`socket.connect()` lanza una excepción si el puerto está cerrado — manejarla con `try/except` en cada uno de los 1024 puertos sería ineficiente y verboso. `connect_ex()` devuelve `0` si la conexión fue exitosa o un código de error si falló, sin interrumpir el flujo. Eso permite escribir simplemente:

```python
return socket.connect_ex((host, puerto)) == 0
```

**Threading con `daemon=True`**

El hilo secundario se marca como daemon para que muera automáticamente si el usuario cierra la ventana, sin dejar procesos huérfanos en el sistema.

**Comunicación entre hilos con `root.after()`**

Tkinter no es thread-safe — un hilo secundario no puede modificar widgets directamente o la UI se corrompe. La solución es encolar la actualización en el hilo principal usando `root.after(0, lambda: ...)`, que ejecuta la función en el próximo ciclo del event loop de Tkinter.

```python
self.root.after(0, lambda: self.tabla.insert("", "end", values=(puerto, servicio, "Abierto")))
```

---

## Aviso de uso ético

> **Este programa es para uso en localhost o en redes de las que seas propietario o tengas autorización explícita.**
>
> Escanear puertos en sistemas ajenos sin permiso es ilegal en la mayoría de países y puede constituir un delito bajo leyes de acceso no autorizado a sistemas informáticos.
>
> Úsalo para aprender, auditar tu propia red, o en entornos de laboratorio controlados.

---

## Mejoras posibles

- [ ] Exportar resultados a `.txt` o `.csv`
- [ ] Soporte para escaneo UDP además de TCP
- [ ] Detección de versión de servicio (banner grabbing)
- [ ] Escaneo con múltiples hilos simultáneos para mayor velocidad
- [ ] Historial de escaneos anteriores

---

## Sobre el proyecto

Desarrollado como parte de una ruta de aprendizaje autodidacta en DevSecOps. Primera vez usando `socket` y `threading` de forma consciente — el objetivo fue entender los mecanismos, no solo hacer funcionar la herramienta.
