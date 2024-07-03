import logging
from rest_framework import status
from rest_framework import mixins
from .responses import SuccessResponse

logger = logging.getLogger(__name__)

class MixinClass(mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.ListModelMixin):
    model = None

    def get_object(self):
        uuid_id = str(self.kwargs.get('pk'))
        return self.model.objects.get(id = uuid_id)
        
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        logger.info(f"Performed create operation on {type(serializer)[0].__name__}, Created Successfully")
        result=SuccessResponse(code=status.HTTP_201_CREATED, status='CREATED', message='Created Successfully',data=serializer.data)
        return result.http_response(status=status.HTTP_201_CREATED)     
    
    def list(self,request,*args,**kwargs):
        queryset = self.get_queryset()
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(queryset, request)
        serialized = self.serializer_class(page, many=True)
        serialized_data = serialized.data
        next_page_url = paginator.get_next_link()
        prev_page_url = paginator.get_previous_link()
        logger.info(f"Fetched all records from {serialized.__class__.__name__}") 
        result=SuccessResponse(code=status.HTTP_200_OK, status='OK',message='Fetched all records',data = serialized_data,
                                next_page=next_page_url, previous_page=prev_page_url)
        return result.http_response(status=status.HTTP_200_OK) 
    
    def getById(self,request,*args,**kwargs): 
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        logger.info(f"Performed getById on {type(serializer)[0].__name__}, Fetched by uuid successfully")
        result=SuccessResponse(code=status.HTTP_200_OK, status='OK',message='Fetched by uuid',data=data)
        return result.http_response(status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        logger.info(f"Performed update on {type(serializer)[0].__name__}, Updated Successfully")
        result=SuccessResponse(code=status.HTTP_205_RESET_CONTENT, status='RESET CONTENT',message='Updated Successfully',data = serializer.data)
        return result.http_response(status=205)  
    
    def destroy(self,request,*args,**kwargs):
        queryset = self.get_object()
        data = str(queryset.id)
        queryset.delete()
        logger.info("Deleted record")
        result=SuccessResponse(code=status.HTTP_200_OK,status='OK',message=f' UUID  : {data} Deleted Successfully')
        return result.http_response(status=status.HTTP_200_OK)