from typing import Any, List, Optional

from sqlalchemy import Boolean, Column, DateTime, ForeignKeyConstraint, Identity, Index, Integer, LargeBinary, PrimaryKeyConstraint, REAL, String, TEXT, Table, Unicode, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.sql.sqltypes import NullType
import datetime

class Base(DeclarativeBase):
    pass


class Sysdiagrams(Base):
    __tablename__ = 'sysdiagrams'
    __table_args__ = (
        PrimaryKeyConstraint('diagram_id', name='PK__sysdiagrams__0169315C'),
        Index('UK_principal_name', 'principal_id', 'name', unique=True)
    )

    name: Mapped[str] = mapped_column(String(255))
    principal_id: Mapped[int] = mapped_column(Integer)
    diagram_id: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1), primary_key=True)
    version: Mapped[Optional[int]] = mapped_column(Integer)
    definition: Mapped[Optional[bytes]] = mapped_column(LargeBinary)


class TbAds(Base):
    __tablename__ = 'tbAds'
    __table_args__ = (
        PrimaryKeyConstraint('ID', name='PK_tbAds'),
    )

    ID: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1), primary_key=True)
    Name: Mapped[Optional[str]] = mapped_column(String(150, 'SQL_Latin1_General_CP1_CI_AS'))
    HeaderText: Mapped[Optional[str]] = mapped_column(String(150, 'SQL_Latin1_General_CP1_CI_AS'))
    PostingDate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    TextField: Mapped[Optional[str]] = mapped_column(String(2000, 'SQL_Latin1_General_CP1_CI_AS'))
    NavigateURL: Mapped[Optional[str]] = mapped_column(String(200, 'SQL_Latin1_General_CP1_CI_AS'))
    ImageUrl: Mapped[Optional[str]] = mapped_column(String(100, 'SQL_Latin1_General_CP1_CI_AS'))
    Type: Mapped[Optional[str]] = mapped_column(String(100, 'SQL_Latin1_General_CP1_CI_AS'))


class TbColleges(Base):
    __tablename__ = 'tbColleges'
    __table_args__ = (
        PrimaryKeyConstraint('SchoolID', name='PK_tbColleges'),
    )

    SchoolID: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1), primary_key=True)
    Name: Mapped[Optional[str]] = mapped_column(String(200, 'SQL_Latin1_General_CP1_CI_AS'))
    Address: Mapped[Optional[str]] = mapped_column(String(250, 'SQL_Latin1_General_CP1_CI_AS'))
    Phone: Mapped[Optional[str]] = mapped_column(String(50, 'SQL_Latin1_General_CP1_CI_AS'))
    Website: Mapped[Optional[str]] = mapped_column(String(150, 'SQL_Latin1_General_CP1_CI_AS'))
    Type: Mapped[Optional[str]] = mapped_column(String(250, 'SQL_Latin1_General_CP1_CI_AS'))
    AwardsOffered: Mapped[Optional[str]] = mapped_column(String(500, 'SQL_Latin1_General_CP1_CI_AS'))
    CampusSetting: Mapped[Optional[str]] = mapped_column(String(90, 'SQL_Latin1_General_CP1_CI_AS'))
    CampusHousing: Mapped[Optional[str]] = mapped_column(String(150, 'SQL_Latin1_General_CP1_CI_AS'))
    StudentPopulation: Mapped[Optional[int]] = mapped_column(Integer)
    UnderGradStudents: Mapped[Optional[int]] = mapped_column(Integer)
    StudentToFacultyRatio: Mapped[Optional[str]] = mapped_column(String(50, 'SQL_Latin1_General_CP1_CI_AS'))
    IPEDSID: Mapped[Optional[str]] = mapped_column(String(150, 'SQL_Latin1_General_CP1_CI_AS'))
    OPEID: Mapped[Optional[str]] = mapped_column(String(50, 'SQL_Latin1_General_CP1_CI_AS'))
    State: Mapped[Optional[str]] = mapped_column(String(10, 'SQL_Latin1_General_CP1_CI_AS'))
    ImageFile: Mapped[Optional[str]] = mapped_column(String(50, 'SQL_Latin1_General_CP1_CI_AS'))


t_tbDays = Table(
    'tbDays', Base.metadata,
    Column('Day', String(2, 'SQL_Latin1_General_CP1_CI_AS'))
)


class TbDegreeType(Base):
    __tablename__ = 'tbDegreeType'
    __table_args__ = (
        PrimaryKeyConstraint('DegreeTypeID', name='PK_tbDegreeType'),
    )

    DegreeTypeID: Mapped[int] = mapped_column(Integer, primary_key=True)
    DegreeTypeDesc: Mapped[Optional[str]] = mapped_column(String(50, 'SQL_Latin1_General_CP1_CI_AS'))


class TbForgotPwdCodes(Base):
    __tablename__ = 'tbForgotPwdCodes'
    __table_args__ = (
        PrimaryKeyConstraint('CodeID', name='PK_tbForgotPwdCodes'),
    )

    CodeID: Mapped[int] = mapped_column(Integer, Identity(start=1000, increment=1), primary_key=True)
    Email: Mapped[Optional[str]] = mapped_column(String(100, 'SQL_Latin1_General_CP1_CI_AS'))
    CodeDate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    Status: Mapped[Optional[int]] = mapped_column(Integer)


class TbInterests(Base):
    __tablename__ = 'tbInterests'
    __table_args__ = (
        PrimaryKeyConstraint('InterestID', name='PK_tbInterests'),
    )

    InterestID: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1), primary_key=True)
    InterestDesc: Mapped[Optional[str]] = mapped_column(String(150, 'SQL_Latin1_General_CP1_CI_AS'))
    InterestType: Mapped[Optional[str]] = mapped_column(String(20, 'SQL_Latin1_General_CP1_CI_AS'))


class TbMajors(Base):
    __tablename__ = 'tbMajors'
    __table_args__ = (
        PrimaryKeyConstraint('MajorID', name='PK_tbMajors'),
    )

    MajorID: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1), primary_key=True)
    MajorDesc: Mapped[Optional[str]] = mapped_column(String(100, 'SQL_Latin1_General_CP1_CI_AS'))


class TbMemberFollowing(Base):
    __tablename__ = 'tbMemberFollowing'
    __table_args__ = (
        PrimaryKeyConstraint('Id', name='PK_tbMemberFollowing'),
    )

    Id: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1), primary_key=True)
    MemberId: Mapped[Optional[int]] = mapped_column(Integer)
    FollowingMemberId: Mapped[Optional[int]] = mapped_column(Integer)


