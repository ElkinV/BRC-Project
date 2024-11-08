# People Counting Project - Real-Time Transmission API

This project implements an API designed for real-time transmission of people counting data from specialized cameras. The API, built with **FastAPI** and **Server-Sent Events (SSE)**, facilitates continuous data updates from Hanwha people counting cameras to a database system, allowing users to receive real-time notifications of people entering and exiting various locations.

## Design Approach

The system was developed using **FastAPI** to create a robust and efficient API, and it is designed with software patterns that facilitate scalability and maintenance:

- **Proxy Pattern**: Used in the `ProxyDB` class, which acts as an intermediary for managing connections and queries to the database. This allows for more precise control over database interactions, applying additional logic before executing queries or retrieving data.

## Compatibility with Hanwha Cameras

This project is specifically designed to operate with **Hanwha** cameras that have the **People Counting** module enabled. These cameras feature advanced capabilities for detecting and counting people entering and exiting various spaces, allowing the API to capture accurate, real-time data.

The integration with Hanwha cameras enables the API to leverage counting data provided by the module, maintaining continuous and automated communication with the database system for updates and synchronization.

## API Overview

The API communicates with the people counting cameras through periodic requests, retrieving entry and exit counting data and updating it in real time via SSE. This architecture allows "push" communication from the server to the client, ideal for real-time data flows in physical space monitoring applications.

### Technologies and Protocols Used

- **FastAPI**: Framework for building fast and robust APIs in Python.
- **Server-Sent Events (SSE)**: Technology for transmitting data from the server to the client in real time, using a persistent HTTP connection.
- **Uvicorn**: ASGI server for deploying FastAPI applications, optimized for real-time performance.
- **Starlette**: ASGI infrastructure to handle events in FastAPI.

### System Design Diagram

![System Design](Diseño%20del%20Sistema.png)

The design includes the following key components:

1. **IDBConnection Interface**: Defines the necessary methods for database connection and query execution, enabling a modular and flexible architecture.
2. **ProxyDB**: Acts as an intermediary, securely and efficiently managing connections and queries.
3. **SQLServerConnection**: Provides the specific implementation for connecting to SQL Server, including authentication details.
4. **SSEClient**: Responsible for managing the SSE event stream, maintaining a list of cameras, and managing the transmission buffer.
5. **Camera**: Data model representing Hanwha cameras, with attributes for storing people counting values according to configured rules.

## Domain Model

The domain model describes the core functionality of the system in terms of the objects and their relationships within the application’s context. The API acts as the central component, connecting the cameras, database, and monitoring system.

### Domain Model Diagram

![Domain Model](Modelo%20de%20Dominio.png)

This diagram illustrates how the various components interact within the system domain:

1. **Hanwha Cameras**: Located at different sites, these cameras capture people counting data.
2. **API-SSE**: Receives requests through the SunAPI, updates the database, and transmits real-time data to connected systems.
3. **SQL Server Database**: Stores historical counting data, allowing continuous updates.
4. **Dashboard**: Interface where the System Administrator consults real-time data, integrating with Power Automate to automate reports.

The system is designed to offer efficient data transmission and reliable access to real-time records, facilitating administration and monitoring of people flows at each location.

### Database Interaction

Although the API focuses on data transmission, it interacts with an SQL database that stores entry and exit data for each camera. This information is used to compare real-time data, and if discrepancies are detected, the records are updated to reflect the new counting values.

- **API_camaras View**: The API queries this view to obtain the status of active cameras, including their IP and authentication details.
- **Records Table**: Stores people counting data, allowing a detailed history of entries and exits per camera.

## Components Diagram

The diagram shows the relationship between the system's various components. The API acts as an intermediary between the cameras and the database, ensuring that transmitted data is synchronized with the database.

![Components Diagram](Diagrama_de_Componentes.png)

## Setup and Installation

### Prerequisites

- Python 3.8 or higher
- SQL Server or a compatible database environment to store counting data

### Installation Instructions

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/user/people-counting-project.git
   cd people-counting-project
   ```

2. **Set Up the Virtual Environment**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Linux or macOS
   .venv\Scripts\activate     # On Windows
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
   
4. **Configure the `.env` File**: Create a `.env` file in the project root and add the necessary environment variables for database connections and camera authentication. Here is an example configuration:

   ```env
   DATABASE_URL=mssql+pyodbc://username:password@server/database
   DB_SERVER= your_server
   DB_PASSWORD = your_password
   DB_USER = your_user
   ```

   - `DATABASE_URL`: The connection string for SQL Server, including the username, password, server, and database name.
   - `CAMERA_USER`: The default username for authenticating with Hanwha cameras.
   - `CAMERA_PASSWORD`: The default password for authenticating with Hanwha cameras.


5. **Start the API**:
   ```bash
   uvicorn main:app --reload
   ```
   This will run the API at `http://127.0.0.1:8000`.
