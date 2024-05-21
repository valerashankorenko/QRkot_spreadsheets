from datetime import datetime

from aiogoogle import Aiogoogle

from app.core.config import settings

FORMAT = "%Y/%m/%d %H:%M:%S"
SPREADSHEET_BODY = {
    'properties': {'title': '',
                   'locale': 'ru_RU'},
    'sheets': [{'properties': {'sheetType': 'GRID',
                               'sheetId': 0,
                               'title': 'Лист1',
                               'gridProperties': {'rowCount': 100,
                                                  'columnCount': 11}}}]
}
PERMISSIONS_BODY = {
    'type': 'user',
    'role': 'writer',
    'emailAddress': settings.email
}
TABLE_HEADERS = [
    ['Отчёт от', None],
    ['Топ проектов по скорости закрытия'],
    ['Название проекта', 'Время сбора', 'Описание']
]
UPDATE_BODY_TEMPLATE = {
    'majorDimension': 'ROWS',
    'values': []
}


async def spreadsheets_create(wrapper_services: Aiogoogle) -> str:
    """
    Создание Google таблицы.
    """
    now_date_time = datetime.now().strftime(FORMAT)
    service = await wrapper_services.discover('sheets', 'v4')
    spreadsheet_body = SPREADSHEET_BODY.copy()
    spreadsheet_body['properties']['title'] = f'Отчёт на {now_date_time}'

    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=spreadsheet_body)
    )
    spreadsheet_id = response['spreadsheetId']
    return spreadsheet_id


async def set_user_permissions(
        spreadsheet_id: str,
        wrapper_services: Aiogoogle
) -> None:
    """
    Права доступа к Google таблице.
    """
    service = await wrapper_services.discover('drive', 'v3')
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheet_id,
            json=PERMISSIONS_BODY,
            fields="id"
        ))


async def spreadsheets_update_value(
    spreadsheet_id: str,
    charity_project: list,
    wrapper_services: Aiogoogle
) -> None:
    """
    Обновление Google таблицы.
    """
    now_date_time = datetime.now().strftime(FORMAT)
    service = await wrapper_services.discover('sheets', 'v4')

    table_values = TABLE_HEADERS.copy()
    table_values[0][1] = now_date_time

    for project in charity_project:
        new_row = [project.name,
                   str(project.close_date - project.create_date),
                   project.description]
        table_values.append(new_row)

    update_body = UPDATE_BODY_TEMPLATE.copy()
    update_body['values'] = table_values

    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheet_id,
            range='A1:E30',
            valueInputOption='USER_ENTERED',
            json=update_body
        )
    )
