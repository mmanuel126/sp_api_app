from typing import List, Optional

from sqlalchemy import BigInteger, Boolean, Column, DateTime, ForeignKeyConstraint, Identity, Integer, Numeric, PrimaryKeyConstraint, REAL, String, Table, Text, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
import datetime
import decimal

class Base(DeclarativeBase):
    pass


class Tbads(Base):
    __tablename__ = 'tbads'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='tbads_pkey'),
    )

    id: Mapped[int] = mapped_column(BigInteger, Identity(always=True, start=1, increment=1, minvalue=1, maxvalue=9223372036854775807, cycle=False, cache=1), primary_key=True)
    name: Mapped[Optional[str]] = mapped_column(String(150))
    headertext: Mapped[Optional[str]] = mapped_column(String(150))
    postingdate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    textfield: Mapped[Optional[str]] = mapped_column(String(2000))
    navigateurl: Mapped[Optional[str]] = mapped_column(String(200))
    imageurl: Mapped[Optional[str]] = mapped_column(String(100))
    type: Mapped[Optional[str]] = mapped_column(String(100))


class Tbcolleges(Base):
    __tablename__ = 'tbcolleges'
    __table_args__ = (
        PrimaryKeyConstraint('school_id', name='tbcolleges_pkey'),
    )

    school_id: Mapped[int] = mapped_column(BigInteger, Identity(always=True, start=1, increment=1, minvalue=1, maxvalue=9223372036854775807, cycle=False, cache=1), primary_key=True)
    name: Mapped[Optional[str]] = mapped_column(String(200))
    address: Mapped[Optional[str]] = mapped_column(String(250))
    phone: Mapped[Optional[str]] = mapped_column(String(50))
    website: Mapped[Optional[str]] = mapped_column(String(150))
    type: Mapped[Optional[str]] = mapped_column(String(250))
    awards_offered: Mapped[Optional[str]] = mapped_column(String(500))
    campus_setting: Mapped[Optional[str]] = mapped_column(String(90))
    campus_housing: Mapped[Optional[str]] = mapped_column(String(150))
    student_population: Mapped[Optional[int]] = mapped_column(BigInteger)
    undergrad_students: Mapped[Optional[int]] = mapped_column(BigInteger)
    Student_to_faculty_ratio: Mapped[Optional[str]] = mapped_column(String(50))
    ipedsid: Mapped[Optional[str]] = mapped_column(String(150))
    opeid: Mapped[Optional[str]] = mapped_column(String(50))
    state: Mapped[Optional[str]] = mapped_column(String(10))
    imagefile: Mapped[Optional[str]] = mapped_column(String(50))


class Tbdays(Base):
    __tablename__ = 'tbdays'
    __table_args__ = (
        PrimaryKeyConstraint('day', name='tbdays_pkey'),
        UniqueConstraint('day', name='tbdays_Day_key'),
        UniqueConstraint('day', name='tbdays_day_key')
    )

    day: Mapped[str] = mapped_column(String(2), primary_key=True)


class Tbdegreetype(Base):
    __tablename__ = 'tbdegreetype'
    __table_args__ = (
        PrimaryKeyConstraint('degree_type_id', name='tbdegreetype_pkey'),
        UniqueConstraint('degree_type_id', name='tbdegreetype_degree_type_id_key'),
        UniqueConstraint('degree_type_id', name='tbdegreetype_DegreeTypeID_key')
    )

    degree_type_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    degree_type_desc: Mapped[Optional[str]] = mapped_column(String(50))


class Tbforgotpwdcodes(Base):
    __tablename__ = 'tbforgotpwdcodes'
    __table_args__ = (
        PrimaryKeyConstraint('code_id', name='tbforgotpwdcodes_pkey'),
        UniqueConstraint('code_id', name='tbforgotpwdcodes_CodeID_key'),
        UniqueConstraint('code_id', name='tbforgotpwdcodes_code_id_key')
    )

    code_id: Mapped[int] = mapped_column(BigInteger, Identity(always=True, start=1, increment=1, minvalue=1, maxvalue=9223372036854775807, cycle=False, cache=1), primary_key=True)
    email: Mapped[Optional[str]] = mapped_column(String(100))
    codedate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    status: Mapped[Optional[int]] = mapped_column(BigInteger)


class Tbinterests(Base):
    __tablename__ = 'tbinterests'
    __table_args__ = (
        PrimaryKeyConstraint('interest_id', name='tbinterests_pkey'),
        UniqueConstraint('interest_id', name='tbinterests_InterestID_key'),
        UniqueConstraint('interest_id', name='tbinterests_interest_id_key')
    )

    interest_id: Mapped[int] = mapped_column(BigInteger, Identity(always=True, start=1, increment=1, minvalue=1, maxvalue=9223372036854775807, cycle=False, cache=1), primary_key=True)
    interest_desc: Mapped[Optional[str]] = mapped_column(String(150))
    interest_type: Mapped[Optional[str]] = mapped_column(String(20))


