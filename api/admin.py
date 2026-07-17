from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from core.logger import get_logger
from api.auth import get_current_user
from core.database import get_db
from models.user import User


router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
)
logger = get_logger("AdminAPI")

def require_admin(
    current_user: User = Depends(get_current_user),
):
    if current_user.role != "admin":
        logger.warning(
            "Admin access denied | user_id=%s | email=%s | role=%s",
            current_user.id,
            current_user.email,
            current_user.role,
        )

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required.",
        )
    logger.info(
        "Admin access granted | user_id=%s | email=%s",
        current_user.id,
        current_user.email,
    )

    return current_user


@router.get("/users")
def list_users(
    db: Session = Depends(get_db),
    admin_user: User = Depends(require_admin),
):
    users = db.query(User).all()

    return [
        {
            "id": user.id,
            "email": user.email,
            "full_name": user.full_name,
            "role": user.role,
            "is_active": user.is_active,
        }
        for user in users
    ]