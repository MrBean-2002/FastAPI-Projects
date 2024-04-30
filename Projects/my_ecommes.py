from fastapi import APIRouter,Query
from uuid import UUID
from pydantic import BaseModel,HttpUrl,Field
from typing import Annotated

router=APIRouter()

class User(BaseModel):
    first_name: str =Field(max_length=20,description='Can not be more than 20 characters')
    last_name: str =Field(max_length=20,description='Can not be more than 20 characters')
    email: str = Field(pattern='^[a-z0-9]@[a-z].com$')
    age: int = Field(ge=18,description='The working age is form 18 and above below 18 is prohibited')
    password: str = Field(min_length=8,
                          pattern='[a-zA-Z0-9\$\_\%\@\#\*\?\&\!]',
                          description='Should be a minimum of 8 characters and must contain Upper and lower cases with numbers and symbols[%,$,#,@,!,&,*,?]')

class Product (BaseModel):
    user: list[User]
    userId: UUID
    productId:UUID
    productName: str
    productPrice: float
    imageUrl: HttpUrl
    
@router.post('/auth/register')
async def create_register(user: User):
    return user

@router.post('/auth/login/')
async def call_login(email: Annotated[str,Query(pattern='^[a-z0-9][@][a-z].com$')],
                     password: Annotated[str,Query(
                            min_length=8,
                            pattern='[a-zA-Z0-9\$\_\%\@\#\*\?\&\!]',
                            description='Should be a minimum of 8 characters and must contain Upper and lower cases with numbers and symbols[%,$,#,@,!,&,*,?]')]):
    if (email is User.email) and (password is User.password):
        return {'email':email,'password':password}
    else:
        return {'Details':'Not Found'}

@router.post('/product')
async def create_product(product: Product):
    return product

@router.get('/product/get/{productId}')
async def read_product(productId:int,product:Product):
    if productId is product.productId:
        return product
    else:
        return {'product':'Not Found'}

@router.patch('/product/')
async def update_product(productId:int,product:Product):
    item_dict=product.dict()
    if productId is product.productId:
        item_dict.update({'productName':product.productName,
                          'productPrice':product.productPrice})
        return item_dict
    else:
        return {'Details':'Product not Found'}
        
        
@router.delete('/product/delete/{productId}')
async def del_product(productId: int,product:Product):
    if productId in product:
        del product
        return product
    else:
        return {'Product':"Can't be Found"}
