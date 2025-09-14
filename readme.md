

---

## 📌 README.md

````markdown
# 📦 Realtime Orders API (FastAPI + MySQL)

A simple **Realtime Orders Management System** built with **FastAPI**, **MySQL**, and **WebSockets**.  
The app allows you to:
- Insert or update orders in MySQL.
- Broadcast changes to all connected clients **in real-time** using WebSockets.

---

## 🚀 Features
- **FastAPI** for REST API & WebSocket server
- **MySQL** as the database
- **aiomysql** for async DB connection pooling
- **WebSocket** support for real-time updates
- Minimal front-end client for testing

---

## 🛠️ Installation & Setup

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/realtime-orders.git
cd realtime-orders
````

### 2️⃣ Create Virtual Environment

On Windows (PowerShell):

```bash
python -m venv venv
venv\Scripts\activate
```

On Mac/Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🗄️ Database Setup (MySQL)

### 1️⃣ Log in to MySQL

```bash
mysql -u root -p
```

### 2️⃣ Create Database & User

```sql
CREATE DATABASE orders_db;
CREATE USER 'db_user'@'localhost' IDENTIFIED BY 'yourpassword';
GRANT ALL PRIVILEGES ON orders_db.* TO 'db_user'@'localhost';
FLUSH PRIVILEGES;
```

### 3️⃣ Create Table

```sql
USE orders_db;
CREATE TABLE orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    customer_name VARCHAR(100),
    product_name VARCHAR(100),
    status ENUM('pending', 'shipped', 'delivered') DEFAULT 'pending',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

---

## ⚙️ Configure Environment Variables

Create a `.env` file in the project root:

```ini
DB_HOST=localhost
DB_PORT=3306
DB_USER=db_user
DB_PASSWORD=yourpassword
DB_NAME=orders_db
```

---

## ▶️ Run the Server

```bash
uvicorn main:app --reload
```

Expected output:

```
🔄 Connecting to database...
✅ Database connected
```

Visit [http://127.0.0.1:8000](http://127.0.0.1:8000) → You should see:

```json
{"message":"Realtime Orders API is running 🚀"}
```

---

## 🌐 WebSocket Client

Create a file `client.html`:

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Realtime Orders Client</title>
</head>
<body>
  <h1>📦 Realtime Orders Updates</h1>
  <ul id="updates"></ul>

  <script>
    const socket = new WebSocket("ws://127.0.0.1:8000/ws");

    socket.onopen = () => console.log("✅ Connected to WebSocket");

    socket.onmessage = (event) => {
      const data = JSON.parse(event.data);
      const li = document.createElement("li");
      li.textContent = `Order #${data.id} | ${data.customer_name} | ${data.product_name} | ${data.status} | ${data.updated_at}`;
      document.getElementById("updates").appendChild(li);
    };

    socket.onclose = () => console.log("❌ Disconnected from WebSocket");
  </script>
</body>
</html>
```

Open `client.html` in a browser.

---

## 🧪 Test the Realtime System

Insert a new order:

```sql
INSERT INTO orders (customer_name, product_name, status)
VALUES ('Alice', 'Laptop', 'pending');
```

Update an order:

```sql
UPDATE orders
SET status = 'shipped'
WHERE id = 1;
```

You should see **live updates** appear instantly in the browser.

---

## 📜 API Endpoints

| Method | Endpoint | Description                          |
| ------ | -------- | ------------------------------------ |
| GET    | `/`      | Returns a welcome message            |
| WS     | `/ws`    | Connect to realtime WebSocket stream |

---

## 🏗️ Tech Stack

* **Backend:** FastAPI
* **Database:** MySQL
* **WebSocket:** Starlette / Uvicorn
* **ORM:** aiomysql (async connection pool)

---

## 📌 Notes

* You must have **MySQL running** locally.
* Use `.env` to configure DB connection.
* You can easily deploy this on **Railway**, **Render**, or **Docker**.

---

```

---

Would you like me to include **Docker support** in this README (so that MySQL + FastAPI can run with a single `docker-compose up`)? This would make it super easy for others to run your project.
```
