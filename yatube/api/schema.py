import graphene
from graphene_django.types import DjangoObjectType, ObjectType
from posts.models import Comment, Post, User


# Create a GraphQL type for the User model
class UserType(DjangoObjectType):

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name')


# Create a GraphQL type for the Post model
class PostType(DjangoObjectType):

    class Meta:
        model = Post
        fields = '__all__'


# Create a GraphQL type for the Post model
class CommentType(DjangoObjectType):

    class Meta:
        model = Comment
        fields = '__all__'


class Query(ObjectType):
    user = graphene.Field(UserType, id=graphene.Int())
    post = graphene.Field(PostType, id=graphene.Int())
    comment = graphene.Field(CommentType, id=graphene.Int())
    users = graphene.List(UserType)
    posts = graphene.List(PostType)
    comments = graphene.List(CommentType)

    def resolve_user(self, info, **kwargs):
        id = kwargs.get('id')
        if id is not None:
            return User.objects.get(pk=id)
        return None

    def resolve_post(self, info, **kwargs):
        id = kwargs.get('id')
        if id is not None:
            return Post.objects.get(pk=id)
        return None

    def resolve_comment(self, info, **kwargs):
        id = kwargs.get('id')
        if id is not None:
            return Comment.objects.get(pk=id)
        return None

    def resolve_users(self, info, **kwargs):
        return User.objects.all()

    def resolve_posts(self, info, **kwargs):
        return Post.objects.all()

    def resolve_comments(self, info, **kwargs):
        return Comment.objects.all()


# class UserInput(graphene.InputObjectType):
#     id = graphene.ID()
#     name = graphene.String()


# class PostInput(graphene.InputObjectType):
#     id = graphene.ID()
#     title = graphene.String()
#     actors = graphene.List(ActorInput)
#     year = graphene.Int()

schema = graphene.Schema(query=Query,
                         # mutation=Mutation
                         )