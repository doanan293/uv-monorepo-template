from fastapi import APIRouter

router = APIRouter(tags=["health"])


@router.get("/health")
def get_health() -> dict[str, str]:
    """Report that the service is up.

    Returns:
        `{"status": "ok"}` while the process is serving requests.
    """
    return {"status": "ok"}
