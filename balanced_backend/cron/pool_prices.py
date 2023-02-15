from typing import TYPE_CHECKING
from sqlmodel import select
from typing import Optional
from loguru import logger

from balanced_backend.config import settings
from balanced_backend.tables.pools import Pool
from balanced_backend.utils.rpc import (
    get_pool_stats,
    get_pool_price,
    ReachableNotValidException
)
from balanced_backend.utils.block_times import get_block_times

if TYPE_CHECKING:
    from sqlalchemy.orm import Session


def get_pool_price_decimals(pool: Pool, height: Optional[int]) -> float:
    return get_pool_price(pool_id=pool.pool_id, height=height) / 10 ** (
            18 + pool.quote_decimals - pool.base_decimals)


def update_total_supply_and_liquidites(pool: Pool):
    stats = get_pool_stats(pool_id=pool.pool_id)
    pool.total_supply = int(stats['total_supply'], 16)
    pool.base_supply = int(stats['base'], 16) / 10 ** pool.base_decimals
    pool.quote_supply = int(stats['quote'], 16) / 10 ** pool.quote_decimals


def get_pool_price_decimals_fallback(
        pool: Pool,
        height: Optional[int],
        fallback: float
) -> float:
    try:
        return get_pool_price_decimals(pool=pool, height=height)
    except ReachableNotValidException:
        logger.info(f"Pool id {pool.pool_id} not able get price at height={height}.")
        return fallback


def run_pool_prices(session: 'Session'):
    logger.info("Running pool prices cron...")

    result = session.execute(select(Pool).where(Pool.chain_id == settings.CHAIN_ID))
    pools: list[Pool] = result.scalars().all()

    block_height_24h, block_height_7d, block_height_30d = get_block_times()

    for pool in pools:
        # TODO: This could be updated as it is erroneous to simply return a fallback
        #  Instead the fallback could be when the first trade happened. Can't be the
        #  pool origination date as there is no trade then.
        price = get_pool_price_decimals_fallback(
            pool=pool, height=None, fallback=0  # Fallback means no trades / 0 price
        )
        price_24h = get_pool_price_decimals_fallback(
            pool=pool, height=block_height_24h, fallback=price
        )
        price_7d = get_pool_price_decimals_fallback(
            pool=pool, height=block_height_7d, fallback=price_24h
        )
        price_30d = get_pool_price_decimals_fallback(
            pool=pool, height=block_height_30d, fallback=price_7d
        )

        pool.price = price
        pool.price_change_24h = price - price_24h
        pool.price_change_7d = price - price_7d
        pool.price_change_30d = price - price_30d

        # TODO: Fix this
        update_total_supply_and_liquidites(pool=pool)

        # pool.total_supply = get_contract_method_int(
        #     to_address=addresses.DEX_CONTRACT_ADDRESS,
        #     method='totalSupply',
        # )
        # TODO: Implement stream processor to find total participants then query that
        # pool.holders =

        session.merge(pool)
        session.commit()

        # TODO: RM this -> Should go in contract methods
        # pool_price = PoolPrice(
        #     base_address=pool.base_address,
        #     quote_address=pool.quote_address,
        #     pool_id=pool.pool_id,
        #     name=pool.name,
        #     timestamp=int(datetime.now().timestamp()),
        #     price=pool.price,
        # )


if __name__ == "__main__":
    from balanced_backend.db import session_factory

    run_pool_prices(session_factory())
