# -*- coding: utf-8 -*-
import os
from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy import Column, Integer, String, Float, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database setup
DATABASE_URL = "sqlite:///./pharmacy.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
Base = declarative_base()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    quantity = Column(Integer, nullable=False)


def init_db():
    Base.metadata.create_all(bind=engine)


app = FastAPI()


@app.on_event("startup")
def on_startup():
    init_db()


def get_html(products, total_value):
    rows = ""
    for p in products:
        rows += f"""
        <tr>
            <td>{p.id}</td>
            <td>{p.name}</td>
            <td>{p.price:.2f}</td>
            <td>{p.quantity}</td>
            <td>{p.price * p.quantity:.2f}</td>
        </tr>
        """
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Farmacia - Productos</title>
        <style>
            body {{font-family: Arial, sans-serif; margin:0; padding:20px; background:#f5f5f5;}}
            h1 {{color:#2c3e50;}}
            form {{background:#fff; padding:20px; border-radius:5px; margin-bottom:20px; box-shadow:0 2px 4px rgba(0,0,0,0.1);}}
            input[type=text], input[type=number] {{
                width:100%; padding:8px; margin:5px 0 10px 0; border:1px solid #ccc; border-radius:4px;
            }}
            input[type=submit] {{
                background:#27ae60; color:#fff; border:none; padding:10px 20px;
                border-radius:4px; cursor:pointer;
            }}
            input[type=submit]:hover {{background:#219150;}}
            table {{width:100%; border-collapse:collapse; background:#fff;}}
            th, td {{padding:12px; border:1px solid #ddd; text-align:left;}}
            th {{background:#2c3e50; color:#fff;}}
            @media (max-width:600px) {{
                table, thead, tbody, th, td, tr {{display:block;}}
                th {{position:absolute; top:-9999px; left:-9999px;}}
                td {{border:none; position:relative; padding-left:50%;}}
                td:before {{
                    position:absolute; left:6px; width:45%; padding-right:10px;
                    white-space:nowrap; font-weight:bold;
                }}
                td:nth-of-type(1):before {{content:"ID";}}
                td:nth-of-type(2):before {{content:"Nombre";}}
                td:nth-of-type(3):before {{content:"Precio";}}
                td:nth-of-type(4):before {{content:"Cantidad";}}
                td:nth-of-type(5):before {{content:"Valor Total";}}
            }}
        </style>
    </head>
    <body>
        <h1>Farmacia - Gestion de Productos</h1>
        <form action="/add-product" method="post">
            <label for="name">Nombre del producto:</label>
            <input type="text" id="name" name="name" required>

            <label for="price">Precio (USD):</label>
            <input type="number" step="0.01" id="price" name="price" required>

            <label for="quantity">Cantidad:</label>
            <input type="number" id="quantity" name="quantity" required>

            <input type="submit" value="Agregar producto">
        </form>

        <h2>Listado de productos</h2>
        <table>
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Nombre</th>
                    <th>Precio (USD)</th>
                    <th>Cantidad</th>
                    <th>Valor Total (USD)</th>
                </tr>
            </thead>
            <tbody>
                {rows}
            </tbody>
        </table>

        <h3>Total inventario: USD {total_value:.2f}</h3>
    </body>
    </html>
    """
    return html_content


@app.get("/", response_class=HTMLResponse)
def read_root():
    db = SessionLocal()
    products = db.query(Product).all()
    total_value = sum(p.price * p.quantity for p in products)
    db.close()
    return HTMLResponse(content=get_html(products, total_value))


@app.post("/add-product")
def add_product(
    name: str = Form(...),
    price: float = Form(...),
    quantity: int = Form(...)
):
    db = SessionLocal()
    new_product = Product(name=name, price=price, quantity=quantity)
    db.add(new_product)
    db.commit()
    db.close()
    return RedirectResponse(url="/", status_code=303)


if __name__ == "__main__":
    import os, uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))