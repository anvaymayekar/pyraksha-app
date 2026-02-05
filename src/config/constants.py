from enum import Enum


class SOSStatus(Enum):
    IDLE = "idle"
    ACTIVE = "active"
    RESOLVED = "resolved"


class ComplaintStatus(Enum):
    PENDING = "pending"
    UNDER_REVIEW = "under_review"
    RESOLVED = "resolved"
    CLOSED = "closed"


class ScreenNames:
    SPLASH = "splash"
    LOGIN = "login"
    REGISTER = "register"
    HOME = "home"
    SOS = "sos"
    COMPLAINT = "complaint"
    COMPLAINT_LIST = "complaint_list"
    PROFILE = "profile"
