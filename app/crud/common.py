# app/crud/common.py

from typing import List
from pytest import Session
from sqlalchemy import text
from app.core.config import Settings
from app.db.models.sp_db_models import TbAds, TbColleges, TbPrivateSchools, TbPublicSchools, TbRecentNews, TbSports, TbStates
from app.schemas.common import Ads, RecentNews, Schools, Sports, States


def get_states(db: Session) -> List[States]:
    return db.query(TbStates).order_by(TbStates.Name.asc()).all()

#-----------------------------------------------------------------------------------

def get_sports(db: Session) -> List[Sports]:
    return db.query(TbSports).order_by(TbSports.Name.asc()).all()

#-----------------------------------------------------------------------------------

def get_schools_by_state(db:Session, state: str, institution_type:str) -> List[Schools]:
    results = []
    if institution_type == "1":  # Public
        query = (
            db.query(TbPublicSchools)
            .filter(TbPublicSchools.State == state)
            .order_by(TbPublicSchools.SchoolName.asc())
            .distinct()
            .all()
        )
        results = [
            Schools(
                SchoolId=str(s.Lgid),
                SchoolName=s.SchoolName or ""
            )
            for s in query
        ]
    elif institution_type == "2":  # Private
        query = (
            db.query(TbPrivateSchools)
            .filter(TbPrivateSchools.State == state)
            .order_by(TbPrivateSchools.SchoolName.asc())
            .distinct()
            .all()
        )
        results = [
            Schools(
                SchoolId=str(s.Lgid),
                SchoolName=s.SchoolName or ""
            )
            for s in query
        ]
    elif institution_type == "3":  # Colleges
        query = (
            db.query(TbColleges)
            .filter(TbColleges.State == state)
            .order_by(TbColleges.Name.asc())
            .distinct()
            .all()
        )
        results = [
            Schools(
                SchoolID=str(s.SchoolID),
                SchoolName=s.Name or ""
            )
            for s in query
        ]
    return results

#-----------------------------------------------------------------------------------

def get_ads(db:Session, type: str) -> List[Ads]:
    query = (
        db.query(TbAds)
        .filter(TbAds.Type == type)
        .all()
    )
    return query

#-----------------------------------------------------------------------------------

def get_recent_news(db:Session) -> List[RecentNews]:
    query = (
        db.query(TbRecentNews)
        .all()
    )
    return query

#-----------------------------------------------------------------------------------