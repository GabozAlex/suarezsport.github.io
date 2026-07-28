-- Pegar esto en: Supabase Dashboard → SQL Editor → New query

CREATE TABLE IF NOT EXISTS products (
  id SERIAL PRIMARY KEY,
  name VARCHAR(200) NOT NULL,
  description TEXT DEFAULT '',
  category VARCHAR(50) NOT NULL,
  price FLOAT NOT NULL,
  images JSONB DEFAULT '[]',
  sizes JSONB DEFAULT '[]',
  colors JSONB DEFAULT '[]',
  active BOOLEAN DEFAULT TRUE,
  views INTEGER DEFAULT 0,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS orders (
  id SERIAL PRIMARY KEY,
  customer_name VARCHAR(200) NOT NULL,
  phone VARCHAR(50) NOT NULL,
  address TEXT NOT NULL,
  items JSONB NOT NULL,
  total FLOAT NOT NULL,
  status VARCHAR(20) DEFAULT 'pendiente',
  notes TEXT DEFAULT '',
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS testimonials (
  id SERIAL PRIMARY KEY,
  name VARCHAR(200) NOT NULL,
  product VARCHAR(200) DEFAULT '',
  opinion TEXT NOT NULL,
  rating INTEGER DEFAULT 5,
  active BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS contact_messages (
  id SERIAL PRIMARY KEY,
  name VARCHAR(200) NOT NULL,
  email VARCHAR(200) NOT NULL,
  message TEXT NOT NULL,
  read BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS users (
  id SERIAL PRIMARY KEY,
  username VARCHAR(100) UNIQUE NOT NULL,
  hashed_password VARCHAR(200) NOT NULL,
  is_admin BOOLEAN DEFAULT TRUE
);

-- Crear índices
CREATE INDEX IF NOT EXISTS idx_products_category ON products(category);
CREATE INDEX IF NOT EXISTS idx_products_active ON products(active);
CREATE INDEX IF NOT EXISTS idx_testimonials_active ON testimonials(active);
CREATE INDEX IF NOT EXISTS idx_orders_created ON orders(created_at DESC);