class TbMemberNotifications(Base):
    __tablename__ = 'tbMemberNotifications'
    __table_args__ = (
        PrimaryKeyConstraint('NotificationMemberID', 'MemberID', 'NotificationID', name='PK_tbMemberNotifications'),
    )

    NotificationMemberID: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1), primary_key=True)
    MemberID: Mapped[int] = mapped_column(Integer, primary_key=True)
    NotificationID: Mapped[int] = mapped_column(Integer, primary_key=True)


class TbMemberProfileEducationV2(Base):
    __tablename__ = 'tbMemberProfileEducationV2'
    __table_args__ = (
        PrimaryKeyConstraint('MemberID', 'SchoolID', 'SchoolType', name='PK_tbMemberProfileEducationV2'),
    )

    MemberID: Mapped[int] = mapped_column(Integer, primary_key=True)
    SchoolID: Mapped[int] = mapped_column(Integer, primary_key=True)
    SchoolType: Mapped[int] = mapped_column(Integer, primary_key=True, comment='1 pub, 2 priv, 3 col')
    SchoolName: Mapped[Optional[str]] = mapped_column(String(100, 'SQL_Latin1_General_CP1_CI_AS'))
    ClassYear: Mapped[Optional[str]] = mapped_column(String(10, 'SQL_Latin1_General_CP1_CI_AS'))
    Major: Mapped[Optional[str]] = mapped_column(String(100, 'SQL_Latin1_General_CP1_CI_AS'))
    DegreeType: Mapped[Optional[int]] = mapped_column(Integer)
    Societies: Mapped[Optional[str]] = mapped_column(String(300, 'SQL_Latin1_General_CP1_CI_AS'))
    Description: Mapped[Optional[str]] = mapped_column(String(200, 'SQL_Latin1_General_CP1_CI_AS'))
    SportLevelType: Mapped[Optional[str]] = mapped_column(String(20, 'SQL_Latin1_General_CP1_CI_AS'))


class TbMemberProfilePictures(Base):
    __tablename__ = 'tbMemberProfilePictures'
    __table_args__ = (
        PrimaryKeyConstraint('ProfileID', 'MemberID', name='PK_tbMemberProfilePictures'),
    )

    ProfileID: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1), primary_key=True)
    MemberID: Mapped[int] = mapped_column(Integer, primary_key=True)
    FileName: Mapped[Optional[str]] = mapped_column(String(100, 'SQL_Latin1_General_CP1_CI_AS'))
    IsDefault: Mapped[Optional[bool]] = mapped_column(Boolean)
    Removed: Mapped[Optional[bool]] = mapped_column(Boolean)


class TbMembers(Base):
    __tablename__ = 'tbMembers'
    __table_args__ = (
        PrimaryKeyConstraint('MemberID', name='PK_tbMembers'),
    )

    MemberID: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1), primary_key=True)
    Email: Mapped[Optional[str]] = mapped_column(String(100, 'SQL_Latin1_General_CP1_CI_AS'))
    Password: Mapped[Optional[str]] = mapped_column(String(50, 'SQL_Latin1_General_CP1_CI_AS'))
    Status: Mapped[Optional[int]] = mapped_column(Integer, comment='1-NewlyRegistered,2-Active, 3-InActive')
    SecurityQuestion: Mapped[Optional[int]] = mapped_column(Integer)
    SecurityAnswer: Mapped[Optional[str]] = mapped_column(String(50, 'SQL_Latin1_General_CP1_CI_AS'))
    DeactivateReason: Mapped[Optional[int]] = mapped_column(Integer)
    DeactivateExplanation: Mapped[Optional[str]] = mapped_column(String(1000, 'SQL_Latin1_General_CP1_CI_AS'))
    FutureEmails: Mapped[Optional[bool]] = mapped_column(Boolean)
    ChatStatus: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('((1))'), comment='1=available, 2=busy, 3=offline')
    LogOn: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('((0))'))
    YoutubeChannel: Mapped[Optional[str]] = mapped_column(String(100, 'SQL_Latin1_General_CP1_CI_AS'))

    tbContactRequests: Mapped[List['TbContactRequests']] = relationship('TbContactRequests', foreign_keys='[TbContactRequests.FromMemberID]', back_populates='tbMembers')
    tbContactRequests_: Mapped[List['TbContactRequests']] = relationship('TbContactRequests', foreign_keys='[TbContactRequests.ToMemberID]', back_populates='tbMembers_')
    tbContacts: Mapped[List['TbContacts']] = relationship('TbContacts', foreign_keys='[TbContacts.ContactID]', back_populates='tbMembers')
    tbContacts_: Mapped[List['TbContacts']] = relationship('TbContacts', foreign_keys='[TbContacts.MemberID]', back_populates='tbMembers_')
    tbMemberPosts: Mapped[List['TbMemberPosts']] = relationship('TbMemberPosts', back_populates='tbMembers')
    tbMembersPrivacySettings: Mapped[List['TbMembersPrivacySettings']] = relationship('TbMembersPrivacySettings', back_populates='tbMembers')
    tbMembersRecentActivities: Mapped[List['TbMembersRecentActivities']] = relationship('TbMembersRecentActivities', back_populates='tbMembers')
    tbMembersRegistered: Mapped[List['TbMembersRegistered']] = relationship('TbMembersRegistered', back_populates='tbMembers')
    tbMessages: Mapped[List['TbMessages']] = relationship('TbMessages', foreign_keys='[TbMessages.ContactID]', back_populates='tbMembers')
    tbMessages_: Mapped[List['TbMessages']] = relationship('TbMessages', foreign_keys='[TbMessages.SenderID]', back_populates='tbMembers_')
    tbMessagesSent: Mapped[List['TbMessagesSent']] = relationship('TbMessagesSent', foreign_keys='[TbMessagesSent.ContactID]', back_populates='tbMembers')
    tbMessagesSent_: Mapped[List['TbMessagesSent']] = relationship('TbMessagesSent', foreign_keys='[TbMessagesSent.SenderID]', back_populates='tbMembers_')
    tbNotificationSettings: Mapped[List['TbNotificationSettings']] = relationship('TbNotificationSettings', back_populates='tbMembers')
    tbMemberPostResponses: Mapped[List['TbMemberPostResponses']] = relationship('TbMemberPostResponses', back_populates='tbMembers')


