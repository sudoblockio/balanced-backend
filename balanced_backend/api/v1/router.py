from fastapi import APIRouter

from balanced_backend.api.v1.endpoints import (
    supply,
    volumes,
    pools,
    tokens,
    holders,
    cmc,
    coingecko,
    stats,
    contract_methods,
)

api_router = APIRouter()
api_router.include_router(contract_methods.router)
api_router.include_router(volumes.router)
api_router.include_router(pools.router)
api_router.include_router(tokens.router)
api_router.include_router(holders.router)
api_router.include_router(cmc.router, prefix='/coin-market-cap',
                          tags=["coin-market-cap"])
api_router.include_router(coingecko.router, prefix='/coingecko', tags=["coingecko"])
api_router.include_router(stats.router)
api_router.include_router(supply.router)
