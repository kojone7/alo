from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
import logging

from database import get_db
import schemas
from auth import (
    get_current_user, 
    get_password_hash, 
    verify_password, 
    create_access_token,
    ACCESS_TOKEN_EXPIRE_MINUTES
)
from models import User, UserProfile

# Configura il logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={404: {"description": "Not found"}},
)


@router.post("/register", response_model=schemas.User)
async def register(user_data: schemas.UserCreate, db: Session = Depends(get_db)):
    try:
        logger.info(f"Tentativo di registrazione per email: {user_data.email}")
        
        # Verifica se l'utente esiste già
        db_user = db.query(User).filter(User.email == user_data.email).first()
        if db_user:
            logger.warning(f"Email già registrata: {user_data.email}")
            raise HTTPException(status_code=400, detail="Email già registrata")
        
        if user_data.password != user_data.confirm_password:
            logger.warning("Le password non coincidono")
            raise HTTPException(status_code=400, detail="Le password non coincidono")

        # Crea il nuovo utente
        db_user = User(
            email=user_data.email,
            hashed_password=get_password_hash(user_data.password),
            full_name=user_data.full_name,
            is_active=True
        )
        
        logger.info("Creazione nuovo utente nel database")
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        
        # Crea un profilo utente base
        logger.info("Creazione profilo utente base")
        db_profile = UserProfile(
            user_id=db_user.id,
            indirizzo="",
            citta="",
            cap="",
            telefono="",
            rating_medio=0.0
        )
        db.add(db_profile)
        db.commit()
        db.refresh(db_profile)
        
        logger.info(f"Registrazione completata con successo per: {user_data.email}")
        return db_user
        
    except HTTPException as he:
        logger.error(f"HTTP Exception durante la registrazione: {str(he.detail)}")
        raise he
    except Exception as e:
        logger.error(f"Errore durante la registrazione: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Errore durante la registrazione: {str(e)}"
        )


@router.post("/token", response_model=schemas.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    try:
        logger.info(f"Tentativo di login per: {form_data.username}")
        
        # Cerca l'utente nel database
        user = db.query(User).filter(User.email == form_data.username).first()
        if not user:
            logger.warning(f"Utente non trovato: {form_data.username}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Email o password non corrette",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Verifica la password
        if not verify_password(form_data.password, user.hashed_password):
            logger.warning(f"Password non valida per: {form_data.username}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Email o password non corrette",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Crea il token di accesso
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.email}, expires_delta=access_token_expires
        )
        
        logger.info(f"Login completato con successo per: {form_data.username}")
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user_id": user.id
        }
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"Errore durante il login: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Errore durante il login: {str(e)}"
        )


@router.get("/me", response_model=schemas.UserDetail)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user