class Tbmajors(Base):
    __tablename__ = 'tbmajors'
    __table_args__ = (
        PrimaryKeyConstraint('major_id', name='tbmajors_pkey'),
        UniqueConstraint('major_id', name='tbmajors_major_id_key'),
        UniqueConstraint('major_id', name='tbmajors_MajorID_key')
    )

    major_id: Mapped[int] = mapped_column(BigInteger, Identity(always=True, start=1, increment=1, minvalue=1, maxvalue=9223372036854775807, cycle=False, cache=1), primary_key=True)
    major_desc: Mapped[Optional[str]] = mapped_column(String(100))


class Tbmemberfollowing(Base):
    __tablename__ = 'tbmemberfollowing'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='tbmemberfollowing_pkey'),
        UniqueConstraint('id', name='tbmemberfollowing_id_key'),
        UniqueConstraint('id', name='tbmemberfollowing_Id_key')
    )

    id: Mapped[int] = mapped_column(BigInteger, Identity(always=True, start=1, increment=1, minvalue=1, maxvalue=9223372036854775807, cycle=False, cache=1), primary_key=True)
    member_id: Mapped[Optional[int]] = mapped_column(BigInteger)
    following_member_id: Mapped[Optional[int]] = mapped_column(BigInteger)


class Tbmembernotifications(Base):
    __tablename__ = 'tbmembernotifications'
    __table_args__ = (
        PrimaryKeyConstraint('notification_member_id', 'member_id', 'notification_id', name='tbmembernotifications_pkey'),
    )

    notification_member_id: Mapped[int] = mapped_column(BigInteger, Identity(always=True, start=1, increment=1, minvalue=1, maxvalue=9223372036854775807, cycle=False, cache=1), primary_key=True)
    member_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    notification_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)


class Tbmemberprofileeducationv2(Base):
    __tablename__ = 'tbmemberprofileeducationv2'
    __table_args__ = (
        PrimaryKeyConstraint('member_id', 'school_id', 'school_type', name='tbmemberprofileeducationv2_pkey'),
    )

    member_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    school_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    school_type: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    school_name: Mapped[Optional[str]] = mapped_column(String(100))
    class_year: Mapped[Optional[str]] = mapped_column(String(10))
    major: Mapped[Optional[str]] = mapped_column(String(100))
    degree_type: Mapped[Optional[int]] = mapped_column(BigInteger)
    societies: Mapped[Optional[str]] = mapped_column(String(300))
    description: Mapped[Optional[str]] = mapped_column(String(200))
    sport_level_type: Mapped[Optional[str]] = mapped_column(String(20))


class Tbmemberprofilepictures(Base):
    __tablename__ = 'tbmemberprofilepictures'
    __table_args__ = (
        PrimaryKeyConstraint('profile_id', 'member_id', name='tbmemberprofilepictures_pkey'),
    )

    profile_id: Mapped[int] = mapped_column(BigInteger, Identity(always=True, start=1, increment=1, minvalue=1, maxvalue=9223372036854775807, cycle=False, cache=1), primary_key=True)
    member_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    file_name: Mapped[Optional[str]] = mapped_column(String(100))
    is_default: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(1, 0))
    removed: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(1, 0))


class Tbmembers(Base):
    __tablename__ = 'tbmembers'
    __table_args__ = (
        PrimaryKeyConstraint('member_id', name='tbmembers_pkey'),
        UniqueConstraint('member_id', name='tbmembers_MemberID_key'),
        UniqueConstraint('member_id', name='tbmembers_member_id_key'),
        {'schema': 'public'}
    )

    member_id: Mapped[int] = mapped_column(BigInteger, Identity(always=True, start=1, increment=1, minvalue=1, maxvalue=9223372036854775807, cycle=False, cache=1), primary_key=True)
    email: Mapped[Optional[str]] = mapped_column(String(100))
    password: Mapped[Optional[str]] = mapped_column(String(50))
    status: Mapped[Optional[int]] = mapped_column(BigInteger)
    security_question: Mapped[Optional[int]] = mapped_column(BigInteger)
    security_answer: Mapped[Optional[str]] = mapped_column(String(50))
    deactivate_reason: Mapped[Optional[int]] = mapped_column(BigInteger)
    deactivate_explanation: Mapped[Optional[str]] = mapped_column(String(1000))
    future_emails: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(1, 0))
    chat_status: Mapped[Optional[int]] = mapped_column(BigInteger)
    log_on: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(1, 0))
    youtube_channel: Mapped[Optional[str]] = mapped_column(String(100))

    tbcontactrequests: Mapped[List['Tbcontactrequests']] = relationship('Tbcontactrequests', foreign_keys='[Tbcontactrequests.from_member_id]', back_populates='from_member')
    tbcontactrequests_: Mapped[List['Tbcontactrequests']] = relationship('Tbcontactrequests', foreign_keys='[Tbcontactrequests.to_member_id]', back_populates='to_member')
    tbcontacts: Mapped[List['Tbcontacts']] = relationship('Tbcontacts', foreign_keys='[Tbcontacts.contact_id]', back_populates='contact')
    tbcontacts_: Mapped[List['Tbcontacts']] = relationship('Tbcontacts', foreign_keys='[Tbcontacts.member_id]', back_populates='member')
    tbmemberposts: Mapped[List['Tbmemberposts']] = relationship('Tbmemberposts', back_populates='member')
    tbmembersprivacysettings: Mapped[List['Tbmembersprivacysettings']] = relationship('Tbmembersprivacysettings', back_populates='member')
    tbmembersregistered: Mapped[List['Tbmembersregistered']] = relationship('Tbmembersregistered', back_populates='member')
    tbmessages: Mapped[List['Tbmessages']] = relationship('Tbmessages', foreign_keys='[Tbmessages.contact_id]', back_populates='contact')
    tbmessages_: Mapped[List['Tbmessages']] = relationship('Tbmessages', foreign_keys='[Tbmessages.sender_id]', back_populates='sender')
    tbnotificationsettings: Mapped[List['Tbnotificationsettings']] = relationship('Tbnotificationsettings', back_populates='member')
    tbmemberpostresponses: Mapped[List['Tbmemberpostresponses']] = relationship('Tbmemberpostresponses', back_populates='member')


