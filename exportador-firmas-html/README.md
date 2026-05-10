# Instalador de Firma HTML

Una sencilla herramienta web estática para previsualizar y copiar firmas de correo electrónico con formato enriquecido (Rich Text) para que puedan ser utilizadas en Gmail o cualquier otro cliente de correo.

El problema que resuelve es que si intentas copiar el código HTML y pegarlo directamente en la configuración de firma de Gmail, no funciona correctamente. Con esta herramienta, la firma se inyecta directamente en el portapapeles con el formato MIME `text/html`, lo que te permite pegarla con formato usando `Ctrl+V`.

## 🛠️ Tecnologías

- HTML5
- CSS3 (Vanilla)
- JavaScript (Vanilla)

## 🚀 Cómo Utilizarlo

Este proyecto no requiere ninguna instalación o servidor de desarrollo.

1. Navega a la carpeta `exportador-firmas-html`.
2. Haz doble clic en el archivo `index.html` para abrirlo en tu navegador web de preferencia (Chrome, Edge, Firefox, etc.).
3. Verás una vista previa de la firma.
4. Haz clic en el botón **"📋 Copiar firma para Gmail"**.
5. Abre la [Configuración de Gmail](https://mail.google.com/mail/u/0/#settings/general).
6. Ve a la sección **Firma**, crea una nueva firma y pega el contenido con `Ctrl+V`.

## ✏️ Personalizar la Firma

Para poner tus propios datos sin riesgo de subirlos por accidente al repositorio, sigue estos pasos:

1. En la carpeta `exportador-firmas-html`, busca el archivo `config.js.example`.
2. Haz una copia de ese archivo y nómbralo **`config.js`**.
3. Abre el nuevo archivo `config.js` en cualquier editor de texto o código y coloca tu información real entre las comillas.
   ```javascript
   const firmaConfig = {
       iniciales: "TU",
       nombre: "Tu Nombre Real",
       // ... edita el resto de campos
   };
   ```
4. Guarda el archivo `config.js`. *(Nota: este archivo está protegido por `.gitignore` y no se subirá a tu repositorio).*
5. Abre o recarga la página `index.html` en tu navegador y verás tu nueva firma generada automáticamente y lista para copiar.
