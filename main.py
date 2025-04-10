from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models import Provider, Game
from schemas import ProviderCreate, ProviderRead, GameCreate, GameRead
from database import get_db
import uvicorn

app = FastAPI(
    title="API for managing providers and games. CRUD",
    description="This API allows you to manage providers and games: create, read, update, delete.",
)

# ПРОВАЙДЕРЫ


@app.post(
    "/providers/",
    response_model=ProviderRead,
    summary="Создать провайдера",
    description="Добавляет нового провайдера в базу данных.",
    tags=["Providers"],
)
async def create_provider(provider: ProviderCreate, db: AsyncSession = Depends(get_db)):
    db_provider = Provider(**provider.model_dump())
    db.add(db_provider)
    await db.commit()
    await db.refresh(db_provider)
    return db_provider


@app.get(
    "/providers/{provider_id}",
    response_model=ProviderRead,
    summary="Получить провайдера",
    description="Возвращает данные о конкретном провайдере по его ID.",
    tags=["Providers"],
)
async def read_provider(provider_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Provider).filter(Provider.id == provider_id))
    provider = result.scalars().first()
    if not provider:
        raise HTTPException(status_code=404, detail="Провайдер не найден")
    return provider


@app.put(
    "/providers/{provider_id}",
    response_model=ProviderRead,
    summary="Обновить провайдера",
    description="Обновляет данные о существующем провайдере по его ID.",
    tags=["Providers"],
)
async def update_provider(
    provider_id: int,
    provider_update: ProviderCreate,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Provider).filter(Provider.id == provider_id))
    provider = result.scalars().first()
    if not provider:
        raise HTTPException(status_code=404, detail="Провайдер не найден")
    provider.name = provider_update.name
    provider.email = provider_update.email
    await db.commit()
    await db.refresh(provider)
    return provider


@app.delete(
    "/providers/{provider_id}",
    summary="Удалить провайдера",
    description="Удаляет провайдера из базы данных по его ID.",
    tags=["Providers"],
)
async def delete_provider(provider_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Provider).filter(Provider.id == provider_id))
    provider = result.scalars().first()
    if not provider:
        raise HTTPException(status_code=404, detail="Провайдер не найден")
    await db.delete(provider)
    await db.commit()
    return {"message": "Провайдер удален"}


# ИГРЫ


@app.post(
    "/games/",
    response_model=GameRead,
    summary="Создать игру",
    description="Добавляет новую игру в базу данных.",
    tags=["Games"],
)
async def create_game(game: GameCreate, db: AsyncSession = Depends(get_db)):
    db_game = Game(**game.model_dump())
    db.add(db_game)
    await db.commit()
    await db.refresh(db_game)
    return db_game


@app.get(
    "/games/{game_id}",
    response_model=GameRead,
    summary="Получить игру",
    description="Возвращает данные об игре по её ID.",
    tags=["Games"],
)
async def read_game(game_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Game).filter(Game.id == game_id))
    game = result.scalars().first()
    if not game:
        raise HTTPException(status_code=404, detail="Игра не найдена")
    return game


@app.put(
    "/games/{game_id}",
    response_model=GameRead,
    summary="Обновить игру",
    description="Обновляет данные об игре по её ID.",
    tags=["Games"],
)
async def update_game(
    game_id: int, game_update: GameCreate, db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Game).filter(Game.id == game_id))
    game = result.scalars().first()
    if not game:
        raise HTTPException(status_code=404, detail="Игра не найдена")
    game.title = game_update.title
    game.price = game_update.price
    game.provider_id = game_update.provider_id
    await db.commit()
    await db.refresh(game)
    return game


@app.delete(
    "/games/{game_id}",
    summary="Удалить игру",
    description="Удаляет игру из базы данных по её ID.",
    tags=["Games"],
)
async def delete_game(game_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Game).filter(Game.id == game_id))
    game = result.scalars().first()
    if not game:
        raise HTTPException(status_code=404, detail="Игра не найдена")
    await db.delete(game)
    await db.commit()
    return {"message": "Игра удалена"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
