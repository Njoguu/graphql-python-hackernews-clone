import graphene
from graphene_django import DjangoObjectType
from .models import Link, Vote
from users.schema import UserType
from graphql import GraphQLError
from django.db.models import Q


class LinkType(DjangoObjectType):
    class Meta:
        model = Link

class VoteType(DjangoObjectType):
    class Meta:
        model = Vote

class Query(graphene.ObjectType):
    links = graphene.List(
        LinkType,
        search=graphene.String(), 
        first=graphene.Int(),
        skip=graphene.Int(),
        )
    
    votes = graphene.List(
        VoteType,
        first=graphene.Int(),
        last=graphene.Int(),
        skip=graphene.Int()
    )

    def resolve_links(self, info, search=None, first=None, skip=None, **kwargs):
        qs = Link.objects.all()

        if search:
            filter = (
                Q(url__icontains=search) |
                Q(description__icontains=search)
            )
            qs = qs.filter(filter)

        if skip:
            qs = qs[skip:]

        if first:
            qs = qs[:first]

        return qs

    def resolve_votes(self, info, first=None, skip=None, last=None,**kwargs):
        qs = Vote.objects.all()

        if skip:
            qs = qs[skip:]

        if first:
            qs = qs[:first]

        if last:
            qs = qs.order_by('-id')[:last]

        return qs

class CreateLink(graphene.Mutation):
    id = graphene.Int()
    url = graphene.String()
    description = graphene.String()
    date_posted = graphene.Date()
    posted_by = graphene.Field(UserType)

    #2
    class Arguments:
        url = graphene.String()
        description = graphene.String()

    #3
    def mutate(self, info, url, description):
        user = info.context.user or None

        link = Link(url=url, description=description, posted_by=user)
        link.save()

        return CreateLink(
            id=link.id,
            url=link.url,
            description=link.description,
            date_posted=link.date_posted,
            posted_by=link.posted_by
        )

class DeleteLink(graphene.Mutation):
    id = graphene.Int()

    class Arguments:
        id = graphene.Int()

    def mutate(self, info, id):
        link = Link(id=id)
        link.delete()

        return DeleteLink(
            id=link.id,
        )

class CreateVote(graphene.Mutation):
    user = graphene.Field(UserType)
    link = graphene.Field(LinkType)

    class Arguments:
        link_id = graphene.Int()

    def mutate(self, info, link_id):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError('You must be logged in to vote!')

        link = Link.objects.filter(id=link_id).first()
        if not link:
            raise Exception('Invalid Link!')

        Vote.objects.create(
            user=user,
            link=link,
        )

        return CreateVote(user=user, link=link)

#4
class Mutation(graphene.ObjectType):
    create_link = CreateLink.Field()
    delete_link = DeleteLink.Field()
    create_vote = CreateVote.Field()
