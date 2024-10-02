import os
import strawberry
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from strawberry.asgi import GraphQL
from pymongo import MongoClient


client = MongoClient(os.environ.get("MONGO_URL"))
db = client['management_system']
shift_collection = db['shifts']
users_collection = db['users']


app = FastAPI()

oauth2_schema = OAuth2PasswordBearer(tokenUrl="token")

origins = [
  "http://localhost:3000",
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@strawberry.type
class Shift:
    id: int
    date: str
    category: str


@strawberry.input
class ShiftRegister:
    date: str
    category: str


@strawberry.type
class User:
    name: str
    login_id: str


@strawberry.type
class Query:
    @strawberry.field
    def get_shifts(self) -> Shift:
        return Shift(id=1, date="2024-10-01", category="昼")


@strawberry.type
class Mutation:
    @strawberry.field
    def create_shift(self, shift: ShiftRegister) -> Shift:
        shift_collection.insert_one(shift.__dict__)
        return shift


schema = strawberry.Schema(query=Query, mutation=Mutation)

graphql_app = GraphQL(schema)

app.add_route("/graphql", graphql_app)


# REST APIでの実装例
# @app.get("/shifts/")
# def get_shifts():
#     response = supabase.table("shifts").select("*").execute()
#     shifts = response
#     return shifts.data
