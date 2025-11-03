from fastapi import status, Header, HTTPException

from config.init import conf


async def verify_api_key(x_auth_key: str = Header(...)):
    """
    Dependency только для документации Swagger
    Фактическую проверку делает мидлварь
    """
    if not x_auth_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key"
        )
    
    if x_auth_key != conf.secret_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key"
        )
    return x_auth_key