## **Project Request: Flask Web Application for SIAE**

### **1. Project Overview**

Create a Python Flask web application named **SIAE (Sistema Integral de Auditoría a Entes Estatales)**. This is a Spanish-language application for auditing state entities. The app must run on **port 5027**.

### **2. Core Application Requirements**

- Build an **interactive web interface** with Flask using a **classic HTML structure**.
    
- Implement **base.html template** with navigation, header, and footer.
    
- Create **catalog.html template** specifically for viewing and managing the catalog data.
    
- Implement **secure login system** with session-based authentication.
    
- Use **professional project structure** (modular templates, static files, separate routes).
    

### **3. Authentication System**

Pre-load two user accounts for testing:

- **Username:** `omar` | **Password:** `omar2025`
    
- **Username:** `enrique` | **Password:** `enrique2025`
    

### **4. Data Structure & Catalog Management**

The core feature is managing a primary data catalog. **Order preservation is critical**.

**Key Requirements:**

1. Analyze the provided Excel file structure and design an improved database schema using SQLAlchemy.
    
2. Add a required control field named **`Ejercicio`** (e.g., "Ejercicio 2025").
    
3. Add **filter functionality** for:
    
    - **`Ejercicio`** (year filter)
        
    - **`Fuentes de Financiamiento`** (funding sources filter)
        
4. Include a **sort-order field** to guarantee catalog order is maintained during all CRUD operations.
    
5. Catalog view must display all fields from the Excel example in the **exact original order**.
    

### **5. Template Structure Requirements**

**A. Base Template (base.html):**

- Standard HTML5 structure
    
- Bootstrap 5 for styling
    
- Navigation bar with: Inicio, Catálogo, Filtros, Cerrar Sesión
    
- Main content block (`{% block content %}`)
    
- Footer with application name
    

**B. Catalog Template (catalog.html):**

- Extends `base.html`
    
- Table displaying all catalog items
    
- **Dual filter system at the top:**
    
    1. Dropdown filter for `Ejercicio`
        
    2. Dropdown filter for `Fuentes de Financiamiento`
        
    3. "Aplicar Filtros" button
        
    4. "Limpiar Filtros" button
        
- Action buttons: Ver, Editar, Eliminar
    
- "Añadir Nuevo" button
    
- Pagination support if needed
    

**C. Filter Implementation:**

- Filters must work independently or together
    
- Server-side filtering (SQL queries)
    
- URL parameters for filter state preservation
    
- Clear visual indication of active filters
    

### **6. Database Schema Requirements**

Design SQLAlchemy models with:

- `id` (primary key)
    
- `ejercicio` (String, required) - for "Ejercicio 2025" format
    
- `fuente_financiamiento` (String) - for funding source
    
- `sort_order` (Integer) - to preserve original sequence
    
- All other fields from the Excel example in their original order
    
- Timestamps for created/updated
    

### **7. Complete Application Features**

1. **Login/Logout System** with session management
    
2. **Catalog Dashboard** with all items in original order
    
3. **Dual Filter System** (Ejercicio + Fuentes de Financiamiento)
    
4. **Full CRUD Operations**:
    
    - Create new catalog items
        
    - Read/view items with filters
        
    - Update existing items (preserving order)
        
    - Delete items with confirmation
        
5. **Data Validation** for all fields
    
6. **Spanish Language Interface** throughout
    

### **8. Required Files Structure**

text

siae_app/
├── app.py
├── config.py
├── requirements.txt
├── instance/
│   └── database.db
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── filters.js
├── templates/
│   ├── base.html
│   ├── login.html
│   ├── catalog.html      # Main catalog view with filters
│   ├── add_item.html
│   ├── edit_item.html
│   └── view_item.html
└── models.py

### **9. Filter Behavior Specifications**

- **Ejercicio Filter**: Dropdown with all unique years from database
    
- **Fuentes Filter**: Dropdown with all unique funding sources
    
