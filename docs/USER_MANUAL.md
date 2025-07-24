# Manual de Usuario - Aplicación de Control CFDI

## 📋 Descripción General

La Aplicación de Control CFDI es una herramienta de escritorio diseñada para procesar archivos XML de CFDI (facturas electrónicas mexicanas) y llenar automáticamente plantillas de control en Excel.

### 🎯 Propósito
- Extraer datos de archivos XML de CFDI
- Llenar automáticamente plantillas de Excel con los datos extraídos
- Procesar múltiples archivos XML de forma simultánea
- Generar reportes de procesamiento

## 🚀 Instalación

### Requisitos del Sistema
- **Windows**: Windows 10 o superior
- **macOS**: macOS 10.14 o superior
- **Memoria**: Mínimo 4GB RAM
- **Espacio**: 100MB de espacio libre

### Instalación del Ejecutable

#### Windows
1. Descargue el archivo `CFDI_Control.exe` desde la sección de releases
2. Ejecute el archivo descargado
3. Siga las instrucciones del instalador

#### macOS
1. Descargue el archivo `CFDI_Control.app` desde la sección de releases
2. Arrastre la aplicación a la carpeta Aplicaciones
3. Ejecute la aplicación desde el Launchpad o Finder

## 📖 Guía de Uso

### 1. Iniciar la Aplicación
- Ejecute el archivo `CFDI_Control.exe` (Windows) o `CFDI_Control.app` (macOS)
- La aplicación se abrirá mostrando la ventana principal

### 2. Seleccionar Año y Mes
- En la sección "Seleccionar Año y Mes":
  - Seleccione el **Año** del menú desplegable (por defecto: 2025)
  - Seleccione el **Mes** del menú desplegable (nombres en español: Enero, Febrero, Marzo, etc.)
- **Nota**: El mes debe estar sin seleccionar inicialmente. Seleccione un mes antes de procesar.
- Esta selección determinará en qué pestaña del Excel se llenarán los datos

### 3. Cargar Plantilla Excel
- Haga clic en el botón "Examinar" junto al campo "Plantilla Excel"
- Navegue hasta la ubicación de su plantilla de control
- Seleccione el archivo Excel (.xlsx)
- La aplicación validará que el archivo tenga las 12 pestañas de meses
- **Nota**: Las pestañas del Excel deben tener nombres como "Ene2025", "Feb2025", etc.

### 4. Seleccionar Archivos XML
- Haga clic en el botón "Seleccionar Archivos" junto al campo "Archivos XML"
- Navegue hasta la carpeta que contiene los archivos XML de CFDI
- Seleccione múltiples archivos XML (Ctrl+clic para selección múltiple)
- Los archivos deben ser CFDI válidos del período seleccionado
- **Nota**: El botón "Procesar Archivos CFDI" se habilitará solo cuando todos los campos estén completos

### 5. Procesar Archivos
- Haga clic en el botón "Procesar Archivos CFDI" (solo habilitado cuando todos los campos estén completos)
- La aplicación mostrará una barra de progreso y estado del procesamiento
- Durante el procesamiento:
  - Se validará que la pestaña del mes seleccionado exista en el Excel
  - Se extraerán los datos de cada XML
  - Se validará la estructura de los archivos
  - Se mapearán los datos a las columnas correspondientes
- **Nota**: Si la pestaña del mes no existe en el Excel, se mostrará un error con las pestañas disponibles

### 6. Abrir Ubicación del Archivo
- Una vez completado el procesamiento, aparecerá el botón "Abrir Ubicación del Archivo"
- Haga clic para abrir la carpeta donde se guardó el archivo procesado
- El archivo se guardará automáticamente con el nombre: `CFDI_Control_[AÑO]_[MES]_[FECHA].xlsx`
- **Nota**: El archivo se crea automáticamente al completar el procesamiento. Este botón solo abre la ubicación.

## 📊 Mapeo de Datos

La aplicación extrae los siguientes datos de los archivos XML y los coloca en las columnas correspondientes del Excel:

