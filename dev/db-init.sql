-- Step 1: Create Market Table
CREATE TABLE markets (
    market_id SERIAL PRIMARY KEY,
    market_name VARCHAR(255),
    latitude DECIMAL(9, 6),
    longitude DECIMAL(9, 6),
    created_date DATE
);

-- Step 2: Create Product Table
CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    product_name VARCHAR(255),
    category VARCHAR(255),
    price DECIMAL(10, 2),
    created_date DATE
);

-- Step 3: Create User Table
CREATE TABLE app_users (
    user_id SERIAL PRIMARY KEY,
    fio VARCHAR(255),
    username VARCHAR(255) UNIQUE,
    hashed_password TEXT,
    user_type VARCHAR(50),
    phone VARCHAR(50),
    email VARCHAR(255),
    created_date DATE
);

-- Step 4: Create Goods Availability Table
CREATE TABLE goods_availability (
    availability_id SERIAL PRIMARY KEY,
    market_id INT REFERENCES markets(market_id),
    product_id INT REFERENCES products(product_id),
    available_quantity INT,
    inventarization_date DATE
);

-- Step 5: Create Supply Metadata Table
CREATE TABLE supply_metadata (
    supply_id SERIAL PRIMARY KEY,
    market_id INT REFERENCES markets(market_id),
    date_created DATE,
    date_delivered DATE,
    status VARCHAR(50)
);

-- Step 6: Create Supply Details Table
CREATE TABLE supply_details (
    supply_detail_id SERIAL PRIMARY KEY,
    supply_id INT REFERENCES supply_metadata(supply_id),
    product_id INT REFERENCES products(product_id),
    quantity INT
);

-- Step 7: Create Sales Table
CREATE TABLE sales (
    sale_id SERIAL PRIMARY KEY,
    market_id INT REFERENCES markets(market_id),
    product_id INT REFERENCES products(product_id),
    sale_date DATE,
    quantity INT
);
