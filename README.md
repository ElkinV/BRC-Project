# Proyecto de Conteo de Personas - API de Transmisión en Tiempo Real

Este proyecto implementa una API diseñada para la transmisión en tiempo real de datos de conteo de personas desde cámaras especializadas. La API, basada en **FastAPI** y **Server-Sent Events (SSE)**, facilita la actualización continua de datos entre cámaras de conteo de personas Hanwha y un sistema de base de datos, lo que permite a los usuarios recibir notificaciones en tiempo real de entradas y salidas de personas en distintas ubicaciones.

## Enfoque de Diseño

El sistema fue desarrollado utilizando **FastAPI** para crear una API robusta y eficiente, y está diseñado con patrones de software que facilitan la escalabilidad y mantenimiento:

- **Patrón Proxy**: Utilizado en la clase `ProxyDB`, que actúa como intermediario para la gestión de conexiones y consultas a la base de datos. Esto permite un control más preciso sobre la interacción con la base de datos, aplicando lógica adicional antes de ejecutar consultas o recuperar datos.
  
- **Patrón GRASP - Polimorfismo**: Empleado a través de la interfaz `IDBConnection`, que define métodos genéricos para conectar, desconectar y ejecutar consultas en la base de datos. Las implementaciones específicas, como `ProxyDB` y `SQLServerConnection`, permiten utilizar diferentes mecanismos de conexión sin cambiar la lógica principal de la API, facilitando la extensibilidad del sistema.

## Compatibilidad con Cámaras Hanwha

Este proyecto está diseñado específicamente para operar con cámaras **Hanwha** que tengan el módulo **People Counting** habilitado. Estas cámaras cuentan con capacidades avanzadas para detectar y contar personas en entradas y salidas de distintos espacios, lo que permite a la API obtener datos precisos y en tiempo real.

La integración con cámaras Hanwha permite a la API aprovechar los datos de conteo proporcionados por el módulo, manteniendo una comunicación continua y automatizada con el sistema de base de datos para actualizaciones y sincronización.

## Descripción General de la API

La API se comunica con las cámaras de conteo de personas a través de solicitudes periódicas, recuperando datos de conteo de entradas y salidas, y los actualiza en el sistema en tiempo real mediante eventos SSE. Esta arquitectura permite una comunicación de tipo "push" del servidor hacia el cliente, ideal para flujos de datos en tiempo real en aplicaciones de monitoreo de espacios físicos.

### Tecnologías y Protocolos Utilizados

- **FastAPI**: Framework para construir APIs rápidas y robustas en Python.
- **Server-Sent Events (SSE)**: Tecnología para transmitir datos del servidor al cliente en tiempo real, usando una conexión HTTP persistente.
- **Uvicorn**: Servidor ASGI para el despliegue de aplicaciones FastAPI, optimizado para rendimiento en tiempo real.
- **Starlette**: Infraestructura ASGI para manejar eventos en FastAPI.

### Diagrama de Diseño del Sistema

![Diseño del Sistema](Diseño%20del%20Sistema.png)

El diseño incluye los siguientes elementos clave:

1. **Interface IDBConnection**: Define los métodos necesarios para la conexión y ejecución de consultas en la base de datos, lo que permite una arquitectura modular y flexible.
2. **ProxyDB**: Actúa como un intermediario, gestionando las conexiones y consultas de forma segura y eficiente.
3. **SQLServerConnection**: Proporciona la implementación específica para conectar con SQL Server, incluyendo los datos de autenticación.
4. **SSEClient**: Responsable de gestionar el flujo de eventos SSE, manteniendo una lista de cámaras y administrando el buffer de transmisión.
5. **Camera**: Modelo de datos que representa las cámaras Hanwha, con atributos para almacenar los valores de conteo de personas según las reglas configuradas.

## Modelo de Dominio

El modelo de dominio describe la funcionalidad principal del sistema en términos de los objetos y sus relaciones en el contexto de la aplicación. La API actúa como el componente central, conectando las cámaras, la base de datos y el sistema de monitoreo.

### Diagrama del Modelo de Dominio

![Modelo de Dominio](Modelo%20de%20Dominio.png)

Este diagrama ilustra cómo interactúan los diferentes componentes dentro del dominio del sistema:

1. **Cámaras Hanwha**: Ubicadas en distintas sedes, las cámaras capturan los datos de conteo de personas.
2. **API-SSE**: Recibe peticiones a través de la SunAPI, actualiza la base de datos y transmite datos en tiempo real a los sistemas conectados.
3. **Base de Datos SQL Server**: Almacena los datos históricos de conteo, permitiendo una actualización continua.
4. **Dashboard**: Interfaz donde el Administrador del Sistema consulta los datos en tiempo real, integrándose con Power Automate para automatizar reportes.

El sistema está diseñado para ofrecer una transmisión de datos eficiente y un acceso confiable a los registros en tiempo real, facilitando la administración y el monitoreo de los flujos de personas en cada ubicación.

### Interacción con la Base de Datos

Aunque la API se centra en la transmisión de datos, interactúa con una base de datos SQL que almacena datos de entrada y salida de personas para cada cámara. Esta información se utiliza para comparar datos en tiempo real y, si se detectan discrepancias, se actualizan los registros para reflejar los nuevos valores de conteo.

- **Vista `API_camaras`**: La API consulta esta vista para obtener el estado de las cámaras activas, incluyendo su IP y datos de autenticación.
- **Tabla de Registros**: Los conteos de personas se almacenan en esta tabla, permitiendo un historial detallado de entradas y salidas por cámara.

## Diagrama de Componentes

El diagrama muestra la relación entre los distintos componentes del sistema. La API actúa como intermediario entre las cámaras y la base de datos, asegurando que los datos transmitidos se reflejen en la base de datos de manera sincronizada.

![Diagrama de Componentes](Diagrama_de_Componentes.png)

## Configuración e Instalación

### Requisitos Previos

- Python 3.8 o superior
- SQL Server o un entorno de base de datos compatible para almacenar los datos de conteo

### Instrucciones de Instalación

1. **Clonar el Repositorio**:
   ```bash
   git clone https://github.com/usuario/proyecto-conteo-personas.git
   cd proyecto-conteo-personas
   ```

2. **Configurar el Entorno Virtual**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # En Linux o MacOS
   .venv\Scripts\activate     # En Windows
   ```

3. **Instalar las Dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar la Base de Datos** (Opcional): Si deseas utilizar la base de datos, ejecuta el archivo SQL `PeopleCounting.sql` en SQL Server para crear la estructura necesaria.

5. **Iniciar la API**:
   ```bash
   uvicorn main:app --reload
   ```
   Esto ejecutará la API en `http://127.0.0.1:8000`.
