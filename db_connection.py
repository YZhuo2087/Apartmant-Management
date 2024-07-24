import mysql.connector


def get_all_data():
    db_conn = mysql.connector.connect(user='root', password='6789@jkl',
                                      host='127.0.0.1',
                                      port=3306,
                                      database='apartment_access_control',
                                      charset='utf8mb4',
                                      collation='utf8mb4_unicode_ci')

    res = []

    c = db_conn.cursor()
    c.execute("SHOW TABLES")
    table_data = c.fetchall()

    for tuple in table_data:
        for elem in tuple:
            res.append(str(elem))

    db_conn.close()
    return res


def get_table_data(table_name):
    db_conn = mysql.connector.connect(user='root', password='6789@jkl',
                                      host='127.0.0.1',
                                      port=3306,
                                      database='apartment_access_control',
                                      charset='utf8mb4',
                                      collation='utf8mb4_unicode_ci')

    res = []
    column_names = []

    c = db_conn.cursor()
    c.execute(f"DESCRIBE {table_name}")
    column_data = c.fetchall()
    column_names = [col[0] for col in column_data]

    c.execute(f"SELECT * FROM {table_name}")
    table_data = c.fetchall()

    for tuple in table_data:
        res.append(tuple)

    db_conn.close()
    return column_names, res


def add_table_data(table_name, data):
    db_conn = mysql.connector.connect(user='root', password='6789@jkl',
                                      host='127.0.0.1',
                                      port=3306,
                                      database='apartment_access_control',
                                      charset='utf8mb4',
                                      collation='utf8mb4_unicode_ci')
    placeholders = ', '.join(['%s'] * len(data))
    columns = ', '.join(data.keys())
    sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"

    c = db_conn.cursor()
    c.execute(sql, list(data.values()))
    db_conn.commit()
    db_conn.close()


def update_table_data(table_name, data, where_clause):
    db_conn = mysql.connector.connect(user='root', password='6789@jkl',
                                      host='127.0.0.1',
                                      port=3306,
                                      database='apartment_access_control',
                                      charset='utf8mb4',
                                      collation='utf8mb4_unicode_ci')
    placeholders = ', '.join([f"{key} = %s" for key in data.keys()])
    sql = f"UPDATE {table_name} SET {placeholders} WHERE {where_clause}"

    c = db_conn.cursor()
    c.execute(sql, list(data.values()))
    db_conn.commit()
    db_conn.close()


def delete_table_data(table_name, where_clause):
    db_conn = mysql.connector.connect(user='root', password='6789@jkl',
                                      host='127.0.0.1',
                                      port=3306,
                                      database='apartment_access_control',
                                      charset='utf8mb4',
                                      collation='utf8mb4_unicode_ci')
    sql = f"DELETE FROM {table_name} WHERE {where_clause}"

    c = db_conn.cursor()
    c.execute(sql)
    db_conn.commit()
    db_conn.close()
