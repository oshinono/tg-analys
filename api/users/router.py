from fastapi import APIRouter, Depends, HTTPException
from telethon import TelegramClient
from client import get_telegram_client
from starlette import status


router = APIRouter(prefix="/users")

@router.get("")
async def get_user(username: str, id: int, client: TelegramClient = Depends(get_telegram_client)):
    if id:
        identifier = id
    elif username:
        identifier = username
    else:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Юзер не найден")
    
    user = await client.get_entity(identifier)

    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Юзер не найден")

    return {'ID': user.id,
            'first_name': user.first_name,
            'username': user.username,
            'phone_number': user.phone
            }