from datetime import datetime
from typing import Optional, Tuple


from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.charity_project import CharityProject
from app.models.donation import Donation


def investment_logic(
    project: CharityProject,
    donation: Donation
) -> Tuple[Optional[CharityProject], Optional[Donation]]:
    """Бизнес-логика инвестирования пожертвований в проекты."""
    balance_project = project.full_amount - project.invested_amount
    balance_donation = donation.full_amount - donation.invested_amount

    if balance_project > balance_donation:
        project.invested_amount += balance_donation
        donation.invested_amount += balance_donation
        donation.fully_invested = True
        donation.close_date = datetime.now()

    elif balance_project == balance_donation:
        project.invested_amount += balance_donation
        donation.invested_amount += balance_donation
        project.fully_invested = True
        donation.fully_invested = True
        project.close_date = datetime.now()
        donation.close_date = datetime.now()

    else:
        project.invested_amount += balance_project
        donation.invested_amount += balance_project
        project.fully_invested = True
        project.close_date = datetime.now()

    return project, donation


async def check_not_invested(
    session: AsyncSession,
) -> Tuple[Optional[CharityProject], Optional[Donation]]:
    """
    Получение из БД первых по очереди незакрытых проектов и пожертвований.
    """
    project_result = await session.execute(
        select(CharityProject).where(
            CharityProject.fully_invested == 0
        ).order_by(CharityProject.create_date)
    )
    project = project_result.scalars().first()

    donation_result = await session.execute(
        select(Donation).where(
            Donation.fully_invested == 0
        ).order_by(Donation.create_date)
    )
    donation = donation_result.scalars().first()

    return project, donation


async def process_investment(session: AsyncSession, obj) -> Optional[object]:
    """Процесс инвестирования."""
    project, donation = await check_not_invested(session)

    if project and donation:
        updated_project, updated_donation = investment_logic(project, donation)
        session.add(updated_project)
        session.add(updated_donation)
        await session.commit()
        await session.refresh(updated_project)
        await session.refresh(updated_donation)
        return await process_investment(session, obj)

    await session.commit()
    await session.refresh(obj)
    return obj