t_tbmonths = Table(
    'tbmonths', Base.metadata,
    Column('month', String(2)),
    Column('desc', String(20))
)


class Tbnotifications(Base):
    __tablename__ = 'tbnotifications'
    __table_args__ = (
        PrimaryKeyConstraint('notification_id', name='tbnotifications_pkey'),
        UniqueConstraint('notification_id', name='tbnotifications_NotificationID_key'),
        UniqueConstraint('notification_id', name='tbnotifications_notification_id_key')
    )

    notification_id: Mapped[int] = mapped_column(BigInteger, Identity(always=True, start=1, increment=1, minvalue=1, maxvalue=9223372036854775807, cycle=False, cache=1), primary_key=True)
    subject: Mapped[Optional[str]] = mapped_column(String(100))
    notification: Mapped[Optional[str]] = mapped_column(String(2000))
    sent_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    status: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(1, 0))


class Tbprivateschools(Base):
    __tablename__ = 'tbprivateschools'
    __table_args__ = (
        PrimaryKeyConstraint('lg_id', name='tbprivateschools_pkey'),
        UniqueConstraint('lg_id', name='tbprivateschools_lg_id_key'),
        UniqueConstraint('lg_id', name='tbprivateschools_LGId_key')
    )

    lg_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    pss_school_id: Mapped[Optional[str]] = mapped_column(String(255))
    school_name: Mapped[Optional[str]] = mapped_column(String(255))
    Lo_grade: Mapped[Optional[str]] = mapped_column(String(255))
    hi_grade: Mapped[Optional[str]] = mapped_column(String(255))
    street_name: Mapped[Optional[str]] = mapped_column(String(255))
    city: Mapped[Optional[str]] = mapped_column(String(255))
    pss_county_no: Mapped[Optional[str]] = mapped_column(String(255))
    pss_county_fips: Mapped[Optional[str]] = mapped_column(String(255))
    state: Mapped[Optional[str]] = mapped_column(String(255))
    pss_fips: Mapped[Optional[str]] = mapped_column(String(255))
    zip: Mapped[Optional[str]] = mapped_column(String(255))
    phone: Mapped[Optional[str]] = mapped_column(String(255))
    PSS_SCH_DAYS: Mapped[Optional[str]] = mapped_column(String(255))
    PSS_STU_DAY_HRS: Mapped[Optional[str]] = mapped_column(String(255))
    PSS_LIBRARY: Mapped[Optional[str]] = mapped_column(String(255))
    PSS_ENROLL_UG: Mapped[Optional[str]] = mapped_column(String(255))
    PSS_ENROLL_PK: Mapped[Optional[str]] = mapped_column(String(255))
    PSS_ENROLL_K: Mapped[Optional[str]] = mapped_column(String(255))
    PSS_ENROLL_1: Mapped[Optional[str]] = mapped_column(String(255))
    PSS_ENROLL_2: Mapped[Optional[str]] = mapped_column(String(255))
    PSS_ENROLL_3: Mapped[Optional[str]] = mapped_column(String(255))
    PSS_ENROLL_4: Mapped[Optional[str]] = mapped_column(String(255))
    PSS_ENROLL_5: Mapped[Optional[str]] = mapped_column(String(255))
    PSS_ENROLL_6: Mapped[Optional[str]] = mapped_column(String(255))
    PSS_ENROLL_7: Mapped[Optional[str]] = mapped_column(String(255))
    PSS_ENROLL_8: Mapped[Optional[str]] = mapped_column(String(255))
    PSS_ENROLL_9: Mapped[Optional[str]] = mapped_column(String(255))
    PSS_ENROLL_10: Mapped[Optional[str]] = mapped_column(String(255))
    PSS_ENROLL_11: Mapped[Optional[str]] = mapped_column(String(255))
    PSS_ENROLL_12: Mapped[Optional[str]] = mapped_column(String(255))
    PSS_ENROLL_T: Mapped[Optional[str]] = mapped_column(String(255))
    PSS_ENROLL_TK12: Mapped[Optional[str]] = mapped_column(String(255))
    PSS_RACE_AI: Mapped[Optional[str]] = mapped_column(String(255))
    PSS_RACE_AS: Mapped[Optional[str]] = mapped_column(String(255))
    PSS_RACE_H: Mapped[Optional[str]] = mapped_column(String(255))
    PSS_RACE_B: Mapped[Optional[str]] = mapped_column(String(255))
    PSS_RACE_W: Mapped[Optional[str]] = mapped_column(String(255))
    PSS_RACE_P: Mapped[Optional[str]] = mapped_column(String(255))
    PSS_RACE_2: Mapped[Optional[str]] = mapped_column(String(255))
    PSS_FTE_TEACH: Mapped[Optional[str]] = mapped_column(String(255))
    PSS_LOCALE: Mapped[Optional[str]] = mapped_column(String(255))
    PSS_COED: Mapped[Optional[str]] = mapped_column(String(255))
    PSS_TYPE: Mapped[Optional[str]] = mapped_column(String(255))
    PSS_LEVEL: Mapped[Optional[str]] = mapped_column(String(255))
    PSS_RELIG: Mapped[Optional[str]] = mapped_column(String(255))
    PSS_COMM_TYPE: Mapped[Optional[str]] = mapped_column(String(255))
    PSS_INDIAN_PCT: Mapped[Optional[str]] = mapped_column(String(255))
    PSS_ASIAN_PCT: Mapped[Optional[str]] = mapped_column(String(255))
    PSS_HISP_PCT: Mapped[Optional[str]] = mapped_column(String(255))
    PSS_BLACK_PCT: Mapped[Optional[str]] = mapped_column(String(255))
    PSS_WHITE_PCT: Mapped[Optional[str]] = mapped_column(String(255))
    P_PACISL_PCT: Mapped[Optional[str]] = mapped_column(String(255))
    P_TWOMORE_PCT: Mapped[Optional[str]] = mapped_column(String(255))
    PSS_STDTCH_RT: Mapped[Optional[str]] = mapped_column(String(255))
    PSS_ORIENT: Mapped[Optional[str]] = mapped_column(String(255))
    county: Mapped[Optional[str]] = mapped_column(String(255))
    PSS_ASSOC_1: Mapped[Optional[str]] = mapped_column(String(255))
    PSS_ASSOC_2: Mapped[Optional[str]] = mapped_column(String(255))
    PSS_ASSOC_3: Mapped[Optional[str]] = mapped_column(String(255))
    PSS_ASSOC_4: Mapped[Optional[str]] = mapped_column(String(255))
    PSS_ASSOC_5: Mapped[Optional[str]] = mapped_column(String(255))
    PSS_ASSOC_6: Mapped[Optional[str]] = mapped_column(String(255))
    PSS_ASSOC_7: Mapped[Optional[str]] = mapped_column(String(255))
    image_file: Mapped[Optional[str]] = mapped_column(String(255))


