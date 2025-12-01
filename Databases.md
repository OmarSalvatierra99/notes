# What is a Database?

- It's a collection of data, a method for accessing and manipulating that data 

1. How to put data in DB
2. How to use/update/learn from data 
3. How to remove data

## Confusing Acronyms

DBMS: DataBase Management System
RDBMS: Relational DataBase Management System
SQL:  Structures Query Languages 

Data + DBMS or RDBMS = Databases

## Type of Databases

You can categorize databases into five main types:
### **1. Relational Database**

**Idea:** Data in tables (rows and columns).  
**Example:**

|id|name|email|
|---|---|---|
|1|Ana|ana@email.com|
|2|Diego|diego@email.com|

**Real systems:** MySQL, PostgreSQL

---

### **2. Document Database**

**Idea:** Data stored as documents (usually JSON).  
**Example:**

`{   "name": "Ana",   "email": "ana@email.com",   "hobbies": ["music", "reading"] }`

**Real systems:** MongoDB, CouchDB

---

### **3. Key–Value Database**

**Idea:** Data stored as simple key → value pairs.  
**Example:**

`"user1" → "Ana" "theme" → "dark-mode" "cart123" → ["itemA", "itemB"]`

**Real systems:** Redis, DynamoDB (key-value)

---

### **4. Graph Database**

**Idea:** Data as nodes and relationships.  
**Example:**

`Ana — is friends with — Diego   Ana — follows — Maria`

**Real systems:** Neo4j, JanusGraph

---

### **5. Wide Columnar Database**

**Idea:** Table-like, but each row can have different columns.  
**Example:**

|user_id|name|age|phone|favorite_food|
|---|---|---|---|---|
|1|Ana|23|555-1234|Pizza|
|2|Diego|||Tacos|

**Real systems:** Cassandra, Bigtable

- [[SQL]]