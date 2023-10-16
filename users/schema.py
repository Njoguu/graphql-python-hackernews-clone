from django.contrib.auth import get_user_model
import graphene
from graphene_django import DjangoObjectType
from django.db.models import Q


class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()

class Query(graphene.ObjectType):
    me = graphene.Field(UserType)
    users = graphene.List(
        UserType,
        first=graphene.Int(),
        last=graphene.Int(),
        skip=graphene.Int(),
        search=graphene.String(),
    )

    def resolve_users(self, info, search=None, first=None, skip=None, last=None):
        qs = get_user_model().objects.all()

        if search:
            filter = (
                Q(username__icontains=search)
            )
            qs = qs.filter(filter)

        if skip:
            qs = qs[skip:]

        if first:
            qs = qs[:first]

        if last:
            qs = qs.order_by('-id')[:last]

        return qs
        
    
    def resolve_me(self, info):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Not logged in!')

        return user

class CreateUser(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String(required=True)

    def mutate(self, info, username, password, email):
        user = get_user_model()(
            username=username,
            email=email,
        )
        user.set_password(password)
        user.save()

        return CreateUser(user=user)

class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()