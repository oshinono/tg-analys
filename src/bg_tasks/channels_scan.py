from bg_tasks.main import app
from channels.service import ChannelService
from providers import container
from telethon import TelegramClient
from channels.models import Post
import asyncio

@app.task
def scan_posts_via_telethon():
    # Используем синхронный запуск асинхронного кода
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    try:
        return loop.run_until_complete(_async_scan_posts())
    finally:
        loop.close()

async def _async_scan_posts():
    channels = await ChannelService.get_all()
    telethon = await container.get(TelegramClient)

    for db_channel in channels:
        channel = await telethon.get_entity(db_channel.id)
        posts = []
        
        async for post in telethon.iter_messages(channel):
            if channel.username:
                post_url = f"https://t.me/{channel.username[1:]}/{post.id}"
            else:
                clean_channel_id = str(channel.id)[4:]  # Убираем "-100" для приватных каналов
                post_url = f"https://t.me/c/{clean_channel_id}/{post.id}"

            total_reactions = 0
            # reactions_details = [] если нужна будет инфа по всем реакциям
            if post.reactions and post.reactions.results:
                for reaction in post.reactions.results:
                    reaction_type = reaction.reaction.emoticon if hasattr(reaction.reaction, 'emoticon') else str(reaction.reaction)
                    reaction_count = reaction.count
                    total_reactions += reaction_count
                    # reactions_details.append(f"{reaction_type}: {reaction_count}")
            
            comment_count = 0
            if post.replies:
                comment_count = post.replies.replies or 0

            posts.append(Post(id=post.id,
                              url=post_url,
                              views_count=post.views,
                              reactions_count=total_reactions,
                              comments_count=comment_count,
                              reposts_count=post.forwards,
                              channel_id=channel.id,
                              date=post.date))
            
        # за каждый день выбрать по одному лучшему посту исходя из статистики поста
        # но и думаю лучше алгоритм улучшить, декомпозировать хз

