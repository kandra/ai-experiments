from app.core.database import get_db_connection

def save_invoice_data(parsed_data: dict, file_url: str = None):
    """
    Guarda la data parseada (Vendor, Invoice, Items) en la base de datos.
    """
    conn = get_db_connection()
    cur = conn.cursor()
    saved_invoice_id = None

    try:
        details = parsed_data.get('invoice_details', {})
        items = parsed_data.get('line_items', [])

        # 1. Manejo del VENDOR (Lógica simplificada para el ejemplo)
        # Aquí podrías añadir la lógica de 'get_or_create_vendor' que tenías antes
        # Por ahora asumiremos que insertamos o buscamos por nombre simple
        cur.execute("SELECT id FROM vendors WHERE name = %s", (details.get('vendor_name'),))
        vendor_res = cur.fetchone()
        
        if vendor_res:
            vendor_id = vendor_res[0]
        else:
            print(f"🆕 Creando vendedor: {details.get('vendor_name')}")
            cur.execute(
                "INSERT INTO vendors (name, ruc, contact_email, phone) VALUES (%s, %s, %s, %s) RETURNING id",
                (details.get('vendor_name'), details.get('vendor_ruc'), details.get('vendor_email'), details.get('vendor_phone'))
            )
            vendor_id = cur.fetchone()[0]

        # 2. Guardar INVOICE
        print(f"📄 Guardando factura #{details.get('invoice_number')}...")
        cur.execute(
            """
            INSERT INTO invoices 
            (vendor_id, invoice_number, invoice_date, currency, total_amount, file_url)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id;
            """,
            (
                vendor_id,
                details.get('invoice_number'),
                details.get('date'),
                details.get('currency'),
                details.get('total_amount'),
                file_url
            )
        )
        saved_invoice_id = cur.fetchone()[0]

        # 3. Guardar ITEMS
        print(f"📦 Guardando {len(items)} items...")
        for item in items:
            cur.execute(
                """
                INSERT INTO invoice_items 
                (invoice_id, description, quantity, unit_price, total_price, category)
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (
                    saved_invoice_id,
                    item.get('description'),
                    item.get('quantity'),
                    item.get('unit_price'),
                    item.get('total_price'),
                    item.get('category')
                )
            )

        conn.commit()
        print(f"✅ Éxito! Factura guardada ID: {saved_invoice_id}")
        return saved_invoice_id

    except Exception as e:
        conn.rollback()
        print(f"❌ Error DB: {e}")
        raise e
    finally:
        cur.close()
        conn.close()