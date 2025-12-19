-- 1. Create Vendors Table
CREATE TABLE IF NOT EXISTS vendors (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    ruc VARCHAR(50),
    contact_email VARCHAR(255),
    phone VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Create Invoices Table
CREATE TABLE IF NOT EXISTS invoices (
    id SERIAL PRIMARY KEY,
    vendor_id INTEGER REFERENCES vendors(id) ON DELETE SET NULL,
    invoice_number VARCHAR(100),
    invoice_date DATE,
    currency VARCHAR(10),
    total_amount DECIMAL(10, 2),
    file_url TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3. Create Invoice Items Table
CREATE TABLE IF NOT EXISTS invoice_items (
    id SERIAL PRIMARY KEY,
    invoice_id INTEGER REFERENCES invoices(id) ON DELETE CASCADE,
    description TEXT,
    quantity DECIMAL(10, 2),
    unit_price DECIMAL(10, 2),
    total_price DECIMAL(10, 2),
    category VARCHAR(100)
);

-- Optional: Create indexes for faster searching
CREATE INDEX IF NOT EXISTS idx_invoice_vendor ON invoices(vendor_id);
CREATE INDEX IF NOT EXISTS idx_item_invoice ON invoice_items(invoice_id);