t_tbpublicschools = Table(
    'tbpublicschools', Base.metadata,
    Column('school_id', String(50)),
    Column('state_school_id', String(50)),
    Column('district_id', String(50)),
    Column('state_district', String(100)),
    Column('low_grade', String(50)),
    Column('high_grade', String(50)),
    Column('school_name', String(100)),
    Column('district', String(100)),
    Column('country_name', String(100)),
    Column('street_name', String(100)),
    Column('city', String(50)),
    Column('state', String(20)),
    Column('zip', String(10)),
    Column('zip_4_digit', String(4)),
    Column('phone', String(20)),
    Column('local_code', String(50)),
    Column('locale', String(50)),
    Column('charter', String(50)),
    Column('magnet', String(50)),
    Column('titlle_1_school', String(50)),
    Column('title_1_school_wide', String(50)),
    Column('students', BigInteger),
    Column('teachers', BigInteger),
    Column('student_teacher_ratio', REAL),
    Column('free_lunch', BigInteger),
    Column('reduced_lunch', BigInteger),
    Column('image_file', String(70)),
    Column('lgid', BigInteger, nullable=False)
)


class Tbrecentnews(Base):
    __tablename__ = 'tbrecentnews'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='tbrecentnews_pkey'),
        UniqueConstraint('id', name='tbrecentnews_ID_key'),
        UniqueConstraint('id', name='tbrecentnews_id_key')
    )

    id: Mapped[int] = mapped_column(BigInteger, Identity(always=True, start=1, increment=1, minvalue=1, maxvalue=9223372036854775807, cycle=False, cache=1), primary_key=True)
    name: Mapped[Optional[str]] = mapped_column(String(150))
    header_text: Mapped[Optional[str]] = mapped_column(String(150))
    posting_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    text_field: Mapped[Optional[str]] = mapped_column(String(2000))
    navigate_url: Mapped[Optional[str]] = mapped_column(String(200))
    image_url: Mapped[Optional[str]] = mapped_column(String(100))


