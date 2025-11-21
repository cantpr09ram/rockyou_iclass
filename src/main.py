import asyncio
import logging
from api.auth_module import Authenticator
from api.http_headers import session_headers
from getrollcall import wait_for_rollcall
from sendRadar import answer_rollcall_Radar
from sendNum import answer_rollcall_number_async

if not logging.getLogger().hasHandlers():
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    )

logger = logging.getLogger(__name__)


async def main():
    logger.info("🔐 Logging in...")
    auth = Authenticator()
    session = auth.perform_auth()

    session.headers.update(session_headers())

    rollcall_id, source = wait_for_rollcall(session)
    logger.info("Returned: rollcall_id=%s, source=%s", rollcall_id, source)

    if source == "number":
        data = await answer_rollcall_number_async(session, rollcall_id)
        logger.info("Number rollcall response: %s", data)

    elif source == "radar":
        radar_response = answer_rollcall_Radar(session, rollcall_id)
        logger.info("Radar rollcall response: %s", radar_response.text)


if __name__ == "__main__":
    asyncio.run(main())
