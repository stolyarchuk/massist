from db.redis import RedisAsyncPool
from massist.logger import get_logger
from massist.models import get_gemini_pri_model
from massist.team import get_mitigator_team
from massist.team_lead import TeamLead, create_teamlead

logger = get_logger(__name__)


async def get_cached_teamlead(
    session_id: str, pool: RedisAsyncPool, prefix: str = "teamlead"
) -> TeamLead | None:
    """
    Retrieves a TeamLead profile from cache if it exists.

    Args:
        session_id: The unique session identifier
        rdb: Redis connection pool
        prefix: Cache key prefix

    Returns:
        The TeamLead object if found in cache, None otherwise
    """
    teamlead_cache = await pool.get_model(f"{prefix}:{session_id}", TeamLead)

    if not teamlead_cache:
        return None

    teamlead = TeamLead.model_validate(teamlead_cache)

    teamlead.team = get_mitigator_team(
        user_id=teamlead.user_id,
        session_id=teamlead.session_id,
        model=get_gemini_pri_model(),
    )

    return teamlead


async def cache_teamlead(
    teamlead: TeamLead, pool: RedisAsyncPool, prefix: str = "teamlead"
) -> bool:
    """Cache the TeamLead object in Redis."""
    try:
        # serialized = teamlead.model_dump_json()
        logger.debug("serializing teamlead: %s", teamlead.session_id)
        return await pool.set_model(
            f"{prefix}:{teamlead.session_id}", teamlead, ex=7200
        )
    except Exception as e:
        logger.error(f"Caching failed: {e}")

        # Fall back to caching only essential data
        essential_data = {
            "user_id": teamlead.user_id,
            "session_id": teamlead.session_id,
            "storage_id": teamlead.storage_id,
            "memory_id": teamlead.memory_id,
        }
        return await pool.set_model(
            f"teamlead:{teamlead.session_id}", essential_data, ex=7200
        )


async def get_team_lead(
    user_id: str, session_id: str, pool: RedisAsyncPool
) -> TeamLead:
    teamlead = await get_cached_teamlead(session_id=session_id, pool=pool)

    if teamlead is None:
        teamlead = await create_teamlead(user_id=user_id, session_id=session_id)

        teamlead_cached = await cache_teamlead(teamlead, pool=pool)

        logger.info(
            "TeamLead created: %s. Cached: %s", teamlead.session_id, teamlead_cached
        )
    else:
        logger.info("TeamLead fetched from cache: %s", teamlead.session_id)

    return teamlead