class Tbschooltype(Base):
    __tablename__ = 'tbschooltype'
    __table_args__ = (
        PrimaryKeyConstraint('school_type_id', name='tbschooltype_pkey'),
        UniqueConstraint('school_type_id', name='tbschooltype_school_type_id_key'),
        UniqueConstraint('school_type_id', name='tbschooltype_SchoolTypeID_key')
    )

    school_type_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    school_type_desc: Mapped[Optional[str]] = mapped_column(String(50))


class Tbsports(Base):
    __tablename__ = 'tbsports'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='tbsports_pkey'),
        UniqueConstraint('id', name='tbsports_id_key')
    )

    id: Mapped[int] = mapped_column(BigInteger, Identity(always=True, start=1, increment=1, minvalue=1, maxvalue=9223372036854775807, cycle=False, cache=1), primary_key=True)
    name: Mapped[Optional[str]] = mapped_column(String(50))


class Tbstates(Base):
    __tablename__ = 'tbstates'
    __table_args__ = (
        PrimaryKeyConstraint('state_id', name='tbstates_pkey'),
        UniqueConstraint('state_id', name='tbstates_state_id_key'),
        UniqueConstraint('state_id', name='tbstates_StateID_key')
    )

    state_id: Mapped[int] = mapped_column(BigInteger, Identity(always=True, start=1, increment=1, minvalue=1, maxvalue=9223372036854775807, cycle=False, cache=1), primary_key=True)
    name: Mapped[Optional[str]] = mapped_column(String(50))
    abbreviation: Mapped[Optional[str]] = mapped_column(String(5))


t_tbyears = Table(
    'tbyears', Base.metadata,
    Column('year', String(4))
)


class Tbcontactrequests(Base):
    __tablename__ = 'tbcontactrequests'
    __table_args__ = (
        ForeignKeyConstraint(['from_member_id'], ['public.tbmembers.member_id'], name='fk_tbcontactrequests_tbmembers'),
        ForeignKeyConstraint(['to_member_id'], ['public.tbmembers.member_id'], name='fk_tbcontactrequests_tbmembers1'),
        PrimaryKeyConstraint('request_id', name='tbcontactrequests_pkey'),
        {'schema': 'public'}
    )

    request_id: Mapped[int] = mapped_column(BigInteger, Identity(always=True, start=1, increment=1, minvalue=1, maxvalue=9223372036854775807, cycle=False, cache=1), primary_key=True)
    from_member_id: Mapped[Optional[int]] = mapped_column(BigInteger)
    to_member_id: Mapped[Optional[int]] = mapped_column(BigInteger)
    request_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    status: Mapped[Optional[int]] = mapped_column(BigInteger)

    from_member: Mapped[Optional['Tbmembers']] = relationship('Tbmembers', foreign_keys=[from_member_id], back_populates='tbcontactrequests')
    to_member: Mapped[Optional['Tbmembers']] = relationship('Tbmembers', foreign_keys=[to_member_id], back_populates='tbcontactrequests_')


class Tbcontacts(Base):
    __tablename__ = 'tbcontacts'
    __table_args__ = (
        ForeignKeyConstraint(['contact_id'], ['public.tbmembers.member_id'], name='fk_tbcontacts_tbmembers1'),
        ForeignKeyConstraint(['member_id'], ['public.tbmembers.member_id'], name='fk_tbcontacts_tbmembers'),
        PrimaryKeyConstraint('member_id', 'contact_id', name='tbfriends_pkey'),
        {'schema': 'public'}
    )

    member_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    contact_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    status: Mapped[int] = mapped_column(BigInteger)
    datestamp: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)

    contact: Mapped['Tbmembers'] = relationship('Tbmembers', foreign_keys=[contact_id], back_populates='tbcontacts')
    member: Mapped['Tbmembers'] = relationship('Tbmembers', foreign_keys=[member_id], back_populates='tbcontacts_')


