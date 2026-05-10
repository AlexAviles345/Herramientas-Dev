# Simulador Límite de Correos

Esta es una aplicación construida con **Spring Boot** para simular envíos continuos y repetitivos de correo electrónico. Es útil para observar y probar los límites de envío, bloqueos o timeouts del proveedor SMTP que estés utilizando.

## 🛠️ Tecnologías

- Java 17
- Spring Boot 3
- Maven

## 📋 Requisitos Previos

- Tener instalado Java 17 o superior.
- Una cuenta de correo electrónico SMTP (por ejemplo, Gmail).
- Si usas Gmail, necesitas generar una **App Password** (Contraseña de Aplicación) ya que las contraseñas normales no sirven para autenticación SMTP por seguridad.

## ⚙️ Configuración

Este proyecto utiliza variables de entorno para proteger tu información sensible (como correos y contraseñas). **¡Nunca subas tus contraseñas al repositorio!**

1. En la raíz del proyecto `simulador-limite-correos`, encontrarás un archivo llamado `.env.example`.
2. Haz una copia de ese archivo y renómbralo a `.env`.
3. Abre el archivo `.env` y llena tus credenciales reales:

```env
MAIL_HOST=smtp.gmail.com
MAIL_PORT=465
MAIL_USERNAME=tu_correo@gmail.com
MAIL_PASSWORD=tu_contraseña_de_aplicacion
MAIL_TO=correo_destino@ejemplo.com
MAIL_DELAY_MS=1000
```

*Nota: El archivo `.env` está ignorado en git (`.gitignore`), así que no se subirá accidentalmente a tu repositorio.*

## 🚀 Cómo Ejecutar

Una vez configurado tu archivo `.env`, abre una terminal en la carpeta `simulador-limite-correos` y ejecuta:

**En Windows:**
```bash
./mvnw.cmd spring-boot:run
```

**En macOS / Linux:**
```bash
./mvnw spring-boot:run
```

## 🛑 Comportamiento

La aplicación comenzará a enviar correos electrónicos al destinatario definido en `MAIL_TO`.
- El envío tiene un retraso definido por `MAIL_DELAY_MS` (por defecto 1 segundo).
- El programa llevará una cuenta de los correos enviados correctamente.
- Si ocurre algún error (por límite de envíos, bloqueo del proveedor, error de red), se contará como una falla.
- El envío se detendrá automáticamente después de **3 fallas consecutivas**.
