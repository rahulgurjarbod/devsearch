from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from .serializers import ProjectSerializer
from projects.models import Project, Review, Tag


@api_view(['GET'])
def getRoutes(request):

    routes = [
        {'GET':'api/projects'},
        {'GET':'api/projects/id'},

        {'POST':'api/projects/id/vote'},
        {'PUT':'api/projects/id/changes'},

        {'POST':'api/users/token'},
        {'POST':'api/users/token/refresh'},
    ]
    return Response(routes)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_projects(request):
    projects = Project.objects.all()
    serializer = ProjectSerializer(projects, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_project(request, pk):
    project = Project.objects.get(id=pk)
    serializer = ProjectSerializer(project, many=False)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def projectVote(request, pk):
    project = Project.objects.get(id=pk)
    user = request.user.profile
    print(user)
    data = request.data

    review, created = Review.objects.get_or_create(
        owner = user,
        project = project,
    )

    review.value = data['value']
    review.save()
    project.getVoteCount

    serializer = ProjectSerializer(project, many=False)
    return Response(serializer.data)


@api_view(['DELETE'])
def removeTag(request):

    projectId = request.data['project']
    tagId = request.data['tag']                      #--> It takes data from frontend

    project = Project.objects.get(id=projectId) 
    tag = Tag.objects.get(id=tagId)                  #--> It confirm that id is present in database

    project.tags.remove(tag)

    return Response('Tag was Deleted !!')

