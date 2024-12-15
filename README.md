
# 🎂 Cakery

An online bakery platform where customers can browse, customize, and order cakes and pastries, with features for store staff to manage logistics and operations.

---

## 🌟 Features

### 👥 Customer Features:
- 🛍️ Browse available products and customize cakes.
- 🛒 Add products to the cart and place orders.
- 📜 View order history, track order status, and leave reviews.

### 🛠️ Admin Features:
- 🧑‍💼 Manage customer and staff data.
- 📊 Access analytics and view platform performance reports.

### 👩‍🍳 Baker Features:
- 🧾 View assigned orders and update order status.

### 🚚 Delivery Features:
- 🚦 View assigned orders and update delivery status.

---

## 🖥️ Technologies Used
- **Frontend:** ⚛️ Next.js  
- **Backend:** 🐍 Flask (Python)  
- **Database:** 🐘 PostgreSQL  
- **APIs and Libraries:** 🌐 Gemini API (if applicable)  

---

## ⚙️ Setup and Installation

Follow the steps below to set up the project on your local machine.

---

### 1️⃣ Clone the Repository
Clone the project repository to your local machine:  
```bash
git clone https://github.com/Anas-Ah25/Cakery.git
```

Navigate to the project directory:
```bash
cd Cakery
```

---

### 2️⃣ Set Up the Database

#### 🗃️Load the Database
1. Ensure PostgreSQL is installed on your system and the `psql` command-line tool is accessible.

2. Create an empty database. For example, to create a database named `cakery`, run:
   ```bash
   createdb -U postgres cakery
   ```

3. Load the database schema and data:
   - Use the provided backup file `CakeryDB_backup_populated_Tr4.sql`:
     ```bash
     psql -U postgres -d cakery -f "/path/to/CakeryDB_backup_populated_Tr2.sql"
     ```
     Replace `/path/to` with the actual path where the `.sql` file is located.

4. (Optional) If prompted for the PostgreSQL password, you can temporarily set it in the terminal:
   ```bash
   set PGPASSWORD=your_postgres_password
   ```
   Replace `your_postgres_password` with your actual PostgreSQL password.

5. Confirm the database is populated:
   ```bash
   psql -U postgres -d cakery
   ```

---

### 3️⃣ Set Up the Backend
1. Navigate to the backend folder:
   ```bash
   cd app
   ```

2. Install the required Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure the environment variables:
   - Create a `.env` file in the backend directory:
     ```bash
     touch .env
     ```
   - Use the provided `.env.example` file as a reference:
     ```bash
     cp .env.example .env
     ```
   - Update the `.env` file with your database credentials. For example:
     ```
     DATABASE_URL=postgresql://username:password@localhost/cakery
     ```
     Replace `username`, `password`, and `cakery` with your PostgreSQL username, password, and database name.

4. Start the backend server:
   ```bash
   flask run
   ```
   The backend will run on `http://127.0.0.1:5000`.

---

### 4️⃣ Set Up the Frontend
1. Navigate to the frontend folder:
   ```bash
   cd frontend
   ```

2. Install the required dependencies:
   ```bash
   npm install
   ```

3. Start the frontend development server:
   ```bash
   npm run dev
   ```
   The frontend will run on `http://localhost:3000`.

---

### 5️⃣ Open the Application
Once the frontend and backend are running:

- 🌐 Frontend: [http://localhost:3000](http://localhost:3000)
- 🌐 Backend: [http://127.0.0.1:5000](http://127.0.0.1:5000)
