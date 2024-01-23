# Sr Backend Engineer Project

# Usage

## Build docker containers

```
docker-compose build
```

## Run the project

```
docker compose up
```

## Run tests

```
docker compose exec app python manage.py test
```

## Create superuser

```
docker compose exec app python manage.py createsuperuser
```

# Endpoint Details

### 1. Database Credentials Management

`POST /api/db-credentials/`

Add new database credentials to the system.

- **Request Body**:

  | Field    | Type   | Description                                     |
  | -------- | ------ | ----------------------------------------------- |
  | hostname | String | Database server hostname or IP.                 |
  | db_name  | String | Name of the database.                           |
  | username | String | Username for database access.                   |
  | password | String | Password for database access.                   |
  | port     | Int    | Port for database connection.                   |
  | db_type  | String | Type of the database (e.g., PostgreSQL, MySQL). |

- **Response**:
  - `201 Created`: Successfully added credentials.
  - `400 Bad Request`: Invalid data provided.

### 2. Retrieve Database Schema

#### `GET /api/db-schema/`

Retrieve the schema information of a specified database.

- **Query Parameters**:

  - `db_name`: (Required) The name of the database for which the schema is requested.

- **Response**:

  | Status Code     | Description                     |
  | --------------- | ------------------------------- |
  | 200 OK          | Successfully retrieved schema.  |
  | 404 Not Found   | Database credentials not found. |
  | 400 Bad Request | Database name not provided.     |

### 3. Search Table within Database

#### `GET /api/search-table/`

Search for a specific table within a database and retrieve its schema if it exists.

- **Query Parameters**:

  - `db_name`: (Required) The name of the database.
  - `table_name`: (Required) The name of the table to search for.

- **Response**:

  | Status Code     | Description                              |
  | --------------- | ---------------------------------------- |
  | 200 OK          | Table found and schema returned.         |
  | 404 Not Found   | Table or database credentials not found. |
  | 400 Bad Request | Required parameters not provided.        |

## DatabaseCredentials Data Model

### Entity Description

- **Name**: `DatabaseCredentials`
- **Purpose**: Stores the credentials and connection information for various databases.

### Attributes

- **hostname**:

  - **Type**: String
  - **Description**: The hostname or IP address of the database server.

- **db_name**:

  - **Type**: String
  - **Description**: The name of the database.

- **username**:

  - **Type**: String
  - **Description**: The username used for database access.

- **password**:

  - **Type**: String
  - **Description**: The password for database access, stored securely.

- **port**:

  - **Type**: Integer
  - **Description**: The port number through which the database is accessible.

- **db_type**:
  - **Type**: String
  - **Description**: The type of database (e.g., PostgreSQL, MySQL).

### Constraints and Indices

- **Primary Key**: Typically, an auto-generated ID.
- **Unique Constraints**: Depending on the use case, attributes like `db_name` might have unique constraints.
- **Indices**: Consider adding indices on frequently queried fields for performance optimization.

## High-Level Answers to Key Questions

### How would you implement authentication?

To implement authentication in this system, I would consider using token-based authentication, especially JWT (JSON Web Tokens). This approach would involve:

- **User Authentication Endpoint**: Create an endpoint for user login. Upon successful login, the server issues a JWT.
- **Token Verification**: Each subsequent request from the client should include this token in the header. The server decodes and verifies the token.
- **Integration with Django**: Utilize Django REST Framework's built-in support for token authentication.
- **Secure Storage of Tokens**: Ensure tokens are stored securely on the client side.
- **Token Expiry and Refresh**: Implement token expiry and provide a mechanism for token refresh.

### Scaling the System to Serve 1000s of Requests per Hour

To scale the system to handle thousands of requests per hour, the following strategies would be employed:

- **Load Balancing**: Use a load balancer to distribute incoming traffic across multiple server instances.
- **Database Optimization**: Optimize database queries and indexes, and consider read replicas for load distribution.
- **Caching**: Implement caching strategies to reduce database load, using tools like Redis.
- **Asynchronous Processing**: For non-critical, time-consuming tasks, use asynchronous processing.
- **Monitoring and Auto-scaling**: Monitor the system's performance and implement auto-scaling to adjust resources based on traffic.

### Supporting Databases with 10,000 Tables or Millions of Columns

To support databases with a vast number of tables or columns, changes in design would include:

- **Schema Management**: Implement dynamic schema management to efficiently handle a large number of tables and columns.
- **Query Optimization**: Carefully optimize queries to handle large datasets, possibly using more complex SQL statements.
- **Resource Allocation**: Ensure the database server has sufficient resources (memory, CPU) to handle large schemas.
- **Metadata Caching**: Cache database metadata to improve the efficiency of schema retrieval operations.
- **Modular Design**: For databases with extremely high complexity, consider a modular design that splits the schema into more manageable segments.
