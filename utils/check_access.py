from assets.bot_config import admin_ids

def is_admin(user_id: int):
    return user_id in admin_ids