t_tbMonths = Table(
    'tbMonths', Base.metadata,
    Column('month', String(2, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Desc', String(20, 'SQL_Latin1_General_CP1_CI_AS'))
)


class TbNotifications(Base):
    __tablename__ = 'tbNotifications'
    __table_args__ = (
        PrimaryKeyConstraint('NotificationID', name='PK_tbNotifications'),
    )

    NotificationID: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1), primary_key=True)
    Subject: Mapped[Optional[str]] = mapped_column(String(100, 'SQL_Latin1_General_CP1_CI_AS'))
    Notification: Mapped[Optional[str]] = mapped_column(String(2000, 'SQL_Latin1_General_CP1_CI_AS'))
    SentDate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    Status: Mapped[Optional[bool]] = mapped_column(Boolean)


class TbPrivateSchools(Base):
    __tablename__ = 'tbPrivateSchools'
    __table_args__ = (
        PrimaryKeyConstraint('LGId', name='PK_tbPrivateSchools'),
    )

    LGId: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1), primary_key=True)
    PSS_SCHOOL_ID: Mapped[Optional[str]] = mapped_column(Unicode(255, 'SQL_Latin1_General_CP1_CI_AS'))
    SchoolName: Mapped[Optional[str]] = mapped_column(Unicode(255, 'SQL_Latin1_General_CP1_CI_AS'))
    LoGrade: Mapped[Optional[str]] = mapped_column(Unicode(255, 'SQL_Latin1_General_CP1_CI_AS'))
    HiGrade: Mapped[Optional[str]] = mapped_column(Unicode(255, 'SQL_Latin1_General_CP1_CI_AS'))
    StreetName: Mapped[Optional[str]] = mapped_column(Unicode(255, 'SQL_Latin1_General_CP1_CI_AS'))
    City: Mapped[Optional[str]] = mapped_column(Unicode(255, 'SQL_Latin1_General_CP1_CI_AS'))
    PSS_COUNTY_NO: Mapped[Optional[str]] = mapped_column(Unicode(255, 'SQL_Latin1_General_CP1_CI_AS'))
    PSS_COUNTY_FIPS: Mapped[Optional[str]] = mapped_column(Unicode(255, 'SQL_Latin1_General_CP1_CI_AS'))
    State: Mapped[Optional[str]] = mapped_column(Unicode(255, 'SQL_Latin1_General_CP1_CI_AS'))
    PSS_FIPS: Mapped[Optional[str]] = mapped_column(Unicode(255, 'SQL_Latin1_General_CP1_CI_AS'))
    Zip: Mapped[Optional[str]] = mapped_column(Unicode(255, 'SQL_Latin1_General_CP1_CI_AS'))
    Phone: Mapped[Optional[str]] = mapped_column(Unicode(255, 'SQL_Latin1_General_CP1_CI_AS'))
    PSS_SCH_DAYS: Mapped[Optional[str]] = mapped_column(Unicode(255, 'SQL_Latin1_General_CP1_CI_AS'))
    PSS_STU_DAY_HRS: Mapped[Optional[str]] = mapped_column(Unicode(255, 'SQL_Latin1_General_CP1_CI_AS'))
    PSS_LIBRARY: Mapped[Optional[str]] = mapped_column(Unicode(255, 'SQL_Latin1_General_CP1_CI_AS'))
    PSS_ENROLL_UG: Mapped[Optional[str]] = mapped_column(Unicode(255, 'SQL_Latin1_General_CP1_CI_AS'))
    PSS_ENROLL_PK: Mapped[Optional[str]] = mapped_column(Unicode(255, 'SQL_Latin1_General_CP1_CI_AS'))
    PSS_ENROLL_K: Mapped[Optional[str]] = mapped_column(Unicode(255, 'SQL_Latin1_General_CP1_CI_AS'))
    PSS_ENROLL_1: Mapped[Optional[str]] = mapped_column(Unicode(255, 'SQL_Latin1_General_CP1_CI_AS'))
    PSS_ENROLL_2: Mapped[Optional[str]] = mapped_column(Unicode(255, 'SQL_Latin1_General_CP1_CI_AS'))
    PSS_ENROLL_3: Mapped[Optional[str]] = mapped_column(Unicode(255, 'SQL_Latin1_General_CP1_CI_AS'))
    PSS_ENROLL_4: Mapped[Optional[str]] = mapped_column(Unicode(255, 'SQL_Latin1_General_CP1_CI_AS'))
    PSS_ENROLL_5: Mapped[Optional[str]] = mapped_column(Unicode(255, 'SQL_Latin1_General_CP1_CI_AS'))
    PSS_ENROLL_6: Mapped[Optional[str]] = mapped_column(Unicode(255, 'SQL_Latin1_General_CP1_CI_AS'))
    PSS_ENROLL_7: Mapped[Optional[str]] = mapped_column(Unicode(255, 'SQL_Latin1_General_CP1_CI_AS'))
    PSS_ENROLL_8: Mapped[Optional[str]] = mapped_column(Unicode(255, 'SQL_Latin1_General_CP1_CI_AS'))
    PSS_ENROLL_9: Mapped[Optional[str]] = mapped_column(Unicode(255, 'SQL_Latin1_General_CP1_CI_AS'))
    PSS_ENROLL_10: Mapped[Optional[str]] = mapped_column(Unicode(255, 'SQL_Latin1_General_CP1_CI_AS'))
    PSS_ENROLL_11: Mapped[Optional[str]] = mapped_column(Unicode(255, 'SQL_Latin1_General_CP1_CI_AS'))
    PSS_ENROLL_12: Mapped[Optional[str]] = mapped_column(Unicode(255, 'SQL_Latin1_General_CP1_CI_AS'))
    PSS_ENROLL_T: Mapped[Optional[str]] = mapped_column(Unicode(255, 'SQL_Latin1_General_CP1_CI_AS'))
    PSS_ENROLL_TK12: Mapped[Optional[str]] = mapped_column(Unicode(255, 'SQL_Latin1_General_CP1_CI_AS'))
    PSS_RACE_AI: Mapped[Optional[str]] = mapped_column(Unicode(255, 'SQL_Latin1_General_CP1_CI_AS'))
    PSS_RACE_AS: Mapped[Optional[str]] = mapped_column(Unicode(255, 'SQL_Latin1_General_CP1_CI_AS'))
    PSS_RACE_H: Mapped[Optional[str]] = mapped_column(Unicode(255, 'SQL_Latin1_General_CP1_CI_AS'))
    PSS_RACE_B: Mapped[Optional[str]] = mapped_column(Unicode(255, 'SQL_Latin1_General_CP1_CI_AS'))
    PSS_RACE_W: Mapped[Optional[str]] = mapped_column(Unicode(255, 'SQL_Latin1_General_CP1_CI_AS'))
    PSS_RACE_P: Mapped[Optional[str]] = mapped_column(Unicode(255, 'SQL_Latin1_General_CP1_CI_AS'))
    PSS_RACE_2: Mapped[Optional[str]] = mapped_column(Unicode(255, 'SQL_Latin1_General_CP1_CI_AS'))
    PSS_FTE_TEACH: Mapped[Optional[str]] = mapped_column(Unicode(255, 'SQL_Latin1_General_CP1_CI_AS'))
    PSS_LOCALE: Mapped[Optional[str]] = mapped_column(Unicode(255, 'SQL_Latin1_General_CP1_CI_AS'))
    PSS_COED: Mapped[Optional[str]] = mapped_column(Unicode(255, 'SQL_Latin1_General_CP1_CI_AS'))
    PSS_TYPE: Mapped[Optional[str]] = mapped_column(Unicode(255, 'SQL_Latin1_General_CP1_CI_AS'))
    PSS_LEVEL: Mapped[Optional[str]] = mapped_column(Unicode(255, 'SQL_Latin1_General_CP1_CI_AS'))
    PSS_RELIG: Mapped[Optional[str]] = mapped_column(Unicode(255, 'SQL_Latin1_General_CP1_CI_AS'))
    PSS_COMM_TYPE: Mapped[Optional[str]] = mapped_column(Unicode(255, 'SQL_Latin1_General_CP1_CI_AS'))
    PSS_INDIAN_PCT: Mapped[Optional[str]] = mapped_column(Unicode(255, 'SQL_Latin1_General_CP1_CI_AS'))
    PSS_ASIAN_PCT: Mapped[Optional[str]] = mapped_column(Unicode(255, 'SQL_Latin1_General_CP1_CI_AS'))
    PSS_HISP_PCT: Mapped[Optional[str]] = mapped_column(Unicode(255, 'SQL_Latin1_General_CP1_CI_AS'))
    PSS_BLACK_PCT: Mapped[Optional[str]] = mapped_column(Unicode(255, 'SQL_Latin1_General_CP1_CI_AS'))
    PSS_WHITE_PCT: Mapped[Optional[str]] = mapped_column(Unicode(255, 'SQL_Latin1_General_CP1_CI_AS'))
    P_PACISL_PCT: Mapped[Optional[str]] = mapped_column(Unicode(255, 'SQL_Latin1_General_CP1_CI_AS'))
    P_TWOMORE_PCT: Mapped[Optional[str]] = mapped_column(Unicode(255, 'SQL_Latin1_General_CP1_CI_AS'))
    PSS_STDTCH_RT: Mapped[Optional[str]] = mapped_column(Unicode(255, 'SQL_Latin1_General_CP1_CI_AS'))
    PSS_ORIENT: Mapped[Optional[str]] = mapped_column(Unicode(255, 'SQL_Latin1_General_CP1_CI_AS'))
    County: Mapped[Optional[str]] = mapped_column(Unicode(255, 'SQL_Latin1_General_CP1_CI_AS'))
    PSS_ASSOC_1: Mapped[Optional[str]] = mapped_column(Unicode(255, 'SQL_Latin1_General_CP1_CI_AS'))
    PSS_ASSOC_2: Mapped[Optional[str]] = mapped_column(Unicode(255, 'SQL_Latin1_General_CP1_CI_AS'))
    PSS_ASSOC_3: Mapped[Optional[str]] = mapped_column(Unicode(255, 'SQL_Latin1_General_CP1_CI_AS'))
    PSS_ASSOC_4: Mapped[Optional[str]] = mapped_column(Unicode(255, 'SQL_Latin1_General_CP1_CI_AS'))
    PSS_ASSOC_5: Mapped[Optional[str]] = mapped_column(Unicode(255, 'SQL_Latin1_General_CP1_CI_AS'))
    PSS_ASSOC_6: Mapped[Optional[str]] = mapped_column(Unicode(255, 'SQL_Latin1_General_CP1_CI_AS'))
    PSS_ASSOC_7: Mapped[Optional[str]] = mapped_column(Unicode(255, 'SQL_Latin1_General_CP1_CI_AS'))
    ImageFile: Mapped[Optional[str]] = mapped_column(Unicode(255, 'SQL_Latin1_General_CP1_CI_AS'))


