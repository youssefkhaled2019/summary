
from pydantic import   BaseModel,Field,EmailStr,field_validator ,HttpUrl,computed_field,ConfigDict,field_validator,field_serializer,model_validator

from typing import Optional,List,Dict,Set,Union,Literal
from uuid import UUID
from enum import Enum
from datetime import date
from datetime import datetime
from decimal import Decimal
from typing import Annotated


class UserRole(str, Enum):
    admin = "admin"
    user = "user"
    moderator = "moderator"

class Address(BaseModel):
    city: str
    street: str

class User(BaseModel):
    Age = Annotated[int, Field(gt=0, lt=120)]  # Python و FastAPI.  الأسلوب الحديث في 

    name: str
    age: int = Field(gt=0, lt=100)
    username: str = Field(min_length=3) #Validation   
    email: EmailStr
    is_active: bool = False
    price1: float
    price2: Decimal
    id: UUID
  
    start_date: date
    created_at: datetime
    email: EmailStr
    
    bio: Optional[str] = None
    address: Optional[Address]= None
    agex: int | None = None

    skills: List[str]      #    skills=["Python", "FastAPI"]
    settings: Dict[str, str] #{"theme": "dark","lang": "ar"}
    data: Dict[str, List[str]]  #   "skills": ["Python", "FastAPI"]
    tags: Set[str]           #{'python', 'ai'}
    id: Union[int, str]

    role: Literal["admin","user","moderator"]
    role: UserRole

    url: HttpUrl
    # ItemResponse
    model_config = ConfigDict(from_attributes=True)  #<-------- orm to json
    model_config = ConfigDict(extra="forbid") # الزياده لو أرسلت حقولًا إضافية سيظهر خطأ.   
    
    class Config:
        from_attributes = True
    
    @field_serializer("created_at")
    def serialize_date(self, value):
        return value.strftime("%Y-%m-%d")
    
    @computed_field
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    @field_validator("name")
    @classmethod
    def validate_name(cls, value):
        if len(value) < 3:
            raise ValueError("Name too short")
        return value
    
    password: str
    confirm_password: str
    @model_validator(mode="after")
    def passwords_match(self):
        if self.password != self.confirm_password:
            raise ValueError("Passwords do not match")
        return self


class Profile(BaseModel):
    bio: str
    city: str

class User(BaseModel):
    username: str
    profile: Profile


class User(BaseModel):
    name: str
    age: int
    address: Optional[Dict[str, str]] = Field(default_factory=lambda: { "name": "Youssef", "city": "Luxor"})


class ItemUpdate(BaseModel):
    title: str | None = None
    description: str | None = None

"""
age: int = Field( gt=0,lt=100)
first_name: str = Field(alias="firstName")  
phone: str = Field(pattern=r"^01[0-9]{9}$")
username: str = Field(min_length=3,max_length=20)

| Constraint | المعنى        |
| ---------- | ------------- |
| min_length | أقل عدد حروف  |
| max_length | أكبر عدد حروف |
| gt         | أكبر من       |
| lt         | أقل من        |
| ge         | أكبر أو يساوي |
| le         | أقل أو يساوي  |

"""
#  ValidationError   # 
# =======================
class User(BaseModel):
    name: str
    age: int

user = User(name="Ahmed",age=25)

print(user.model_dump())
print(user.model_dump_json())
user.model_dump(exclude={"age"})
user.model_dump( include={"name"})
update_data = data.model_dump(exclude_unset=True)  # 1. خذ البيانات النظيفة فقط
new_item = Item(**update_data)

# 3. احفظ في الداتابيز
db.add(new_item)
db.commit()
db.refresh(new_item)

data = item.model_dump(exclude={"user"})
new_item = Item(**data)

user = User.model_validate(data)
new_user = user.model_copy()
new_user = user.model_copy(update={"age": 30})



"""
new_item = Item(**item.model_dump())

---- servese
user.model_dump(exclude_unset=True)
user.model_dump(exclude={"extra"})
----
data = user.model_dump(exclude_unset=True)

new_user = User(**data)
"""





# =======================
# تستخدم لقراءة متغيرات البيئة (.env).
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    secret_key: str

    # settings = Settings()