- **Combined Filtering**: When both selected, show items matching BOTH criteria
    
- **URL Integration**: Filters should be bookmarkable via URL parameters
    
- **State Preservation**: Filters remain selected after page reload
    

### **10. Expected Output Format**

Please provide:

1. **Complete Database Schema** (SQLAlchemy models)
    
2. **Full Application Code** (all Python files)
    
3. **All HTML Templates** (with Bootstrap 5 integration)
    
4. **Filter Implementation Code** (both backend routes and frontend JavaScript)
    
5. **Setup & Run Instructions**
    
6. **Example Data** to populate the catalog
    

### **11. Additional Notes**

- Use Flask-SQLAlchemy for database ORM
    
- Use Flask-Login or manual session handling for authentication
    
- Implement secure password handling
    
- Include error handling and user feedback messages
    
- All text must be in Spanish
    
- Ensure responsive design works on desktop and tablet

```

```propm
|NUM|Nombre|Siglas|Clasificación|
|---|---|---|---|
|1|PODER EJECUTIVO DEL ESTADO DE TLAXCALA|EJECUTIVO|PODER DEL ESTADO|
|1.1|DESPACHO DE LA GOBERNADORA|DG|DEPENDENCIA|
|1.2|SECRETARÍA DE GOBIERNO|SEGOB|DEPENDENCIA|
|1.3|OFICIALIA MAYOR DE GOBIERNO|OMG|DEPENDENCIA|
|1.4|SECRETARÍA DE FINANZAS|SF|DEPENDENCIA|
|1.5|SECRETARÍA DE DESARROLLO ECONOMICO|SEDECO|DEPENDENCIA|
|1.6|SECRETARÍA DE TURISMO|SECTUR|DEPENDENCIA|
|1.7|SECRETARÍA DE INFRAESTRUCTURA|SI|DEPENDENCIA|
|1.8|SECRETARÍA DE EDUCACIÓN PÚBLICA|SEPE|DEPENDENCIA|
|1.9|SECRETARÍA DE MOVILIDAD Y TRANSPORTE|SMYT|DEPENDENCIA|
|1.10|SECRETARÍA DE LA FUNCIÓN PÚBLICA|SFP|DEPENDENCIA|
|1.11|SECRETARÍA DE IMPULSO AGROPECUARIO|SIA|DEPENDENCIA|
|1.12|COORDINACIÓN DE COMUNICACIÓN|CCOM|DEPENDENCIA|
|1.13|SECRETARÍA DE MEDIO AMBIENTE|SMA|DEPENDENCIA|
|1.14|SECRETARÍA DE CULTURA|SC|DEPENDENCIA|
|1.15|SECRETARÍA DE LAS MUJERES|SMET|DEPENDENCIA|
|1.16|SECRETARÍA DE ORDENAMIENTO TERRITORIAL Y VIVIENDA|SOTYV|DEPENDENCIA|
|1.17|SECRETARÍA DE SEGURIDAD CIUDADANA|SSC|DEPENDENCIA|
|1.18|COORDINACIÓN GENERAL DE PLANEACIÓN E INVERSIÓN|CGPI|DEPENDENCIA|
|1.19|SECRETARÍA DE BIENESTAR|SB|DEPENDENCIA|
|1.20|SECRETARÍA DE TRABAJO Y COMPETITIVIDAD|STYC|DEPENDENCIA|
|1.21|CONSEJERÍA JURÍDICA DEL EJECUTIVO|CJE|DEPENDENCIA|
|1.22|COORDINACIÓN ESTATAL DE PROTECCIÓN CIVIL|CEPC|DESCONCENTRADOS|
|1.23|SECRETARIADO EJECUTIVO DEL SISTEMA ESTATAL DE SEGURIDAD PÚBLICA|SESESP|DESCONCENTRADOS|
|1.24|INSTITUTO TLAXCALTECA DE DESARROLLO TAURINO|ITDT|DESCONCENTRADOS|
|1.25|INSTITUTO TLAXCALTECA DE ASISTENCIA ESPECIALIZADA A LA SALUD|ITAES|DESCONCENTRADOS|
|1.26|COMISIÓN ESTATAL DE ARBITRAJE MÉDICO|CEAM|DESCONCENTRADOS|
|1.27|CASA DE LAS ARTESANÍAS DE TLAXCALA|CAT|DESCONCENTRADOS|
|1.28|PROCURADURÍA DE PROTECCIÓN AL AMBIENTE DEL ESTADO DE TLAXCALA|PROPAET|DESCONCENTRADOS|
|1.29|INSTITUTO DE FAUNA SILVESTRE PARA EL ESTADO DE TLAXCALA|IFAST|DESCONCENTRADOS|
|2|PODER LEGISLATIVO DEL ESTADO DE TLAXCALA|LEGISLATIVO|PODERES DEL ESTADO|
|3|PODER JUDICIAL DEL ESTADO DE TLAXCALA|PJET|PODERES DEL ESTADO|
|4|CENTRO DE CONCILIACIÓN LABORAL DEL ESTADO DE TLAXCALA|CCLET|DESCENTRALIZADO/PARAESTATAL|
|5|COMISIÓN ESTATAL DEL AGUA Y SANEAMIENTO DEL ESTADO DE TLAXCALA|CEAS|DESCENTRALIZADO/PARAESTATAL|
|6|COLEGIO DE BACHILLERES DEL ESTADO DE TLAXCALA|COBAT|DESCENTRALIZADO/PARAESTATAL|
|7|COLEGIO DE EDUCACIÓN PROFESIONAL TÉCNICA DEL ESTADO DE TLAXCALA|CONALEP|DESCENTRALIZADO/PARAESTATAL|
|8|COLEGIO DE ESTUDIOS CIENTÍFICOS Y TECNOLÓGICOS DEL ESTADO DE TLAXCALA|CECYTE|DESCENTRALIZADO/PARAESTATAL|
|9|CONSEJO ESTATAL DE POBLACIÓN|COESPO|DESCENTRALIZADO/PARAESTATAL|
|10|COORDINACIÓN DE RADIO, CINE Y TELEVISIÓN|CORACYT|DESCENTRALIZADO/PARAESTATAL|
|11|EL COLEGIO DE TLAXCALA, A.C.|COLTLAX|DESCENTRALIZADO/PARAESTATAL|
|12|FIDEICOMISO DE LA CIUDAD INDUSTRIAL DE XICOTÉNCATL|FIDECIX|DESCENTRALIZADO/PARAESTATAL|
|13|COMISIÓN EJECUTIVA DE ATENCIÓN A VÍCTIMAS DEL ESTADO DE TLAXCALA|CEAVIT|DESCENTRALIZADO/PARAESTATAL|
|14|FONDO MACRO PARA EL DESARROLLO INTEGRAL DE TLAXCALA|FOMTLAX|DESCENTRALIZADO/PARAESTATAL|
|15|INSTITUTO DE CAPACITACIÓN PARA EL TRABAJO DEL ESTADO DE TLAXCALA|ICATLAX|DESCENTRALIZADO/PARAESTATAL|
|16|INSTITUTO DE CATASTRO DEL ESTADO DE TLAXCALA|IDC|DESCENTRALIZADO/PARAESTATAL|
|17|INSTITUTO DEL DEPORTE DE TLAXCALA|IDET|DESCENTRALIZADO/PARAESTATAL|
|18|INSTITUTO TECNOLÓGICO SUPERIOR DE TLAXCO|ITST|DESCENTRALIZADO/PARAESTATAL|
|19|INSTITUTO TLAXCALTECA DE LA INFRAESTRUCTURA FÍSICA EDUCATIVA|ITIFE|DESCENTRALIZADO/PARAESTATAL|
|20|INSTITUTO TLAXCALTECA DE LA JUVENTUD|ITJ|DESCENTRALIZADO/PARAESTATAL|
|21|INSTITUTO TLAXCALTECA PARA LA EDUCACIÓN DE LOS ADULTOS, ITEA|ITEA|DESCENTRALIZADO/PARAESTATAL|
|22|ÓRGANISMO PÚBLICO DESCENTRALIZADO SALUD DE TLAXCALA|OPD_SALUD|DESCENTRALIZADO/PARAESTATAL|
|23|PATRONATO CENTRO DE REHABILITACIÓN INTEGRAL Y ESCUELA EN TERAPIA FÍSICA Y REHABILITACIÓN|CRI-ESCUELA|DESCENTRALIZADO/PARAESTATAL|
|24|PATRONATO "LA LIBERTAD CENTRO CULTURAL DE APIZACO"|LA_LIBERTAD|DESCENTRALIZADO/PARAESTATAL|
|25|PENSIONES CIVILES DEL ESTADO DE TLAXCALA|PCET|DESCENTRALIZADO/PARAESTATAL|
|26|SISTEMA ESTATAL PARA EL DESARROLLO INTEGRAL DE LA FAMILIA|SEDIF|DESCENTRALIZADO/PARAESTATAL|
|27|UNIDAD DE SERVICIOS EDUCATIVOS DEL ESTADO DE TLAXCALA|USET|DESCENTRALIZADO/PARAESTATAL|
|28|UNIVERSIDAD POLITÉCNICA DE TLAXCALA|UPT|DESCENTRALIZADO/PARAESTATAL|
|29|UNIVERSIDAD POLITÉCNICA DE TLAXCALA REGIÓN PONIENTE|UPTREP|DESCENTRALIZADO/PARAESTATAL|
|30|UNIVERSIDAD TECNOLÓGICA DE TLAXCALA|UTT|DESCENTRALIZADO/PARAESTATAL|
|31|UNIVERSIDAD INTERCULTURAL DE TLAXCALA|UIT|DESCENTRALIZADO/PARAESTATAL|
|32|ARCHIVO GENERAL E HISTORICO DEL ESTADO DE TLAXCALA|AGHET|DESCENTRALIZADO/PARAESTATAL|
|33|TRIBUNAL DE JUSTICIA ADMINISTRATIVA DEL ESTADO DE TLAXCALA|TJA|ORGANISMO AUTÓNOMO|
|34|UNIVERSIDAD AUTÓNOMA DE TLAXCALA|UAT|ORGANISMO AUTÓNOMO|
|35|COMISIÓN ESTATAL DE DERECHOS HUMANOS|CEDH|ORGANISMO AUTÓNOMO|
|36|INSTITUTO TLAXCALTECA DE ELECCIONES|ITE|ORGANISMO AUTÓNOMO|
|37|INSTITUTO DE ACCESO A LA INFORMACIÓN PÚBLICA Y PROTECCIÓN DE DATOS PERSONALES DEL ESTADO DE TLAXCALA|IAIP|ORGANISMO AUTÓNOMO|
|38|TRIBUNAL DE CONCILIACIÓN Y ARBITRAJE DEL ESTADO DE TLAXCALA|TCYA|ORGANISMO AUTÓNOMO|
|39|TRIBUNAL ELECTORAL DE TLAXCALA|TET|ORGANISMO AUTÓNOMO|
|40|FISCALÍA GENERAL DE JUSTICIA DEL ESTADO DE TLAXCALA|FGJET|ORGANISMO AUTÓNOMO|
|41|SECRETARIA EJECUTIVA DEL SISTEMA ANTICORRUPCIÓN DEL ESTADO DE TLAXCALA|SESAET|ORGANISMO DESCENTRALIZADO NO SECTORIZADO|
|42|PATRONATO PARA LAS EXPOSICIONES Y FERIAS EN LA CIUDAD DE TLAXCALA|P_FERIA|PATRONATO|
```