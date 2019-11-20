import sqlite3
import json


def open_db():
    conn = sqlite3.connect('test.db')
    print("Opened database successfully")
    return conn

def create_db_table(table_name: str, schema: dict, conn: sqlite3.Connection):
    cursor = conn.cursor()
    schema_str = ', '.join([str(k)+' '+str(v) for k, v in schema.items()])

    cursor.execute("CREATE TABLE IF NOT EXISTS "+table_name+" ("+schema_str+")"
            
            )

def populate_db(list_of_dicts: list, table_name: str, conn: sqlite3.Connection):
    cursor = conn.cursor()
    for dic in list_of_dicts:
        cursor.execute("INSERT INTO "+table_name+" VALUES (?, ?)", 
                [dic['id'], json.dumps(dic, indent=4, sort_keys=True, default=str)])

if __name__ == "__main__":
    d = {'id': '1', 'address': 'Horbaczewskiego 21/...0 Wrocław', 'date': 'datetime.datetime(20..., 4, 0, 0)', 'kw': None, 'price': "Decimal('234750.00')", 'url': 'http://www.licytacj...ls/486059'}
    try:
        with open_db() as con:
            table_name = 'auctions'
            create_db_table(table_name, {'id': 'varchar(16)', 'data': 'json'}, con)
            # populate_db([d], table_name, con)
    except sqlite3.IntegrityError as e:
        print(e.args)


