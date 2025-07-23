# Aplicación de Control CFDI

Una aplicación de escritorio para procesar archivos XML de CFDI (facturas electrónicas mexicanas) y llenar plantillas de control en Excel.

## 🎯 Project Overview

### Objetivo
Crear una aplicación de escritorio para controlar CFDI (Facturas) extrayendo datos de archivos XML y llenándolos en una plantilla de control de Excel.

### Visión
Una aplicación de escritorio construida con Python 3.11+, Tkinter para la interfaz gráfica, y módulos para procesamiento de Excel y XML para manejar carga, procesamiento de XML, y generación de archivos Excel llenos.

## 🚀 Características

- **Procesamiento XML**: Extraer datos CFDI de archivos XML de facturas
- **Integración Excel**: Llenar datos extraídos en plantilla de control Excel
- **Interfaz de Escritorio**: Interfaz amigable usando Tkinter
- **Procesamiento por Lotes**: Manejar múltiples archivos XML a la vez
- **Multiplataforma**: Ejecutable para Windows y macOS
- **Procesamiento Mensual**: Procesar facturas por año y mes

## 📋 Flujo de Trabajo

1. **Seleccionar Año y Mes** (interfaz desplegable)
2. **Cargar Plantilla Excel** (formato existente con 12 pestañas de meses)
3. **Seleccionar Múltiples Archivos XML** (asumidos del mes seleccionado)
4. **Procesar Archivos XML** (extraer datos usando mapeo predefinido)
5. **Llenar Plantilla Excel** (poblar pestaña del mes correspondiente)
6. **Generar Salida Descargable** (nuevo archivo con datos llenos + registro de procesamiento)

## 🛠️ Technical Stack

- **Python 3.11+**: Core programming language
- **Tkinter**: GUI framework for desktop application
- **openpyxl**: Excel file processing
- **lxml**: XML processing
- **PyInstaller**: Cross-platform executable creation

## 📁 Project Structure

```
cfdi_control/
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── gui/
│   │   ├── __init__.py
│   │   ├── main_window.py
│   │   └── components/
│   ├── core/
│   │   ├── __init__.py
│   │   ├── xml_parser.py
│   │   ├── excel_processor.py
│   │   └── data_models.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── validators.py
│   │   └── helpers.py
│   └── config/
│       ├── __init__.py
│       └── settings.py
├── tests/
├── docs/
├── resources/
├── requirements.txt
├── README.md
└── todo.md
```

## 🚀 Installation

### Prerequisites
- Python 3.11 or higher
- pip (Python package installer)

### Development Setup
1. Clone the repository
2. Create a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the application:
   ```bash
   python src/main.py
   ```

### Building Executables

#### Windows (.exe)
```bash
pyinstaller --onefile --windowed src/main.py --name CFDI_Control
```

#### macOS (.app)
```bash
pyinstaller --onefile --windowed src/main.py --name CFDI_Control
```

## 📊 CFDI XML to Excel Mapping

The application uses a predefined mapping to extract CFDI data:

| XML Path | Excel Column | Description |
|----------|-------------|-------------|
| `cfdi:Comprobante/@Fecha` | B | Date |
| `cfdi:Comprobante/@FormaPago` | C | Payment Method |
| `cfdi:Comprobante/@SubTotal` | D | Subtotal |
| `cfdi:Comprobante/@Descuento` | E | Discount |
| `cfdi:Comprobante/@Moneda` | F | Currency |
| `cfdi:Comprobante/@Total` | G | Total |
| `cfdi:Comprobante/@TipoDeComprobante` | H | Document Type |
| `cfdi:Comprobante/@MetodoPago` | I | Payment Method |
| `cfdi:Emisor/@Rfc` | J | Sender RFC |
| `cfdi:Emisor/@Nombre` | K | Sender Name |
| `cfdi:Emisor/@RegimenFiscal` | L | Sender Tax Regime |
| `cfdi:Receptor/@Rfc` | M | Receiver RFC |
| `cfdi:Receptor/@RegimenFiscalReceptor` | N | Receiver Tax Regime |
| `cfdi:Receptor/@UsoCFDI` | O | Receiver Uso CFDI |
| `cfdi:Impuestos/@TotalImpuestosTrasladados` | P | Total Taxes |

## 🧪 Testing

Run tests with pytest:
```bash
pytest tests/
```

## 📝 Development

### Code Style
- Use Black for code formatting
- Use flake8 for linting
- Follow PEP 8 guidelines

### Project Status
- **Current Phase**: Planning & Setup
- **Next Steps**: See `todo.md` for detailed roadmap

## 📄 License

[Add your license information here]

## 🤝 Contributing

[Add contribution guidelines here]

---

*Last updated: [Current Date]*
*Project Status: Development Phase* 