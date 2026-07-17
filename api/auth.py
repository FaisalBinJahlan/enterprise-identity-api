from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from core.database import get_db
from core.logger import get_logger
from models.user import User
from schemas.auth import (LoginRequest,RegisterRequest,RegisterResponse,TokenResponse,CurrentUserResponse,)
from security.crypto_manager import CryptoManager
from security.jwt_manager import JWTManager
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
router = APIRouter(prefix="/auth", tags=["Auth"])

crypto = CryptoManager()
jwt_manager = JWTManager()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")
logger = get_logger("AuthAPI")

@router.post(
    "/register",
    response_model=RegisterResponse,
    status_code=status.HTTP_201_CREATED,
)
def register_user(
    payload: RegisterRequest,
    db: Session = Depends(get_db),
):
    existing_user = db.query(User).filter(User.email == payload.email).first()

    if existing_user:
        logger.warning(
         "Registration failed: email already exists | email=%s",
            payload.email,
        )

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email is already registered.",
        )

    hashed_password = crypto.hash_password(payload.password)

    new_user = User(
        email=payload.email,
        full_name=payload.full_name,
        hashed_password=hashed_password,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    logger.info(
    "New user registered | user_id=%s | email=%s",
    new_user.id,
    new_user.email,
    )

    return RegisterResponse(
        message="User registered successfully",
        email=new_user.email,
        full_name=new_user.full_name,
    )

@router.post(
    "/login",
    response_model=TokenResponse,
)
def login_user(
    payload: LoginRequest,
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.email == payload.email).first()

    if not user:
        logger.warning(
        "Login failed: user not found | email=%s",
        payload.email,
        )
        
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
        )

    is_password_valid = crypto.verify_password(
        payload.password,
        user.hashed_password,
    )

    if not is_password_valid:
        logger.warning(
        "Login failed: invalid password | user_id=%s | email=%s",
        user.id,
        user.email,
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
        )

    access_token = jwt_manager.create_access_token(
        subject=str(user.id),
        extra_claims={
            "email": user.email,
        },
    )
    logger.info(
    "Login successful | user_id=%s | email=%s",
    user.id,
    user.email,
    )

    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
    )

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    try:
        payload = jwt_manager.decode_access_token(token)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_id = payload.get("sub")

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = db.query(User).filter(User.id == int(user_id)).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User no longer exists.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is disabled.",
        )

    return user

@router.get(
    "/me",
    response_model=CurrentUserResponse,
)
def get_me(
    current_user: User = Depends(get_current_user),
):
    return CurrentUserResponse(
        id=current_user.id,
        email=current_user.email,
        full_name=current_user.full_name,
        role=current_user.role,
        is_active=current_user.is_active,
    )

@router.post("/token", response_model=TokenResponse)
def login_for_swagger(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.email == form_data.username).first()

    if not user:
        logger.warning(
            "Swagger login failed: user not found | email=%s",
            form_data.username,
        )

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    is_password_valid = crypto.verify_password(
        form_data.password,
        user.hashed_password,
    )

    if not is_password_valid:
        logger.warning(
            "Swagger login failed: invalid password | user_id=%s | email=%s",
            user.id,
            user.email,
        )

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = jwt_manager.create_access_token(
        subject=str(user.id),
        extra_claims={
            "email": user.email,
        },
    )

    logger.info(
        "Swagger login successful | user_id=%s | email=%s",
        user.id,
        user.email,
    )

    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
    )