class Tbmemberposts(Base):
    __tablename__ = 'tbmemberposts'
    __table_args__ = (
        ForeignKeyConstraint(['member_id'], ['public.tbmembers.member_id'], name='fk_tbmemberposts_tbmembers'),
        PrimaryKeyConstraint('post_id', name='tbmemberposts_pkey'),
        UniqueConstraint('post_id', name='tbmemberposts_post_id_key'),
        UniqueConstraint('post_id', name='tbmemberposts_PostID_key'),
        {'schema': 'public'}
    )

    post_id: Mapped[int] = mapped_column(BigInteger, Identity(always=True, start=1, increment=1, minvalue=1, maxvalue=9223372036854775807, cycle=False, cache=1), primary_key=True)
    title: Mapped[Optional[str]] = mapped_column(String(100))
    description: Mapped[Optional[str]] = mapped_column(String(700))
    post_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    attach_file: Mapped[Optional[str]] = mapped_column(String(100))
    member_id: Mapped[Optional[int]] = mapped_column(BigInteger)
    file_type: Mapped[Optional[int]] = mapped_column(BigInteger)
    like_counter: Mapped[Optional[int]] = mapped_column(BigInteger)

    member: Mapped[Optional['Tbmembers']] = relationship('Tbmembers', back_populates='tbmemberposts')
    tbmemberpostresponses: Mapped[List['Tbmemberpostresponses']] = relationship('Tbmemberpostresponses', back_populates='post')


class Tbmemberprofile(Tbmembers):
    __tablename__ = 'tbmemberprofile'
    __table_args__ = (
        ForeignKeyConstraint(['member_id'], ['public.tbmembers.member_id'], name='fk_tbmemberprofile_tbmembers'),
        PrimaryKeyConstraint('member_id', name='tbmemberprofile_pkey'),
        UniqueConstraint('member_id', name='tbmemberprofile_member_id_key'),
        UniqueConstraint('member_id', name='tbmemberprofile_MemberID_key'),
        {'schema': 'public'}
    )

    member_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    first_name: Mapped[Optional[str]] = mapped_column(String(50))
    middle_name: Mapped[Optional[str]] = mapped_column(String(50))
    last_name: Mapped[Optional[str]] = mapped_column(String(50))
    sex: Mapped[Optional[str]] = mapped_column(String(20))
    show_sex_in_profile: Mapped[Optional[bool]] = mapped_column(Boolean)
    dob_month: Mapped[Optional[str]] = mapped_column(String(3))
    dob_day: Mapped[Optional[str]] = mapped_column(String(3))
    dob_year: Mapped[Optional[str]] = mapped_column(String(5))
    show_dob_type: Mapped[Optional[bool]] = mapped_column(Boolean)
    hometown: Mapped[Optional[str]] = mapped_column(String(50))
    home_neighborhood: Mapped[Optional[str]] = mapped_column(String(50))
    current_status: Mapped[Optional[str]] = mapped_column(String(50))
    interested_in_type: Mapped[Optional[int]] = mapped_column(Integer)
    looking_for_employment: Mapped[Optional[bool]] = mapped_column(Boolean)
    looking_for_recruitment: Mapped[Optional[bool]] = mapped_column(Boolean)
    looking_for_partnership: Mapped[Optional[bool]] = mapped_column(Boolean)
    looking_for_networking: Mapped[Optional[bool]] = mapped_column(Boolean)
    picture_path: Mapped[Optional[str]] = mapped_column(String(150))
    joined_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    current_city: Mapped[Optional[str]] = mapped_column(String(50))
    title_desc: Mapped[Optional[str]] = mapped_column(String(200))
    sport: Mapped[Optional[str]] = mapped_column(String(50))
    preferred_position: Mapped[Optional[str]] = mapped_column(String(50))
    secondary_position: Mapped[Optional[str]] = mapped_column(String(50))
    left_right_hand_foot: Mapped[Optional[str]] = mapped_column(String(30))
    height: Mapped[Optional[str]] = mapped_column(String(20))
    weight: Mapped[Optional[str]] = mapped_column(String(20))
    bio: Mapped[Optional[str]] = mapped_column(Text)


class Tbmemberprofilecontactinfo(Tbmembers):
    __tablename__ = 'tbmemberprofilecontactinfo'
    __table_args__ = (
        ForeignKeyConstraint(['member_id'], ['public.tbmembers.member_id'], name='fk_tbmemberprofilecontactinfo_tbmembers'),
        PrimaryKeyConstraint('member_id', name='tbmemberprofilecontactinfo_pkey'),
        UniqueConstraint('member_id', name='tbmemberprofilecontactinfo_member_id_key'),
        UniqueConstraint('member_id', name='tbmemberprofilecontactinfo_MemberID_key'),
        {'schema': 'public'}
    )

    member_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    email: Mapped[Optional[str]] = mapped_column(String(100))
    show_email_to_members: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(1, 0))
    other_email: Mapped[Optional[str]] = mapped_column(String(100))
    facebook: Mapped[Optional[str]] = mapped_column(String(100))
    instagram: Mapped[Optional[str]] = mapped_column(String(100))
    cell_phone: Mapped[Optional[str]] = mapped_column(String(20))
    show_cell_phone: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(1, 0))
    home_phone: Mapped[Optional[str]] = mapped_column(String(20))
    show_home_phone: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(1, 0))
    other_phone: Mapped[Optional[str]] = mapped_column(String(20))
    address: Mapped[Optional[str]] = mapped_column(String(50))
    show_address: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(1, 0))
    city: Mapped[Optional[str]] = mapped_column(String(50))
    state: Mapped[Optional[str]] = mapped_column(String(50))
    zip: Mapped[Optional[str]] = mapped_column(String(50))
    twitter: Mapped[Optional[str]] = mapped_column(String(300))
    website: Mapped[Optional[str]] = mapped_column(String(100))
    neighborhood: Mapped[Optional[str]] = mapped_column(String(50))


