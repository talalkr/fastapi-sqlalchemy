from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter

from .database import async_session
from api.schema import schema


async def get_context() -> dict:
    async with async_session() as session:
        async with session.begin():
            yield {"session": session}


graphql_app = GraphQLRouter(schema, context_getter=get_context)

app = FastAPI()
app.include_router(graphql_app, prefix="/graphql")
