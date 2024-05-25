from models.user import User
from utils.config import config
from utils.auth import hash_password


async def on_startup():
    print("Starting up...")
    print("Check admin user")
    check_admin_user = await User.get_by_username(config.APP_ADMIN_USERNAME.lower().strip())
    if not check_admin_user:
        print("Admin user not found, try to create")
        admin_user = User(
            username=config.APP_ADMIN_USERNAME.lower().strip(),
            hashed_password=hash_password(config.APP_ADMIN_PASSWORD),
            is_active=True,
            is_superuser=True,
        )
        await User.create(admin_user)
        print("Admin user is created")
    else:
        print("Admin user is already")
    print("Check requirements is OK!")
