from typing import List

from loguru import logger


async def block_resources_and_sentry(request, types: List[str]):
    is_blocked = False

    if request.resourceType in types:
        is_blocked = True

    if "/sentry/" in request.url:
        is_blocked = True

    if is_blocked:
        await request.abort()
    else:
        await request.continue_()


async def catch_response_and_store(response, result):
    if "/item_list" in response.url:
        logger.debug(response.url)
        data = await response.json()

        for item in data["items"]:
            result.append(item)
        logger.debug(f"🛒 Collected {len(data['items'])} items. Total: {len(result)}")