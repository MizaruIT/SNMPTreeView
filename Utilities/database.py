from sqlite3 import *
import os
import json
import argparse
import ast

def init(name):
    conn = connect(name)
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS mibs(oid TEXT PRIMARY KEY NOT NULL, filename TEXT NOT NULL, name TEXT NOT NULL, description TEXT NULL, maxaccess TEXT NULL, indices TEXT NULL)")
    conn.commit()
    c.close()
    conn.close()

def retrieve_MIBS_Info(directory, db_file):
    conn = create_connection(db_file)
    c = conn.cursor()
    number_file = 0
    for filename in os.listdir(directory):
        with open(directory+filename, 'r') as f:
            try:
                data = json.load(f)
            except:
                print(f'{filename} is not a valid JSON file.')
                pass
        number_file += 1
        for name, list_values in data.items():
            if list_values.get('oid'):
                oid, name, description, maxaccess, indices = list_values.get('oid'), list_values.get('name'), list_values.get('description'), list_values.get('maxaccess'), list_values.get('indices')
                if indices is not None:
                    indices_list = ast.literal_eval(str(indices))
                    indices = ''
                    for i in indices_list:
                        indices += f'-Module: {i["module"]}\nObject: {i["object"]}\nImplied: {i["implied"]}\n'
                c.execute("INSERT or IGNORE INTO mibs(oid, filename, name, description, maxaccess, indices) VALUES (?, ?, ?, ?, ?, ?)", (oid, filename, name, description, maxaccess, indices))
    conn.commit()
    c.close()
    conn.close()
    print(f'Number of files parsed = {number_file}')

def create_connection(db_file):
    conn = None
    conn = connect(db_file)
    return conn

def select_all(conn):
    cur = conn.cursor()
    cur.execute("SELECT oid, filename, name, description, maxaccess, indices FROM mibs")
    rows = cur.fetchall()
    for row in rows:
        print(row)

def select_1OID(conn, oid):
    cur = conn.cursor()
    cur.execute("SELECT oid, filename, name, description, maxaccess, indices FROM mibs WHERE oid=?", (oid,))
    rows = cur.fetchall()
    for row in rows:
        print(row)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Parser of MIBs files into JSON files')
    parser.add_argument('-p', '--path', type=str, help='Path to your directory where you have your MIBs files in a JSON format (ex: /home/Downloads/json)', required=True)
    # parser.add_argument('-d', '--database', type=str, help='The name of the database that you will create (ex: mibs_infos.db)', required=True)
    args = parser.parse_args()
    # init(args.database)
    init("snmp_mibs.db")
    retrieve_MIBS_Info(args.path, args.database)
    conn = create_connection(args.database)
    #with conn:
        #print("1. Query mib with an OID:")
        #select_1OID(conn, '1.3.6.1.4.1.43.45.1.2.23.1.17.2')
        #print("2. Query all OIDs")
        #select_all(conn)
