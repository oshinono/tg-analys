from fastapi import APIRouter, Depends, HTTPException
from telethon import TelegramClient
from client import get_telegram_client
from starlette import status


router = APIRouter(prefix="/users")
