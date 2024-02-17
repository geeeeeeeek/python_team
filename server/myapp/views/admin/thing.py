# Create your views here.
from rest_framework.decorators import api_view, authentication_classes

from myapp import utils
from myapp.auth.authentication import AdminTokenAuthtication
from myapp.handler import APIResponse
from myapp.models import Classification, Thing, Tag
from myapp.permission.permission import isDemoAdminUser
from myapp.serializers import ThingSerializer, UpdateThingSerializer


@api_view(['GET'])
def list_api(request):
    if request.method == 'GET':
        keyword = request.GET.get("keyword", None)
        c = request.GET.get("c", None)
        tag = request.GET.get("tag", None)
        if keyword:
            things = Thing.objects.filter(title__contains=keyword).order_by('create_time')
        elif c:
            classification = Classification.objects.get(pk=c)
            things = classification.classification_thing.all()
        elif tag:
            tag = Tag.objects.get(id=tag)
            print(tag)
            things = tag.thing_set.all()
        else:
            things = Thing.objects.all().order_by('create_time')

        serializer = ThingSerializer(things, many=True)
        return APIResponse(code=0, msg='查询成功', data=serializer.data)


@api_view(['GET'])
def detail(request):

    try:
        pk = request.GET.get('id', -1)
        thing = Thing.objects.get(pk=pk)
    except Thing.DoesNotExist:
        utils.log_error(request, '对象不存在')
        return APIResponse(code=1, msg='对象不存在')

    if request.method == 'GET':
        serializer = ThingSerializer(thing)
        return APIResponse(code=0, msg='查询成功', data=serializer.data)

