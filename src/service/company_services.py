from src.repository import company_repository
from src.database.models import Companies


async def get_all_companies():
    companies = await company_repository.get_all_companies()
    return [Companies(**company) for company in companies]


async def get_company_by_id(company_id: int):
    company = await company_repository.get_company_by_id(company_id)
    return Companies(**company) if company else None


async def create_company(company: Companies):
    company_id = await company_repository.create_company(company)
    return await get_company_by_id(company_id)


async def update_company(company_id: int, company: Companies):
    await company_repository.update_company(company_id, company)
    return {"message": "Company updated successfully"}


async def delete_company(company_id: int):
    await company_repository.delete_company(company_id)
    return {"message": "Company deleted successfully"}
