from src.database.my_connector import db
from src.database.models import Fees
from typing import Dict


def get_all_fees(category_id: int = None, limit: int = None, offset: int = None):
    # Формируем строку для LIMIT и OFFSET
    support_sql_str = ""
    if limit:
        support_sql_str = f" LIMIT {limit} OFFSET {offset}"  # Добавляем пробел перед LIMIT
    # Если передан category_id, добавляем условие WHERE
    if category_id:
        query = f"SELECT * FROM fees WHERE fee_category_id=%s" + support_sql_str
        return db.fetch_all(query, (category_id,))
    else:
        query = f"SELECT * FROM fees" + support_sql_str
        return db.fetch_all(query)


def get_fee_by_id(fee_id: int):
    query = "SELECT * FROM fees WHERE id=%s"
    return db.fetch_one(query, (fee_id,))


def get_fee_by_name(fee_name: str):
    query = "SELECT * FROM fees WHERE name=%s"
    return db.fetch_one(query, (fee_name,))


def create_fee(fee: Fees):
    query = ("INSERT INTO fees (name, description, final_cost, gathered_cost,"
             " created_at, date_finish, fee_category_id, image_url)"
             " VALUES (%s, %s, %s, %s, %s, %s, %s, %s)")
    params = (fee.Name, fee.Desc, fee.FCost, fee.GCost, fee.CreatedAt, fee.DateFinish,
              fee.FeeCategoryID, fee.ImageUrl)
    cursor = db.execute_query(query, params)
    return cursor.lastrowid


def update_fee(fee_id: int, fee: Dict):
    fields_to_update = [f"{key}=%s" for key in fee.keys()]
    params = list(fee.values())
    query = f"UPDATE fees SET {', '.join(fields_to_update)} WHERE id=%s"
    params.append(fee_id)
    db.execute_query(query, tuple(params))


def delete_fee(fee_id: int):
    query = "DELETE FROM fees WHERE id=%s"
    db.execute_query(query, (fee_id,))
