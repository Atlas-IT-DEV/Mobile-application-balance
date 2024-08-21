from src.database.my_connector import Database
from src.database.models import Companies
db = Database()


async def get_all_companies():
    query = "SELECT * FROM companies"
    return await db.fetch_all(query)


async def get_company_by_id(company_id: int):
    query = "SELECT * FROM companies WHERE id=%s"
    return await db.fetch_one(query, (company_id,))


async def create_company(company: Companies):
    query = "INSERT INTO companies (name, description) VALUES (%s, %s)"
    params = (company.Name, company.Desc)
    cursor = await db.execute_query(query, params)
    return cursor.lastrowid


async def update_company(company_id: int, company: Companies):
    query = "UPDATE companies SET name=%s, description=%s WHERE id=%s"
    params = (company.Name, company.Desc, company_id)
    await db.execute_query(query, params)


async def delete_company(company_id: int):
    query = "DELETE FROM companies WHERE id=%s"
    await db.execute_query(query, (company_id,))