class TbPublicSchools(Base):
    __tablename__ = 'tbPublicSchools'
    __table_args__ = (
        PrimaryKeyConstraint('LGID', name='PK_tbPublicSchools'),
    )

    LGID: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1), primary_key=True)
    SchoolID: Mapped[Optional[str]] = mapped_column(String(50, 'SQL_Latin1_General_CP1_CI_AS'))
    StateSchoolID: Mapped[Optional[str]] = mapped_column(String(50, 'SQL_Latin1_General_CP1_CI_AS'))
    DistrictID: Mapped[Optional[str]] = mapped_column(String(50, 'SQL_Latin1_General_CP1_CI_AS'))
    StateDistrict: Mapped[Optional[str]] = mapped_column(String(100, 'SQL_Latin1_General_CP1_CI_AS'))
    LowGrade: Mapped[Optional[str]] = mapped_column(String(50, 'SQL_Latin1_General_CP1_CI_AS'))
    HighGrade: Mapped[Optional[str]] = mapped_column(String(50, 'SQL_Latin1_General_CP1_CI_AS'))
    SchoolName: Mapped[Optional[str]] = mapped_column(String(100, 'SQL_Latin1_General_CP1_CI_AS'))
    District: Mapped[Optional[str]] = mapped_column(String(100, 'SQL_Latin1_General_CP1_CI_AS'))
    CountryName: Mapped[Optional[str]] = mapped_column(String(100, 'SQL_Latin1_General_CP1_CI_AS'))
    StreetName: Mapped[Optional[str]] = mapped_column(String(100, 'SQL_Latin1_General_CP1_CI_AS'))
    City: Mapped[Optional[str]] = mapped_column(String(50, 'SQL_Latin1_General_CP1_CI_AS'))
    State: Mapped[Optional[str]] = mapped_column(String(20, 'SQL_Latin1_General_CP1_CI_AS'))
    Zip: Mapped[Optional[str]] = mapped_column(String(10, 'SQL_Latin1_General_CP1_CI_AS'))
    Zip4Digit: Mapped[Optional[str]] = mapped_column(String(4, 'SQL_Latin1_General_CP1_CI_AS'))
    Phone: Mapped[Optional[str]] = mapped_column(String(20, 'SQL_Latin1_General_CP1_CI_AS'))
    localCode: Mapped[Optional[str]] = mapped_column(String(50, 'SQL_Latin1_General_CP1_CI_AS'))
    locale: Mapped[Optional[str]] = mapped_column(String(50, 'SQL_Latin1_General_CP1_CI_AS'))
    Charter: Mapped[Optional[str]] = mapped_column(String(50, 'SQL_Latin1_General_CP1_CI_AS'))
    Magnet: Mapped[Optional[str]] = mapped_column(String(50, 'SQL_Latin1_General_CP1_CI_AS'))
    Titlle1School: Mapped[Optional[str]] = mapped_column(String(50, 'SQL_Latin1_General_CP1_CI_AS'))
    Title1SchoolWide: Mapped[Optional[str]] = mapped_column(String(50, 'SQL_Latin1_General_CP1_CI_AS'))
    Students: Mapped[Optional[int]] = mapped_column(Integer)
    Teachers: Mapped[Optional[int]] = mapped_column(Integer)
    StudeintTeacherRatio: Mapped[Optional[float]] = mapped_column(REAL(24))
    FreeLunch: Mapped[Optional[int]] = mapped_column(Integer)
    ReducedLunch: Mapped[Optional[int]] = mapped_column(Integer)
    ImageFile: Mapped[Optional[str]] = mapped_column(String(70, 'SQL_Latin1_General_CP1_CI_AS'))


