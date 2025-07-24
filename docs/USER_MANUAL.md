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
- En la sección "Selección de Período":
  - Seleccione el **Año** del menú desplegable
  - Seleccione el **Mes** del menú desplegable
- Esta selección determinará en qué pestaña del Excel se llenarán los datos

### 3. Cargar Plantilla Excel
- Haga clic en el botón "Seleccionar Plantilla Excel"
- Navegue hasta la ubicación de su plantilla de control
- Seleccione el archivo Excel (.xlsx)
- La aplicación validará que el archivo tenga las 12 pestañas de meses

### 4. Seleccionar Archivos XML
- Haga clic en el botón "Seleccionar Archivos XML"
- Navegue hasta la carpeta que contiene los archivos XML de CFDI
- Seleccione múltiples archivos XML (Ctrl+clic para selección múltiple)
- Los archivos deben ser CFDI válidos del período seleccionado

### 5. Procesar Archivos
- Haga clic en el botón "Procesar Archivos"
- La aplicación mostrará una barra de progreso
- Durante el procesamiento:
  - Se extraerán los datos de cada XML
  - Se validará la estructura de los archivos
  - Se mapearán los datos a las columnas correspondientes

### 6. Descargar Resultado
- Una vez completado el procesamiento, aparecerá el botón "Descargar Resultado"
- Haga clic para guardar el archivo Excel con los datos llenos
- El archivo se guardará con el nombre: `CFDI_Control_[AÑO]_[MES]_[FECHA].xlsx`

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
- Los nombres de las pestañas deben ser: Enero, Febrero, Marzo, etc.

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
- Verifique que el archivo tenga las 12 pestañas de meses
- Asegúrese de que los encabezados estén en la fila 3
- Verifique que el archivo no esté corrupto

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

### Versión 1.0.0
- Procesamiento básico de archivos XML CFDI
- Llenado automático de plantillas Excel
- Interfaz gráfica intuitiva
- Soporte para Windows y macOS
- Procesamiento por lotes de archivos XML

---

*Última actualización: [Fecha actual]*
*Versión del manual: 1.0* 