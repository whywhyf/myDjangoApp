from django.shortcuts import render, HttpResponse

from django.http import FileResponse, HttpResponse  
import os  

# Create your views here.
# def returnObjData(request):
#     return HttpResponse('nihao ')
def returnObjData(request):  
    file_path = 'data/objData/00OMSZGW_lower.obj'  # 替换为您自己的文件路径  
    if os.path.exists(file_path):  
        with open(file_path, 'rb') as file:  
            response = HttpResponse(file, content_type='application/force-download')  
            response['Content-Disposition'] = 'attachment; filename="00OMSZGW_lower.obj"'  
            return response  
    else:  
        return HttpResponse("File not found", status=404) 