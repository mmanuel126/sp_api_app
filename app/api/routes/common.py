# app/api/routes/common.py - social networking app common related endpoints

from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from pytest import Session
from app.auth.dependencies import get_current_user
from app.crud.common import get_ads, get_recent_news, get_schools_by_state, get_sports, get_states
from app.db.session import get_db
import logging
from app.schemas.common import Ads, RecentNews, Schools, Sports, States

router = APIRouter(prefix="/common", tags=["Common"])

# Setup logger 
logger = logging.getLogger("my_logger")
logging.basicConfig(level=logging.ERROR)

#-------------------------------get U.S. States----------------------------------------------------

@router.get("/states",response_model=List[States],
    summary="Gets the list of states",
    description="This endpoint helps gets the list of states."
)
def states(db: Session = Depends(get_db),current_user: str = Depends(get_current_user)):
    try:
        st = get_states(db)
        if not st:
            raise HTTPException(status_code=404, detail="States not found.")
        return st
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

#---------------------------------logs erors to a file--------------------------------------------------

@router.post("/logs", summary="logs into a file an error message and stack trace.", 
             description="This endpoint logs the specified log info such as error msg, and stack trace into a file.")
def log_error(message: str = Query(...), stack: str = Query(...)):
    try:
        log_text = f"Error Message: {message}\nStack Trace: {stack}"
        logger.error(log_text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

#----------------------------------sports list-------------------------------------------------

@router.get("/sports",response_model=List[Sports],
    summary="Gets the list of sports",
    description="This endpoint gets the list of sports."
)
def sports(db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    try:
        sp = get_sports(db)
        if not sp:
            raise HTTPException(status_code=404, detail="Sports not found.")
        return sp
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

#----------------------------------list of schools-------------------------------------------------

@router.get("/schools",response_model=List[Schools],
    summary="Gets the list of schools",
    description="This endpoint gets the list of schools given a state and school type such as college high school, etc."
)
def schools(
    state: str = Query(..., description="State abbreviation"),
    institutionType: str = Query(..., description="Type of institution"),
    db: Session = Depends(get_db), 
    current_user: str = Depends(get_current_user)
):
    try: 
        sc = get_schools_by_state(db, state, institutionType)
        if not sc:
            raise HTTPException(status_code=404, detail="No schools found.")
        return sc
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
#-------------------------------------list of Ads----------------------------------------------

@router.get("/ads",response_model=List[Ads],
    summary="Gets the list of Ads.",
    description="This endpoint returns the list of ads depending on type."
)
def ads(
    type: str = Query(..., description="the type of ads"),
    db: Session = Depends(get_db), 
    current_user: str = Depends(get_current_user)
):
    try:
        ad = get_ads(db, type)
        if not ad:
            raise HTTPException(status_code=404, detail="No ads found.")
        return ad
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
#--------------------------------------list of recent news---------------------------------------------

@router.get("/news",response_model=List[RecentNews],
    summary="Gets the list of recent news.",
    description="This endpoint gets the list of recent news."
)
def news(db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    try:
        rn = get_recent_news(db)
        if not rn:
            raise HTTPException(status_code=404, detail="News not found.")
        return rn
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


