import compare
import mysql.connector
from getpass import getpass
import pickle
import numpy

dataBase = mysql.connector.connect(
    host="localhost",
    user=input("Enter username: "),
    passwd=getpass("Enter password"),
    database='signs_compare'
)
cursor = dataBase.cursor()


def add_user(id: str, *signs):
    signs_as_str: list[bytes] = [numpy.array(s).dumps().hex() for s in signs][:5]
    columns = ''
    values = ''
    for i in range(len(signs_as_str)):
        columns += f'SIGN{i + 1}, '
        values += f'"{signs_as_str[i]}", '
    columns = columns[:-2]
    values = values[:-2].replace("'", '"')

    insert_user = f"""
    INSERT INTO SIGNS (ID, {columns})
    VALUES ("{id}",{values})"""
    cursor.execute(insert_user)
    dataBase.commit()


def check_to_user(id: str, vect):
    select_by_id = f"""
    SELECT SIGN1,SIGN2,SIGN3,SIGN4,SIGN5
    FROM SIGNS
    WHERE ID="{id}";
    """
    cursor.execute(select_by_id)
    l = cursor.fetchall()[0]
    vects = [pickle.loads(bytes.fromhex(str(v)[2:-1])) for v in l if l is not None]
    return compare.compare_with_lst(vect, vects)
