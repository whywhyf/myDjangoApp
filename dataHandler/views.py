from django.shortcuts import render, HttpResponse
from django.http import JsonResponse 
from django.http import FileResponse 

import os  
import vtk
import json  
import base64

# Create your views here.
# def returnObjData(request):
#     return HttpResponse('nihao ')


# 返回obj文件数据
def returnObjData(request):  
    print('objdata request')
    file_path = 'data/objData/00OMSZGW_lower.obj'  # 替换为您自己的文件路径  
    if os.path.exists(file_path):  
        with open(file_path, 'rb') as file:  
            response = HttpResponse(file, content_type='application/force-download')  
            response['Content-Disposition'] = 'attachment; filename="00OMSZGW_lower.obj"'  
            return response  
    else:  
        return HttpResponse("File not found", status=404) 


# 返回读入obj获得的polydata
def returnPolyData(request):
    
    # 使用objImporter
    objImporter = vtk.vtkOBJImporter()
    # 当前工作目录在项目根目录
    objImporter.SetFileName('data/objData/00OMSZGW_lower.obj')
    objImporter.Update()
    objImporter.InitializeObjectBase()
    objImporter.GetRenderer()
    objImporter.GetOutputDescription(0)
    print(objImporter.GetOutputDescription(0))
    print('vtk v',vtk.VTK_MAJOR_VERSION)
    renderer = vtk.vtkRenderer()
    renderer.UseHiddenLineRemovalOn()
    renWin = vtk.vtkRenderWindow()
    iren = vtk.vtkRenderWindowInteractor()
    renWin.AddRenderer(renderer)
    renWin.SetWindowName('OBJImporter')
    actors = renderer.GetActors()
    actors.InitTraversal()
    iren.SetRenderWindow(renWin)
    objImporter.SetRenderWindow(renWin)
    objImporter.Update()
    actors = renderer.GetActors()
    actors.InitTraversal()
    renWin.Render()
    renderer.ResetCamera()
    # iren.Start()# 开启渲染窗口
    # 获取polydata
    polydata = vtk.vtkPolyData()
    actor = actors.GetNextActor()
    polydata.DeepCopy(actor.GetMapper().GetInput())
    print(polydata)
    # ren = vtk.vtkRenderer()
    polyDataString = polydata_to_string(polydata)

    return JsonResponse({'message': '成功以string接收polydata', 'polydata': polyDataString})


# 将polydata对象转换为Base64编码的XML字符串，用于发送给前端
def polydata_to_string(polydata):
    '''
    将vtkPolyData对象转换为Base64编码的XML字符串，用于发送给前端。

    :param polydata: vtkPolyData对象，包含要转换的数据。
    :return: Base64编码的XML字符串。
    '''
    writer = vtk.vtkXMLPolyDataWriter()
    writer.SetInputData(polydata)
    writer.WriteToOutputStringOn()
    writer.Write()
    xml_string = writer.GetOutputString()
    base64_encoded = base64.b64encode(xml_string.encode()).decode()
    # base64_encoded = base64.b64encode(xml_string.encode())
    return base64_encoded