class Tbmemberprofilepersonalinfo(Tbmembers):
    __tablename__ = 'tbmemberprofilepersonalinfo'
    __table_args__ = (
        ForeignKeyConstraint(['member_id'], ['public.tbmembers.member_id'], name='fk_tbmemberprofilepersonalinfo_tbmembers'),
        PrimaryKeyConstraint('member_id', name='tbmemberprofilepersonalinfo_pkey'),
        UniqueConstraint('member_id', name='tbmemberprofilepersonalinfo_member_id_key'),
        UniqueConstraint('member_id', name='tbmemberprofilepersonalinfo_MemberID_key'),
        {'schema': 'public'}
    )

    member_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    activities: Mapped[Optional[str]] = mapped_column(Text)
    interests: Mapped[Optional[str]] = mapped_column(Text)
    favorite_music: Mapped[Optional[str]] = mapped_column(Text)
    favorite_tv_shows: Mapped[Optional[str]] = mapped_column(Text)
    favorite_movies: Mapped[Optional[str]] = mapped_column(Text)
    favorite_books: Mapped[Optional[str]] = mapped_column(Text)
    favorite_quotations: Mapped[Optional[str]] = mapped_column(Text)
    about_me: Mapped[Optional[str]] = mapped_column(Text)
    special_skills: Mapped[Optional[str]] = mapped_column(Text)


class Tbmembersprivacysettings(Base):
    __tablename__ = 'tbmembersprivacysettings'
    __table_args__ = (
        ForeignKeyConstraint(['member_id'], ['public.tbmembers.member_id'], name='fk_tbmemberprivacysettings_tbmembers'),
        PrimaryKeyConstraint('id', 'member_id', name='tbmembersprivacysettings_pkey'),
        {'schema': 'public'}
    )

    id: Mapped[int] = mapped_column(BigInteger, Identity(always=True, start=1, increment=1, minvalue=1, maxvalue=9223372036854775807, cycle=False, cache=1), primary_key=True)
    member_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    profile: Mapped[Optional[int]] = mapped_column(BigInteger)
    basic_info: Mapped[Optional[int]] = mapped_column(BigInteger)
    personal_info: Mapped[Optional[int]] = mapped_column(BigInteger)
    photos_tag_of_you: Mapped[Optional[int]] = mapped_column(BigInteger)
    videos_tag_of_you: Mapped[Optional[int]] = mapped_column(BigInteger)
    contact_info: Mapped[Optional[int]] = mapped_column(BigInteger)
    education: Mapped[Optional[int]] = mapped_column(BigInteger)
    work_info: Mapped[Optional[int]] = mapped_column(BigInteger)
    im_display_name: Mapped[Optional[int]] = mapped_column(BigInteger)
    mobile_phone: Mapped[Optional[int]] = mapped_column(BigInteger)
    other_phone: Mapped[Optional[int]] = mapped_column(BigInteger)
    email_address: Mapped[Optional[int]] = mapped_column(BigInteger)
    visibility: Mapped[Optional[int]] = mapped_column(BigInteger)
    view_profile_picture: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(1, 0))
    view_friends_list: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(1, 0))
    view_link_to_request_adding_you_as_friend: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(1, 0))
    view_link_to_send_you_msg: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(1, 0))

    member: Mapped['Tbmembers'] = relationship('Tbmembers', back_populates='tbmembersprivacysettings')


class Tbmembersregistered(Base):
    __tablename__ = 'tbmembersregistered'
    __table_args__ = (
        ForeignKeyConstraint(['member_id'], ['public.tbmembers.member_id'], name='fk_tbmembersregistered_tbmembers'),
        PrimaryKeyConstraint('member_code_id', 'member_id', name='tbmembersregistered_pkey'),
        UniqueConstraint('member_code_id', name='tbmembersregistered_member_code_id_key'),
        UniqueConstraint('member_code_id', name='tbmembersregistered_MemberCodeID_key'),
        {'schema': 'public'}
    )

    member_code_id: Mapped[int] = mapped_column(BigInteger, Identity(always=True, start=1, increment=1, minvalue=1, maxvalue=9223372036854775807, cycle=False, cache=1), primary_key=True)
    member_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    registered_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)

    member: Mapped['Tbmembers'] = relationship('Tbmembers', back_populates='tbmembersregistered')


