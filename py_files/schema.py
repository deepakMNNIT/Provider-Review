from py_files.models import Provider_Review as Provider_ReviewModel
from py_files.models import Provider as ProviderModel
from py_files.database import db_session as db
import graphene
from graphene import relay, Int
from graphene_sqlalchemy import SQLAlchemyConnectionField, SQLAlchemyObjectType


class Provider_Review(SQLAlchemyObjectType):
    class Meta:
        model = Provider_ReviewModel
        interfaces = (relay.Node, )


class Provider(SQLAlchemyObjectType):
    class Meta:
        model = ProviderModel
        interfaces = (relay.Node, )


class Query(graphene.ObjectType):
    node = relay.Node.Field()
    # if you don't want node and edges : replace SQLAlchemyConnectionField with graphene.List
    all_providers = SQLAlchemyConnectionField(Provider)#, providerId=graphene.Int())
    all_provider_reviews = SQLAlchemyConnectionField(Provider_Review, pId=graphene.Int())#, sort=Provider_Review.sort_argument())
    
#    def resolve_all_providers(self, info, **args):
#      query = Provider.get_query(info)
#      providerId = args.get('providerId')
#      return query.filter(ProviderModel.provider_id == providerId).all()
    
    def resolve_all_provider_reviews(self, info, **args):
      query = Provider_Review.get_query(info)
      pId = args.get('pId')
      return query.filter(Provider_ReviewModel.p_id == pId).all()
  

class AddReview(graphene.Mutation):
    class Arguments:
        p_id = graphene.Int(required=True)
        review = graphene.String(required=True) 
        result = graphene.String(required=True)
    post = graphene.Field(lambda: Provider_Review)
    def mutate(self, info, p_id, review, result):
        #user = User.query.filter_by(username=username).first()
        post = Provider_ReviewModel(p_id=p_id, review=review, result=result)
        db.add(post)
        db.commit()
        return AddReview(post=post)
    
class Mutation(graphene.ObjectType):
    add_review = AddReview.Field()
    
schema = graphene.Schema(query=Query, mutation=Mutation, types=[Provider, Provider_Review])