class TbRecentNews(Base):
    __tablename__ = 'tbRecentNews'
    __table_args__ = (
        PrimaryKeyConstraint('ID', name='PK_tbRecentNews'),
    )

    ID: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1), primary_key=True)
    Name: Mapped[Optional[str]] = mapped_column(String(150, 'SQL_Latin1_General_CP1_CI_AS'))
    HeaderText: Mapped[Optional[str]] = mapped_column(String(150, 'SQL_Latin1_General_CP1_CI_AS'))
    PostingDate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    TextField: Mapped[Optional[str]] = mapped_column(String(2000, 'SQL_Latin1_General_CP1_CI_AS'))
    NavigateURL: Mapped[Optional[str]] = mapped_column(String(200, 'SQL_Latin1_General_CP1_CI_AS'))
    ImageUrl: Mapped[Optional[str]] = mapped_column(String(100, 'SQL_Latin1_General_CP1_CI_AS'))


class TbSchoolType(Base):
    __tablename__ = 'tbSchoolType'
    __table_args__ = (
        PrimaryKeyConstraint('SchoolTypeID', name='PK_tbSchoolType'),
    )

    SchoolTypeID: Mapped[int] = mapped_column(Integer, primary_key=True)
    SchoolTypeDesc: Mapped[Optional[str]] = mapped_column(String(50, 'SQL_Latin1_General_CP1_CI_AS'))


class TbSports(Base):
    __tablename__ = 'tbSports'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='PK_tbSports'),
    )

    id: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1), primary_key=True)
    Name: Mapped[Optional[str]] = mapped_column(String(50, 'SQL_Latin1_General_CP1_CI_AS'))


class TbStates(Base):
    __tablename__ = 'tbStates'
    __table_args__ = (
        PrimaryKeyConstraint('StateID', name='PK_tbStates'),
    )

    StateID: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1), primary_key=True)
    Name: Mapped[Optional[str]] = mapped_column(String(50, 'SQL_Latin1_General_CP1_CI_AS'))
    Abbreviation: Mapped[Optional[str]] = mapped_column(String(5, 'SQL_Latin1_General_CP1_CI_AS'))


t_tbYears = Table(
    'tbYears', Base.metadata,
    Column('Year', String(4, 'SQL_Latin1_General_CP1_CI_AS'))
)


class TbContactRequests(Base):
    __tablename__ = 'tbContactRequests'
    __table_args__ = (
        ForeignKeyConstraint(['FromMemberID'], ['tbMembers.MemberID'], name='FK_tbContactRequests_tbMembers'),
        ForeignKeyConstraint(['ToMemberID'], ['tbMembers.MemberID'], name='FK_tbContactRequests_tbMembers1'),
        PrimaryKeyConstraint('RequestID', name='PK_tbFriendRequests')
    )

    RequestID: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1), primary_key=True)
    FromMemberID: Mapped[Optional[int]] = mapped_column(Integer)
    ToMemberID: Mapped[Optional[int]] = mapped_column(Integer, comment='0-waiting, 1-accepted, 2-rejected')
    RequestDate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('(getdate())'))
    Status: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('((0))'))

    tbMembers: Mapped[Optional['TbMembers']] = relationship('TbMembers', foreign_keys=[FromMemberID], back_populates='tbContactRequests')
    tbMembers_: Mapped[Optional['TbMembers']] = relationship('TbMembers', foreign_keys=[ToMemberID], back_populates='tbContactRequests_')


class TbContacts(Base):
    __tablename__ = 'tbContacts'
    __table_args__ = (
        ForeignKeyConstraint(['ContactID'], ['tbMembers.MemberID'], name='FK_tbContacts_tbMembers1'),
        ForeignKeyConstraint(['MemberID'], ['tbMembers.MemberID'], name='FK_tbContacts_tbMembers'),
        PrimaryKeyConstraint('MemberID', 'ContactID', name='PK_tbFriends')
    )

    MemberID: Mapped[int] = mapped_column(Integer, primary_key=True)
    ContactID: Mapped[int] = mapped_column(Integer, primary_key=True)
    Status: Mapped[int] = mapped_column(Integer, server_default=text('((0))'), comment=' status (rejected=2, accepted=1, deleted=3, requested=0)')
    DateStamp: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('(getdate())'))

    tbMembers: Mapped['TbMembers'] = relationship('TbMembers', foreign_keys=[ContactID], back_populates='tbContacts')
    tbMembers_: Mapped['TbMembers'] = relationship('TbMembers', foreign_keys=[MemberID], back_populates='tbContacts_')


