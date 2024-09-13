from src.database.my_connector import db
from src.database.models import Fees


def get_all_fees():
    query = "SELECT * FROM fees"
    return db.fetch_all(query)


def get_fee_by_id(fee_id: int):
    query = "SELECT * FROM fees WHERE id=%s"
    return db.fetch_one(query, (fee_id,))


def create_fee(fee: Fees):
    query = ("INSERT INTO fees (name, description, final_cost, gathered_cost,"
             " created_at, fee_category_id, image_url)"
             " VALUES (%s, %s, %s, %s, %s, %s, %s)")
    params = (fee.Name, fee.Desc, fee.FCost, fee.GCost, fee.CreatedAt,
              fee.FeeCategoryID, fee.ImageUrl)
    cursor = db.execute_query(query, params)
    return cursor.lastrowid


def update_fee(fee_id: int, fee: Fees):
    query = ("UPDATE fees SET name=%s, description=%s, final_cost=%s,"
             " gathered_cost=%s, created_at=%s, fee_category_id=%s,"
             " image_url=%s WHERE id=%s")
    params = (fee.Name, fee.Desc, fee.FCost, fee.GCost, fee.CreatedAt,
              fee.FeeCategoryID, fee.ImageUrl, fee_id)
    db.execute_query(query, params)


def delete_fee(fee_id: int):
    query = "DELETE FROM fees WHERE id=%s"
    db.execute_query(query, (fee_id,))
