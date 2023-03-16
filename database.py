from typing import List, Any
import compare
import mysql.connector
from getpass import getpass

import numpy

dataBase = mysql.connector.connect(
    host="localhost",
    user=input("Enter username: "),
    passwd=getpass("Enter password"),
    database='signs_compare'
)
cursor = dataBase.cursor()


def add_user(id: str, *signs):
    signs_as_str: list[bytes] = [s.dumps() for s in signs if s is numpy.ndarray][:5]
    columns = ''
    values = ''
    for i in range(signs_as_str):
        columns += f'SIGN{i + 1}, '
        values += f'"{signs_as_str[i]}", '
    columns = columns[:-2]
    values = values[:-2]

    insert_user = f"""
    INSERT INTO SIGNS (ID, {columns})
    VALUES
        ("{id}",{values})"""
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
    vects = [numpy.load(v) for v in l if l is not None]
    return compare.compare_with_lst(vect, vects)