class TbMemberPosts(Base):
    __tablename__ = 'tbMemberPosts'
    __table_args__ = (
        ForeignKeyConstraint(['MemberID'], ['tbMembers.MemberID'], name='FK_tbMemberPosts_tbMembers'),
        PrimaryKeyConstraint('PostID', name='PK_tbPosts')
    )

    PostID: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1), primary_key=True)
    Title: Mapped[Optional[str]] = mapped_column(String(100, 'SQL_Latin1_General_CP1_CI_AS'))
    Description: Mapped[Optional[str]] = mapped_column(String(700, 'SQL_Latin1_General_CP1_CI_AS'))
    PostDate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    AttachFile: Mapped[Optional[str]] = mapped_column(String(100, 'SQL_Latin1_General_CP1_CI_AS'))
    MemberID: Mapped[Optional[int]] = mapped_column(Integer)
    FileType: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('((0))'), comment='1-photo, 2-video, 3-liink')
    LikeCounter: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('((0))'))

    tbMembers: Mapped[Optional['TbMembers']] = relationship('TbMembers', back_populates='tbMemberPosts')
    tbMemberPostResponses: Mapped[List['TbMemberPostResponses']] = relationship('TbMemberPostResponses', back_populates='tbMemberPosts')


class TbMemberProfiles(TbMembers):
    __tablename__ = 'tbMemberProfile'
    __table_args__ = (
        ForeignKeyConstraint(['MemberID'], ['tbMembers.MemberID'], name='FK_tbMemberProfile_tbMembers'),
        PrimaryKeyConstraint('MemberID', name='PK_tbMemberProfiles')
    )

    MemberID: Mapped[int] = mapped_column(Integer, primary_key=True)
    FirstName: Mapped[Optional[str]] = mapped_column(String(50, 'SQL_Latin1_General_CP1_CI_AS'))
    MiddleName: Mapped[Optional[str]] = mapped_column(String(50, 'SQL_Latin1_General_CP1_CI_AS'))
    LastName: Mapped[Optional[str]] = mapped_column(String(50, 'SQL_Latin1_General_CP1_CI_AS'))
    Sex: Mapped[Optional[str]] = mapped_column(String(20, 'SQL_Latin1_General_CP1_CI_AS'))
    ShowSexInProfile: Mapped[Optional[bool]] = mapped_column(Boolean)
    DOBMonth: Mapped[Optional[str]] = mapped_column(String(3, 'SQL_Latin1_General_CP1_CI_AS'))
    DOBDay: Mapped[Optional[str]] = mapped_column(String(3, 'SQL_Latin1_General_CP1_CI_AS'))
    DOBYear: Mapped[Optional[str]] = mapped_column(String(5, 'SQL_Latin1_General_CP1_CI_AS'))
    ShowDOBType: Mapped[Optional[bool]] = mapped_column(Boolean)
    Hometown: Mapped[Optional[str]] = mapped_column(String(50, 'SQL_Latin1_General_CP1_CI_AS'))
    HomeNeighborhood: Mapped[Optional[str]] = mapped_column(String(50, 'SQL_Latin1_General_CP1_CI_AS'))
    CurrentStatus: Mapped[Optional[str]] = mapped_column(String(50, 'SQL_Latin1_General_CP1_CI_AS'))
    InterestedInType: Mapped[Optional[int]] = mapped_column(Integer)
    LookingForEmployment: Mapped[Optional[bool]] = mapped_column(Boolean)
    LookingForRecruitment: Mapped[Optional[bool]] = mapped_column(Boolean)
    LookingForPartnership: Mapped[Optional[bool]] = mapped_column(Boolean)
    LookingForNetworking: Mapped[Optional[bool]] = mapped_column(Boolean)
    PicturePath: Mapped[Optional[str]] = mapped_column(String(150, 'SQL_Latin1_General_CP1_CI_AS'))
    JoinedDate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    CurrentCity: Mapped[Optional[str]] = mapped_column(String(50, 'SQL_Latin1_General_CP1_CI_AS'))
    TitleDesc: Mapped[Optional[str]] = mapped_column(String(200, 'SQL_Latin1_General_CP1_CI_AS'), server_default=text("('')"))
    Sport: Mapped[Optional[str]] = mapped_column(String(50, 'SQL_Latin1_General_CP1_CI_AS'))
    PreferredPosition: Mapped[Optional[str]] = mapped_column(String(50, 'SQL_Latin1_General_CP1_CI_AS'))
    SecondaryPosition: Mapped[Optional[str]] = mapped_column(String(50, 'SQL_Latin1_General_CP1_CI_AS'))
    LeftRightHandFoot: Mapped[Optional[str]] = mapped_column(String(30, 'SQL_Latin1_General_CP1_CI_AS'))
    Height: Mapped[Optional[str]] = mapped_column(String(20, 'SQL_Latin1_General_CP1_CI_AS'))
    Weight: Mapped[Optional[str]] = mapped_column(String(20, 'SQL_Latin1_General_CP1_CI_AS'))
    Bio: Mapped[Optional[str]] = mapped_column(TEXT(16, 'SQL_Latin1_General_CP1_CI_AS'))


class TbMemberProfileContactInfo(Base):
    __tablename__ = 'tbMemberProfileContactInfo'
    __table_args__ = (
        ForeignKeyConstraint(['MemberID'], ['tbMembers.MemberID'], name='FK_tbMemberProfileContactInfo_tbMembers'),
        PrimaryKeyConstraint('MemberID', name='PK_tbMemberProfileContactInfo')
    )

    MemberID: Mapped[int] = mapped_column(Integer, primary_key=True)
    Email: Mapped[Optional[str]] = mapped_column(String(100, 'SQL_Latin1_General_CP1_CI_AS'))
    ShowEmailToMembers: Mapped[Optional[bool]] = mapped_column(Boolean)
    OtherEmail: Mapped[Optional[str]] = mapped_column(String(100, 'SQL_Latin1_General_CP1_CI_AS'))
    Facebook: Mapped[Optional[str]] = mapped_column(String(100, 'SQL_Latin1_General_CP1_CI_AS'))
    Instagram: Mapped[Optional[str]] = mapped_column(String(100, 'SQL_Latin1_General_CP1_CI_AS'))
    CellPhone: Mapped[Optional[str]] = mapped_column(String(20, 'SQL_Latin1_General_CP1_CI_AS'))
    ShowCellPhone: Mapped[Optional[bool]] = mapped_column(Boolean)
    HomePhone: Mapped[Optional[str]] = mapped_column(String(20, 'SQL_Latin1_General_CP1_CI_AS'))
    ShowHomePhone: Mapped[Optional[bool]] = mapped_column(Boolean)
    OtherPhone: Mapped[Optional[str]] = mapped_column(String(20, 'SQL_Latin1_General_CP1_CI_AS'))
    Address: Mapped[Optional[str]] = mapped_column(String(50, 'SQL_Latin1_General_CP1_CI_AS'))
    ShowAddress: Mapped[Optional[bool]] = mapped_column(Boolean)
    City: Mapped[Optional[str]] = mapped_column(String(50, 'SQL_Latin1_General_CP1_CI_AS'))
    State: Mapped[Optional[str]] = mapped_column(String(50, 'SQL_Latin1_General_CP1_CI_AS'))
    Zip: Mapped[Optional[str]] = mapped_column(String(50, 'SQL_Latin1_General_CP1_CI_AS'))
    Twitter: Mapped[Optional[str]] = mapped_column(String(300, 'SQL_Latin1_General_CP1_CI_AS'))
    Website: Mapped[Optional[str]] = mapped_column(String(100, 'SQL_Latin1_General_CP1_CI_AS'))
    Neighborhood: Mapped[Optional[str]] = mapped_column(String(50, 'SQL_Latin1_General_CP1_CI_AS'))


