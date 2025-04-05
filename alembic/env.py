from sqlalchemy.ext.asyncio import create_async_engine
from alembic import context
from models import Base
from database import DATABASE_URL

target_metadata = Base.metadata

def run_migrations_online():
    connectable = create_async_engine(DATABASE_URL)

    async def do_run_migrations():
        async with connectable.connect() as connection:
            await connection.run_sync(context.run_migrations)

    import asyncio
    asyncio.run(do_run_migrations())
