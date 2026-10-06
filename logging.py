import logging
import time

from fastapi import Request


logger = logging.getLogger(
    "secure_backend"
)


async def logging_middleware(
    request: Request,
    call_next
):
    start_time = time.time()

    response = await call_next(request)

    process_time = (
        time.time() - start_time
    )

    logger.info(
        "%s %s - Status: %s - Time: %.4fs",
        request.method,
        request.url.path,
        response.status_code,
        process_time
    )

    return response