class TbMemberProfilePersonalInfo(TbMembers):
    __tablename__ = 'tbMemberProfilePersonalInfo'
    __table_args__ = (
        ForeignKeyConstraint(['MemberID'], ['tbMembers.MemberID'], name='FK_tbMemberProfilePersonalInfo_tbMembers'),
        PrimaryKeyConstraint('MemberID', name='PK_tbMemberProfilePersonalInfo')
    )

    MemberID: Mapped[int] = mapped_column(Integer, primary_key=True)
    Activities: Mapped[Optional[str]] = mapped_column(TEXT(16, 'SQL_Latin1_General_CP1_CI_AS'))
    Interests: Mapped[Optional[str]] = mapped_column(TEXT(16, 'SQL_Latin1_General_CP1_CI_AS'))
    FavoriteMusic: Mapped[Optional[str]] = mapped_column(TEXT(16, 'SQL_Latin1_General_CP1_CI_AS'))
    FavoriteTVShows: Mapped[Optional[str]] = mapped_column(TEXT(16, 'SQL_Latin1_General_CP1_CI_AS'))
    FavoriteMovies: Mapped[Optional[str]] = mapped_column(TEXT(16, 'SQL_Latin1_General_CP1_CI_AS'))
    FavoriteBooks: Mapped[Optional[str]] = mapped_column(TEXT(16, 'SQL_Latin1_General_CP1_CI_AS'))
    FavoriteQuotations: Mapped[Optional[str]] = mapped_column(TEXT(16, 'SQL_Latin1_General_CP1_CI_AS'))
    AboutMe: Mapped[Optional[str]] = mapped_column(TEXT(16, 'SQL_Latin1_General_CP1_CI_AS'))
    SpecialSkills: Mapped[Optional[str]] = mapped_column(TEXT(16, 'SQL_Latin1_General_CP1_CI_AS'))


class TbMembersPrivacySettings(Base):
    __tablename__ = 'tbMembersPrivacySettings'
    __table_args__ = (
        ForeignKeyConstraint(['MemberID'], ['tbMembers.MemberID'], name='FK_tbMembersPrivacySettings_tbMembers'),
        PrimaryKeyConstraint('ID', 'MemberID', name='PK_tbApplicationSettings')
    )

    ID: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1), primary_key=True)
    MemberID: Mapped[int] = mapped_column(Integer, primary_key=True)
    Profile: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('((3))'), comment='1-everyone, 2-friends of firends, 3- only friends, 4-only you')
    BasicInfo: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('((3))'))
    PersonalInfo: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('((3))'))
    PhotosTagOfYou: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('((3))'))
    VideosTagOfYou: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('((3))'))
    ContactInfo: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('((3))'))
    Education: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('((3))'))
    WorkInfo: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('((3))'))
    IMDisplayName: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('((3))'))
    MobilePhone: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('((3))'))
    OtherPhone: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('((3))'))
    EmailAddress: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('((3))'))
    Visibility: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('((1))'))
    ViewProfilePicture: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('((1))'))
    ViewFriendsList: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('((1))'))
    ViewLinkToRequestAddingYouAsFriend: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('((1))'))
    ViewLinkToSendYouMsg: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('((1))'))

    tbMembers: Mapped['TbMembers'] = relationship('TbMembers', back_populates='tbMembersPrivacySettings')


class TbMembersRecentActivities(Base):
    __tablename__ = 'tbMembersRecentActivities'
    __table_args__ = (
        ForeignKeyConstraint(['MemberID'], ['tbMembers.MemberID'], name='FK_tbMembersRecentActivities_tbMembers'),
        PrimaryKeyConstraint('ActivityID', name='PK_tbRecentActivities')
    )

    ActivityID: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1), primary_key=True)
    Description: Mapped[Optional[str]] = mapped_column(String(200, 'SQL_Latin1_General_CP1_CI_AS'))
    ActivityDate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    MemberID: Mapped[Optional[int]] = mapped_column(Integer)
    ActivityTypeID: Mapped[Optional[int]] = mapped_column(Integer)

    tbMembers: Mapped[Optional['TbMembers']] = relationship('TbMembers', back_populates='tbMembersRecentActivities')


class TbMembersRegistered(Base):
    __tablename__ = 'tbMembersRegistered'
    __table_args__ = (
        ForeignKeyConstraint(['MemberID'], ['tbMembers.MemberID'], name='FK_tbMembersRegistered_tbMembers'),
        PrimaryKeyConstraint('MemberCodeID', 'MemberID', name='PK_tbRegisteredMembers')
    )

    MemberCodeID: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1), primary_key=True)
    MemberID: Mapped[int] = mapped_column(Integer, primary_key=True)
    RegisteredDate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)

    tbMembers: Mapped['TbMembers'] = relationship('TbMembers', back_populates='tbMembersRegistered')


