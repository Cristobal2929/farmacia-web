---
title: Farmacia Web
emoji: 🏥
colorFrom: blue
colorTo: green
sdk: gradio
---

# Farmacia Web

A simple web interface for managing pharmacy products.  
Features:

- View all products in a table
- Add new products
- Update existing products
- Delete products
- Search products by name
- Automatic calculation of total inventory value

## How to run

The app uses **Gradio** and **SQLAlchemy** with a local SQLite database (`pharmacy.db`).  
When the Space starts, the database is created automatically if it does not exist.