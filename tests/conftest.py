import pytest_asyncio
import pytest
import asyncio


@pytest_asyncio.fixture
async def async_client():
    """Фикстура для асинхронного клиента"""
    import aiohttp
    async with aiohttp.ClientSession() as session:
        yield session
