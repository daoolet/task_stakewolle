from attrs import define


@define
class UserCreate:
    email: str
    password: str