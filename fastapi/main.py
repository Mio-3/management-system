import os
import strawberry
from supabase import create_client, Client
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from strawberry.asgi import GraphQL


url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)
app = FastAPI()


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
    id: str
    date: str
    category: str
    employee_id: str


@strawberry.type
class Query:
    @strawberry.field
    async def get_shifts(self) -> list[Shift]:
        response = supabase.table("shifts").select("*").execute()
        shifts_data = response.data

        return [
            Shift(
                id=shift['id'],
                date=shift['date'],
                category=shift['category'],
                employee_id=shift['employee_id']
            )
            for shift in shifts_data
        ]


schema = strawberry.Schema(query=Query)

graphql_app = GraphQL(schema)

app.add_route("/graphql", graphql_app)


# REST APIでの実装例
# @app.get("/shifts/")
# def get_shifts():
#     response = supabase.table("shifts").select("*").execute()
#     shifts = response
#     return shifts.data
