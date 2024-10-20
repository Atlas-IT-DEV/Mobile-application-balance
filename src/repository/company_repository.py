from src.database.my_connector import db
from src.database.models import Companies
from typing import Dict


def get_all_companies():
    query = "SELECT * FROM companies"
    return db.fetch_all(query)


def get_company_by_id(company_id: int):
    query = "SELECT * FROM companies WHERE id=%s"
    return db.fetch_one(query, (company_id,))


def create_company(company: Companies):
    query = "INSERT INTO companies (name, description, contact) VALUES (%s, %s, %s)"
    params = (company.Name, company.Desc, company.Contact)
    cursor = db.execute_query(query, params)
    return cursor.lastrowid


def update_company(company_id: int, company: Dict):
    fields_to_update = [f"{key}=%s" for key in company.keys()]
    params = list(company.values())
    query = f"UPDATE companies SET {', '.join(fields_to_update)} WHERE id=%s"
    params.append(company_id)
    db.execute_query(query, tuple(params))


def delete_company(company_id: int):
    query = "DELETE FROM companies WHERE id=%s"
    db.execute_query(query, (company_id,))
