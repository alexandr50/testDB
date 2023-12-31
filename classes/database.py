import psycopg2


class DBManager:

    def __init__(self, name_bd: str, params: dict):
        self.name_db = name_bd
        self.params = params

    def create_database(self):
        conn = psycopg2.connect(dbname='postgres', **self.params)
        conn.autocommit = True

        with conn.cursor() as cur:
            # cur.execute(f"""DROP DATABASE IF EXISTS {self.name_db}""")
            cur.execute(f"""CREATE DATABASE {self.name_db} IF NOT EXISTS""")

        with psycopg2.connect(dbname=self.name_db, **self.params) as conn:
            with conn.cursor() as cur:
                cur.execute(f"""CREATE TABLE IF NOT EXISTS shelves (
                    shelve_id INT PRIMARY KEY,
                    number VARCHAR(20) UNIQUE NOT NULL);
                """)

                cur.execute(f"""CREATE TABLE IF NOT EXISTS products (
                    product_id INT PRIMARY KEY,
                    title VARCHAR(50),
                    description VARCHAR(255),
                    price INT,
                    count INT,
                    salary INT
                    );
                """)

                cur.execute(f"""CREATE TABLE IF NOT EXISTS shelves_products (
                    id INT PRIMARY KEY,
                    shelve_id INTEGER NOT NULL REFERENCES shelves,
                    product_id   INTEGER NOT NULL REFERENCES products,
                    extra_shelve_id INT NOT NULL REFERENCES shelves UNIQUE,
                    UNIQUE (shelve_id, product_id)
                    );
                """)

                cur.execute(f"""CREATE TABLE IF NOT EXISTS customers (
                    customer_id INT PRIMARY KEY,
                    email VARCHAR(255)
                    );
                """)

                cur.execute(f"""CREATE TABLE IF NOT EXISTS orders (
                    order_id INT PRIMARY KEY,
                    customer_id INT REFERENCES customers(customer_id) NOT NULL
                    );
                """)

                cur.execute(f"""CREATE TABLE IF NOT EXISTS order_items (
                    order_item_id INT PRIMARY KEY,
                    order_id INT REFERENCES orders(order_id) NOT NULL,
                    product_id INT REFERENCES products(product_id) NOT NULL,
                    shelve_id INT REFERENCES shelves(shelve_id) NOT NULL,
                    quantity INT                 
                    );
                """)

    def get_content(self, *args):
        with psycopg2.connect(dbname=self.name_db, **self.params) as conn:
            with conn.cursor() as cur:
                cur.execute(f"""select products.title,
                   order_items.quantity,
                   order_items.order_item_id,
                   orders.order_id,
                   number as shelve_number
                   from products
                inner join order_items
                    on products.product_id = order_items.product_id
                inner join shelves
                    on shelves.shelve_id = order_items.shelve_id
                inner join orders
                    on orders.order_id = order_items.order_id
                    where orders.order_id in {10, 11, 14, 15}
                    order by shelve_number;""")
                rows = cur.fetchall()

                print(rows)