| Campo XML | Columna Excel | Descripción |
|-----------|---------------|-------------|
| `cfdi:Comprobante/@Fecha` | B | Fecha del comprobante |
| `cfdi:Comprobante/@FormaPago` | C | Forma de pago |
| `cfdi:Comprobante/@SubTotal` | D | Subtotal |
| `cfdi:Comprobante/@Descuento` | E | Descuento |
| `cfdi:Comprobante/@Moneda` | F | Moneda |
| `cfdi:Comprobante/@Total` | G | Total |
| `cfdi:Comprobante/@TipoDeComprobante` | H | Tipo de comprobante |
| `cfdi:Comprobante/@MetodoPago` | I | Método de pago |
| `cfdi:Emisor/@Rfc` | J | RFC del emisor |
| `cfdi:Emisor/@Nombre` | K | Nombre del emisor |
| `cfdi:Emisor/@RegimenFiscal` | L | Régimen fiscal del emisor |
| `cfdi:Receptor/@Rfc` | M | RFC del receptor |
| `cfdi:Receptor/@RegimenFiscalReceptor` | N | Régimen fiscal del receptor |
| `cfdi:Receptor/@UsoCFDI` | O | Uso CFDI del receptor |
| `cfdi:Impuestos/@TotalImpuestosTrasladados` | P | Total de impuestos trasladados |

## ⚠️ Consideraciones Importantes

### Formato de Plantilla Excel
- La plantilla debe tener **12 pestañas** (una para cada mes)
- Los **encabezados** deben estar en la **fila 3**
- Los **datos** se llenarán a partir de la **fila 4**
- Los nombres de las pestañas deben ser: **Ene2025, Feb2025, Mar2025, Abr2025, May2025, Jun2025, Jul2025, Ago2025, Sep2025, Oct2025, Nov2025, Dic2025**
- **Nota**: El año en los nombres de las pestañas debe coincidir con el año seleccionado

### Archivos XML
- Deben ser archivos CFDI válidos
- Deben corresponder al período seleccionado
- Se procesarán todos los archivos seleccionados

### Procesamiento
- Solo se procesa **un mes por ejecución**
- Los datos existentes en la pestaña se **borrarán** antes de llenar
- Si un campo XML no existe, la celda correspondiente quedará **vacía**

## 🔧 Solución de Problemas

### Error: "Archivo Excel no válido"
- Verifique que el archivo tenga las 12 pestañas de meses con nombres correctos (Ene2025, Feb2025, etc.)
- Asegúrese de que los encabezados estén en la fila 3
- Verifique que el archivo no esté corrupto
- **Error específico**: "La pestaña 'X' no existe en la plantilla Excel" - Verifique que la pestaña del mes seleccionado exista

### Error: "Archivo XML no válido"
- Verifique que el archivo sea un CFDI válido
- Asegúrese de que el archivo no esté corrupto
- Verifique que el archivo corresponda al período seleccionado

### Error: "No se pueden procesar los archivos"
- Verifique que todos los archivos XML sean válidos
- Asegúrese de que correspondan al período seleccionado
- Verifique que tenga permisos de escritura en la carpeta de destino

### La aplicación no responde
- Cierre la aplicación y vuelva a abrirla
- Verifique que no haya otros procesos usando los archivos
- Reinicie su computadora si el problema persiste

### El botón "Procesar Archivos CFDI" está deshabilitado
- Asegúrese de haber seleccionado un año
- Asegúrese de haber seleccionado un mes
- Asegúrese de haber seleccionado un archivo Excel
- Asegúrese de haber seleccionado al menos un archivo XML
- El botón se habilitará automáticamente cuando todos los campos estén completos

## 📞 Soporte Técnico

Si encuentra algún problema o tiene preguntas:

1. **Revisar la documentación**: Consulte este manual y la documentación en línea
2. **Verificar archivos**: Asegúrese de que los archivos de entrada sean válidos
3. **Contactar soporte**: Envíe un reporte con:
   - Descripción del problema
   - Pasos para reproducir el error
   - Archivos de ejemplo (si es posible)
   - Información del sistema operativo

## 📝 Notas de la Versión

### Versión 1.1.0
- **Nuevo**: Validación de pestañas de mes en Excel antes del procesamiento
- **Nuevo**: Nombres de meses en español en la interfaz (Enero, Febrero, etc.)
- **Nuevo**: Botón "Abrir Ubicación del Archivo" en lugar de descarga
- **Nuevo**: Validación automática de campos - botón de procesar se habilita solo cuando todos los campos están completos
- **Mejorado**: Mensajes de error más detallados con información sobre pestañas disponibles
- **Mejorado**: Interfaz más intuitiva con estados de botones dinámicos
- Procesamiento básico de archivos XML CFDI
- Llenado automático de plantillas Excel
- Interfaz gráfica intuitiva
- Soporte para Windows y macOS
- Procesamiento por lotes de archivos XML

---

*Última actualización: Enero 2025*
*Versión del manual: 1.1* 