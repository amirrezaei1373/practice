from django.shortcuts import render
from rest_framework import generics , permissions , mixins , status
from rest_framework.response import Response
from .models import Post , Vote
from .serializers import PostSerializer ,  VoteSerializer
from rest_framework.exceptions import ValidationError
# Create your views here.


class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def perform_cerate(self, serializer):
        serializer.save(poster= self.request.user)

class VoteCreate(generics.CreateAPIView, mixins.DestroyModelMixin):
    serializer_class = VoteSerializer
    permission_classes= [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        post = Post.objects.get(pk=self.kwargs['pk'])
        return Vote.objects.filter(voter = user , post = post)

    def perfrom_create(self, serializer):
        if self.get_queryset().exists():
            raise ValidationError('you already voted this post')
        serializer.save(voter = self.request.user, post=Post.objects.get(pk=self.kwargs['pk']))
    
    def delete(self, requests, *args, **kwargs):
        if self.get_query().exists():
            self.get_query().delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return ValidationError('oops you never voted this post')