class TbMessages(Base):
    __tablename__ = 'tbMessages'
    __table_args__ = (
        ForeignKeyConstraint(['ContactID'], ['tbMembers.MemberID'], name='FK_tbMessages_tbMembers1'),
        ForeignKeyConstraint(['SenderID'], ['tbMembers.MemberID'], name='FK_tbMessages_tbMembers'),
        PrimaryKeyConstraint('MessageID', name='PK_tbMessages')
    )

    MessageID: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1), primary_key=True)
    MessageState: Mapped[int] = mapped_column(Integer)
    SenderID: Mapped[Optional[int]] = mapped_column(Integer)
    ContactID: Mapped[Optional[int]] = mapped_column(Integer)
    Subject: Mapped[Optional[str]] = mapped_column(String(100, 'SQL_Latin1_General_CP1_CI_AS'))
    Body: Mapped[Optional[str]] = mapped_column(String(500, 'SQL_Latin1_General_CP1_CI_AS'))
    MsgDate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    Attachment: Mapped[Optional[bool]] = mapped_column(Boolean)
    FlagLevel: Mapped[Optional[int]] = mapped_column(Integer)
    ImportanceLevel: Mapped[Optional[int]] = mapped_column(Integer)
    AttachmentFile: Mapped[Optional[str]] = mapped_column(String(150, 'SQL_Latin1_General_CP1_CI_AS'))
    Source: Mapped[Optional[str]] = mapped_column(String(50, 'SQL_Latin1_General_CP1_CI_AS'))
    OriginalMsg: Mapped[Optional[str]] = mapped_column(String(collation='SQL_Latin1_General_CP1_CI_AS'))

    tbMembers: Mapped[Optional['TbMembers']] = relationship('TbMembers', foreign_keys=[ContactID], back_populates='tbMessages')
    tbMembers_: Mapped[Optional['TbMembers']] = relationship('TbMembers', foreign_keys=[SenderID], back_populates='tbMessages_')


class TbMessagesSent(Base):
    __tablename__ = 'tbMessagesSent'
    __table_args__ = (
        ForeignKeyConstraint(['ContactID'], ['tbMembers.MemberID'], name='FK_tbMessagesSent_tbMembers1'),
        ForeignKeyConstraint(['SenderID'], ['tbMembers.MemberID'], name='FK_tbMessagesSent_tbMembers'),
        PrimaryKeyConstraint('MessageID', name='PK_tbSentMessages')
    )

    MessageID: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1), primary_key=True)
    SenderID: Mapped[Optional[int]] = mapped_column(Integer)
    ContactID: Mapped[Optional[int]] = mapped_column(Integer)
    Subject: Mapped[Optional[str]] = mapped_column(String(100, 'SQL_Latin1_General_CP1_CI_AS'))
    Body: Mapped[Optional[str]] = mapped_column(String(500, 'SQL_Latin1_General_CP1_CI_AS'))
    MsgDate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    Attachment: Mapped[Optional[bool]] = mapped_column(Boolean)
    MessageState: Mapped[Optional[int]] = mapped_column(Integer)
    FlagLevel: Mapped[Optional[int]] = mapped_column(Integer)
    ImportanceLevel: Mapped[Optional[int]] = mapped_column(Integer)
    AttachmentFile: Mapped[Optional[str]] = mapped_column(String(150, 'SQL_Latin1_General_CP1_CI_AS'))
    Source: Mapped[Optional[str]] = mapped_column(String(50, 'SQL_Latin1_General_CP1_CI_AS'))
    OriginalMsg: Mapped[Optional[str]] = mapped_column(String(collation='SQL_Latin1_General_CP1_CI_AS'))

    tbMembers: Mapped[Optional['TbMembers']] = relationship('TbMembers', foreign_keys=[ContactID], back_populates='tbMessagesSent')
    tbMembers_: Mapped[Optional['TbMembers']] = relationship('TbMembers', foreign_keys=[SenderID], back_populates='tbMessagesSent_')


class TbNotificationSettings(Base):
    __tablename__ = 'tbNotificationSettings'
    __table_args__ = (
        ForeignKeyConstraint(['MemberID'], ['tbMembers.MemberID'], name='FK_tbNotificationSettings_tbMembers'),
        PrimaryKeyConstraint('ID', 'MemberID', name='PK_tbNotificationSettings')
    )

    ID: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1), primary_key=True)
    MemberID: Mapped[int] = mapped_column(Integer, primary_key=True)
    LG_SendMsg: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('((1))'))
    LG_AddAsFriend: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('((1))'))
    LG_ConfirmFriendShipRequest: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('((1))'))
    LG_Poking: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('((0))'))
    LG_ConfirmFriendDetails: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('((1))'))
    LG_RequestToListAsFamily: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('((1))'))
    LG_AddsFriendYouSuggest: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('((1))'))
    LG_HasBirthDayComingUp: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('((0))'))
    PH_TagInPhoto: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('((1))'))
    PH_TagOneOfYourPhotos: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('((1))'))
    VI_TagsInVideo: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('((1))'))
    VI_TagsOneOfYourVideos: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('((1))'))
    VI_CommentOnVideo: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('((1))'))
    VI_CommentOnVideoOfYou: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('((1))'))
    VI_CommentAfterYouInVideo: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('((1))'))
    GP_InviteYouToJoin: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('((1))'))
    GP_PromoteToAdmin: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('((1))'))
    GP_MakesYouAGPAdmin: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('((1))'))
    GP_RequestToJoinGPYouAdmin: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('((1))'))
    GP_RepliesToYourDiscBooardPost: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('((1))'))
    GP_ChangesTheNameOfGroupYouBelong: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('((1))'))
    EV_InviteToEvent: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('((1))'))
    EV_DateChanged: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('((1))'))
    EV_MakeYouEventAdmin: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('((1))'))
    EV_RequestToJoinEventYouAdmin: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('((1))'))
    NO_TagsYouInNote: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('((1))'))
    NO_CommentYourNotes: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('((1))'))
    NO_CommentAfterYouInNote: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('((1))'))
    GI_SendYouGift: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('((1))'))
    HE_RepliesToYourHelpQuest: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('((1))'))

    tbMembers: Mapped['TbMembers'] = relationship('TbMembers', back_populates='tbNotificationSettings')


class TbMemberPostResponses(Base):
    __tablename__ = 'tbMemberPostResponses'
    __table_args__ = (
        ForeignKeyConstraint(['MemberID'], ['tbMembers.MemberID'], name='FK_tbMemberPostResponses_tbMembers'),
        ForeignKeyConstraint(['PostID'], ['tbMemberPosts.PostID'], name='FK_tbMemberPostResponses_tbMemberPosts'),
        PrimaryKeyConstraint('PostResponseID', name='PK_tbPostResponses')
    )

    PostResponseID: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1), primary_key=True)
    PostID: Mapped[Optional[int]] = mapped_column(Integer)
    Description: Mapped[Optional[str]] = mapped_column(String(500, 'SQL_Latin1_General_CP1_CI_AS'))
    ResponseDate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    MemberID: Mapped[Optional[int]] = mapped_column(Integer)

    tbMembers: Mapped[Optional['TbMembers']] = relationship('TbMembers', back_populates='tbMemberPostResponses')
    tbMemberPosts: Mapped[Optional['TbMemberPosts']] = relationship('TbMemberPosts', back_populates='tbMemberPostResponses')
