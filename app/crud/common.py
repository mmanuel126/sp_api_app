# app/crud/common.py
# This module provides reusable database queries for:
    # * Listing states and sports for dropdowns.
    # * Fetching schools (public, private, or colleges) by state.
    # * Loading ads dynamically by type.
    # * Retrieving recent news for the application.
    # * These functions are simple and efficient, focused on read-only access to common/shared data across the app (often public-facing or used in forms).

from typing import List
from pytest import Session
from sqlalchemy import text
from app.core.config import Settings
from app.db.models.sp_db_models import Tbads, Tbcolleges, Tbprivateschools, Tbrecentnews, Tbsports, Tbstates, t_tbpublicschools
from app.schemas.common import Ads, RecentNews, Schools, Sports, States

#------------------------------------------------------------------------------------
def get_states(db: Session) -> List[States]:
    """
    Retrieves a list of U.S. states from the database.
    - Returns the list ordered alphabetically by state name.
    - Used to populate dropdowns or filters.
    """
    return db.query(Tbstates).order_by(Tbstates.name.asc()).all()

#-----------------------------------------------------------------------------------

def get_sports(db: Session) -> List[Sports]:
    """
    Retrieves all sports from the database.
    - Returns them ordered alphabetically by name.
    - Typically used to show sport options in filters, forms, etc.
    """
    return db.query(Tbsports).order_by(Tbsports.name.asc()).all()

#-----------------------------------------------------------------------------------

def get_schools_by_state(db:Session, state: str, institution_type:str) -> List[Schools]:
    """
    Fetches a list of schools in a given state, filtered by institution type:
    - "1" = Public schools
    - "2" = Private schools
    - "3" = Colleges

    Returns a standardized list of Schools (school_id, school_name).
    Used in school selectors, filtering users by location/education, etc.
    """
    results = []
    if institution_type == "1":  # Public
        query = (
            db.query(t_tbpublicschools)
            .filter(t_tbpublicschools.state == state)
            .order_by(t_tbpublicschools.school_name.asc())
            .distinct()
            .all()
        )
        results = [
            Schools(
                school_id=str(s.lgid),
                SchoolName=s.school_name or ""
            )
            for s in query
        ]
    elif institution_type == "2":  # Private
        query = (
            db.query(Tbprivateschools)
            .filter(Tbprivateschools.state == state)
            .order_by(Tbprivateschools.school_name.asc())
            .distinct()
            .all()
        )
        results = [
            Schools(
                school_id=str(s.lg_id),
                school_name=s.school_name or ""
            )
            for s in query
        ]
    elif institution_type == "3":  # Colleges
        query = (
            db.query(Tbcolleges)
            .filter(Tbcolleges.state == state)
            .order_by(Tbcolleges.name.asc())
            .distinct()
            .all()
        )
        results = [
            Schools(
                school_id=str(s.school_id),
                school_name=s.name or ""
            )
            for s in query
        ]
    return results

#-----------------------------------------------------------------------------------

def get_ads(db:Session, type: str) -> List[Ads]:
    """
    Retrieves a list of ads filtered by type.
    - Could be used to load ads for a specific location, page, or user role.
    """
    query = (
        db.query(Tbads)
        .filter(Tbads.type == type)
        .all()
    )
    return query

#-----------------------------------------------------------------------------------

def get_recent_news(db:Session) -> List[RecentNews]:
    """
    Retrieves a list of recent news items from the database.
    - Could be displayed on a homepage, dashboard, or news feed.
    """
    query = (
        db.query(Tbrecentnews)
        .all()
    )
    return query

#-----------------------------------------------------------------------------------