class Tbmessages(Base):
    __tablename__ = 'tbmessages'
    __table_args__ = (
        ForeignKeyConstraint(['contact_id'], ['public.tbmembers.member_id'], name='fk_tbmessages_tbmembers1'),
        ForeignKeyConstraint(['sender_id'], ['public.tbmembers.member_id'], name='fk_tbmessages_tbmembers'),
        PrimaryKeyConstraint('message_id', name='tbmessages_pkey'),
        UniqueConstraint('message_id', name='tbmessages_MessageID_key'),
        UniqueConstraint('message_id', name='tbmessages_message_id_key'),
        {'schema': 'public'}
    )

    message_id: Mapped[int] = mapped_column(BigInteger, Identity(always=True, start=1, increment=1, minvalue=1, maxvalue=9223372036854775807, cycle=False, cache=1), primary_key=True)
    message_state: Mapped[int] = mapped_column(BigInteger)
    sender_id: Mapped[Optional[int]] = mapped_column(BigInteger)
    contact_id: Mapped[Optional[int]] = mapped_column(BigInteger)
    subject: Mapped[Optional[str]] = mapped_column(String(100))
    body: Mapped[Optional[str]] = mapped_column(String(500))
    msg_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    attachment: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(1, 0))
    flag_level: Mapped[Optional[int]] = mapped_column(BigInteger)
    importance_level: Mapped[Optional[int]] = mapped_column(BigInteger)
    attachment_file: Mapped[Optional[str]] = mapped_column(String(150))
    source: Mapped[Optional[str]] = mapped_column(String(50))
    original_msg: Mapped[Optional[str]] = mapped_column(String(100))

    contact: Mapped[Optional['Tbmembers']] = relationship('Tbmembers', foreign_keys=[contact_id], back_populates='tbmessages')
    sender: Mapped[Optional['Tbmembers']] = relationship('Tbmembers', foreign_keys=[sender_id], back_populates='tbmessages_')


class Tbnotificationsettings(Base):
    __tablename__ = 'tbnotificationsettings'
    __table_args__ = (
        ForeignKeyConstraint(['member_id'], ['public.tbmembers.member_id'], name='fk_tbnotificationsettings_tbmembers'),
        PrimaryKeyConstraint('id', name='tbnotificationsettings_pkey'),
        UniqueConstraint('id', name='tbnotificationsettings_ID_key'),
        UniqueConstraint('id', name='tbnotificationsettings_id_key'),
        {'schema': 'public'}
    )

    id: Mapped[int] = mapped_column(BigInteger, Identity(always=True, start=1, increment=1, minvalue=1, maxvalue=9223372036854775807, cycle=False, cache=1), primary_key=True)
    member_id: Mapped[int] = mapped_column(BigInteger)
    send_msg: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(1, 0))
    add_as_friend: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(1, 0))
    confirm_friendship_request: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(1, 0))
    poking: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(1, 0))
    confirm_friend_details: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(1, 0))
    request_to_list_as_family: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(1, 0))
    adds_friend_you_suggest: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(1, 0))
    has_birthday_comingup: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(1, 0))
    tag_In_Photo: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(1, 0))
    tag_one_of_your_photos: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(1, 0))
    tags_in_video: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(1, 0))
    tags_one_of_your_videos: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(1, 0))
    comment_on_video: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(1, 0))
    comment_on_video_of_you: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(1, 0))
    comment_after_you_in_video: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(1, 0))
    replies_to_your_help_quest: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(1, 0))

    member: Mapped['Tbmembers'] = relationship('Tbmembers', back_populates='tbnotificationsettings')


class Tbmemberpostresponses(Base):
    __tablename__ = 'tbmemberpostresponses'
    __table_args__ = (
        ForeignKeyConstraint(['member_id'], ['public.tbmembers.member_id'], name='fk_tbmemberpostresponses_tbmembers'),
        ForeignKeyConstraint(['post_id'], ['public.tbmemberposts.post_id'], name='fk_tbmemberpostresponses_tbmemberposts'),
        PrimaryKeyConstraint('post_response_id', name='tbmemberpostresponses_pkey'),
        UniqueConstraint('post_response_id', name='tbmemberpostresponses_post_response_id_key'),
        UniqueConstraint('post_response_id', name='tbmemberpostresponses_PostResponseID_key'),
        {'schema': 'public'}
    )

    post_response_id: Mapped[int] = mapped_column(BigInteger, Identity(always=True, start=1, increment=1, minvalue=1, maxvalue=9223372036854775807, cycle=False, cache=1), primary_key=True)
    post_id: Mapped[Optional[int]] = mapped_column(BigInteger)
    description: Mapped[Optional[str]] = mapped_column(String(500))
    response_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    member_id: Mapped[Optional[int]] = mapped_column(BigInteger)

    member: Mapped[Optional['Tbmembers']] = relationship('Tbmembers', back_populates='tbmemberpostresponses')
    post: Mapped[Optional['Tbmemberposts']] = relationship('Tbmemberposts', back_populates='tbmemberpostresponses')
