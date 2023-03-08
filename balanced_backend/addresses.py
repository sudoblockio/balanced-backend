import os
from pydantic import BaseSettings


class Addresses(BaseSettings):
    GOVERNANCE_ADDRESS: str = "cx0000000000000000000000000000000000000000"

    # Contract addresses
    LOANS_CONTRACT_ADDRESS: str = "cx66d4d90f5f113eba575bf793570135f9b10cece1"
    STAKING_CONTRACT_ADDRESS: str = "cx43e2eec79eb76293c298f2b17aec06097be606e0"
    DIVIDENDS_CONTRACT_ADDRESS: str = "cx203d9cd2a669be67177e997b8948ce2c35caffae"
    RESERVE_CONTRACT_ADDRESS: str = "cxf58b9a1898998a31be7f1d99276204a3333ac9b3"
    DAOFUND_CONTRACT_ADDRESS: str = "cx835b300dcfe01f0bdb794e134a0c5628384f4367"
    REWARDS_CONTRACT_ADDRESS: str = "cx10d59e8103ab44635190bd4139dbfd682fa2d07e"
    DEX_CONTRACT_ADDRESS: str = "cxa0af3165c08318e988cb30993b3048335b94af6c"
    GOVERNANCE_CONTRACT_ADDRESS: str = "cx44250a12074799e26fdeee75648ae47e2cc84219"
    ORACLE_CONTRACT_ADDRESS: str = "cxe647e0af68a4661566f5e9861ad4ac854de808a2"
    SICX_CONTRACT_ADDRESS: str = "cx2609b924e33ef00b648a409245c7ea394c467824"
    BNUSD_CONTRACT_ADDRESS: str = "cx88fd7df7ddff82f7cc735c871dc519838cb235bb"
    BALANCED_TOKEN_CONTRACT_ADDRESS: str = "cxf61cd5a45dc9f91c15aa65831a30a90d59a09619"
    BALANCED_WORKER_TOKEN_CONTRACT_ADDRESS: str = "cxcfe9d1f83fa871e903008471cca786662437e58d"
    BAND_CONTRACT_ADDRESS: str = "cxe647e0af68a4661566f5e9861ad4ac854de808a2"  # Post 59878978
    BAND_CONTRACT_ADDRESS_PYTHON: str = "cx087b4164a87fdfb7b714f3bafe9dfb050fd6b132"  # Pre 59878978
    BAND_REF_CONTRACT_ADDRESS: str = "cxca5faa5a71d986a2e84dd7e6f5ff791d29901ebe"
    REBALANCING_CONTRACT_ADDRESS: str = "cx40d59439571299bca40362db2a7d8cae5b0b30b0"
    STABILITY_FUND_CONTRACT_ADDRESS: str = "cxa09dbb60dcb62fffbd232b6eae132d730a2aafa6"

    class Config:
        case_sensitive = True


if os.environ.get("ADDRESS_ENV_FILE", False):
    addresses = Addresses(_env_file=os.environ.get("ADDRESS_ENV_FILE"))
else:
    addresses = Addresses()
