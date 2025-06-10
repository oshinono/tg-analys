from gspread_asyncio import AsyncioGspreadClientManager

"""
Пока будем считать, что будет один лист с каналами и отдельный лист с юзерами.
"""


class BaseGTParser:
    """
    Абстрактный класс парсера Google Tables -> модельки SQLAlchemy.
    """


    def __init__(self, table_url: str, agcm: AsyncioGspreadClientManager):
        self._table_url = table_url
        self._agcm = agcm

    async def _parse_all_rows(self, worksheets: list[int] | None = None, all_worksheets: bool = False) -> list[list[list[str]]]:
        agc = await self._agcm.authorize()
        spreadsheet = await agc.open_by_url(self._table_url)

        data = []

        if all_worksheets:
            worksheets = list(range(len(spreadsheet.worksheets())))

        if not worksheets:
            raise ValueError("Не переданы номера листов. Проверьте, может вы забыли указать all_worksheets=True")

        for worksheet_number in worksheets:
            worksheet = await spreadsheet.get_worksheet(worksheet_number)
            data.append(await worksheet.get_all_values())

        return data
    

        
