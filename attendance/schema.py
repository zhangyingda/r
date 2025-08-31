# attendance/schema.py
import graphene
from attendance import queries, mutations

schema = graphene.Schema(query=queries.Query, mutation=mutations.Mutation)