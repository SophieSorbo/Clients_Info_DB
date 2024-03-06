import psycopg2

conn = psycopg2.connect(database="data_bases_sophie", user="postgres", password="(LilBoPeep2017)")

def delete_table_info(conn):
    with conn.cursor() as cur:
        cur.execute("DROP TABLE client_phones;")
        cur.execute("DROP TABLE clients_info;")
        conn.commit()

def create_table_info(conn):
    with conn.cursor() as cur:
        cur.execute("""
        CREATE TABLE IF NOT EXISTS clients_info(
            id SERIAL PRIMARY KEY,
            name VARCHAR(40),
            last_name VARCHAR(40),
            email VARCHAR(40) UNIQUE
        );
        """)
        cur.execute("""
        CREATE TABLE IF NOT EXISTS client_phones(
            id SERIAL PRIMARY KEY,
            client_id INTEGER NOT NULL REFERENCES clients_info(id),
            phone VARCHAR(40) UNIQUE
        );
        """)
        conn.commit()


def add_client_info(conn, name, last_name, email, phone=None):
    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO clients_info(name, last_name, email) VALUES(%s, %s, %s);",
            (name, last_name, email)
        )
        conn.commit()
        if phone is not None:
            cur.execute(
                "SELECT id FROM clients_info WHERE name=%s AND last_name=%s AND email=%s;",
                (name, last_name, email)
            )
            id_client = cur.fetchone()[0]
            cur.execute(
                "INSERT INTO client_phones(client_id, phone) VALUES(%s, %s);",
                (id_client, phone)
            )
            conn.commit()



def add_phones_number(conn, client_id, phone):
    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO client_phones(client_id, phone) VALUES(%s, %s);",
            (client_id, phone)
        )
        conn.commit()


def update_info_client(conn, client_id, name=None, last_name=None, email=None, phone=None):
    with conn.cursor() as cur:
        cur.execute(
            "SELECT * FROM clients_info WHERE id=%s",
            (client_id, )
        )
        string = cur.fetchone()
        if name is None: name = string[1]
        if last_name is None: last_name = string[2]
        if email is None: email = string[3]
        cur.execute('''
        UPDATE clients_info SET name=%s, last_name=%s, email=%s WHERE id=%s
        RETURNING id, name, last_name, email;
        ''', (name, last_name, email, client_id))
        cur.fetchall()


def delete_phones_number(conn, client_id, phone):
    with conn.cursor() as cur:
        cur.execute("""
        DELETE FROM client_phones WHERE client_id=%s AND phone=%s;
        """, (client_id, phone))
        conn.commit()


def delete_info_client(conn, id):
    with conn.cursor() as cur:
        cur.execute("""
        DELETE FROM client_phones WHERE client_id=%s;
        """, (id,))
        cur.execute("""
        DELETE FROM clients_info WHERE id=%s;
        """, (id,))
        conn.commit()


def get_info_client(conn, object, data):
    with conn.cursor() as cur:
        cur.execute("""
        SELECT * FROM clients_info WHERE %s=%s;
        """, (object, data))
        return cur.fetchall()


def get_phones_number(conn, id):
    with conn.cursor() as cur:
        cur.execute("""
        SELECT * FROM client_phones WHERE client_id=%s;
        """, (id,))
        return cur.fetchall()


def get_all_clients(conn):
    with conn.cursor() as cur:
        cur.execute("""
        SELECT * FROM clients_info;
        """)
        return cur.fetchall()


def get_all_phones(conn):
    with conn.cursor() as cur:
        cur.execute("""
        SELECT * FROM client_phones;
        """)
        return cur.fetchall()


with conn as conn:
    delete_table_info(conn)
    create_table_info(conn)
    add_client_info(conn, "Sofi", "Pup", "sophie@ya.ru", "+71112223330")
    add_client_info(conn, "Bob", "Marley", "bobmarley@ya.ru", "+71234567890")
    add_phones_number(conn, 1, "+71122334455")
    update_info_client(conn, 1, last_name="Kek")
    # delete_phones_number(conn, 1, "+71122334455")
    # delete_info_client(conn, 1)
    print(get_info_client(conn, "name", "Sofi"))
    print(get_phones_number(conn, 1))
    print(get_all_clients(conn))
    print(get_all_phones(conn))
conn.close()
