from django.shortcuts import render, HttpResponse
from django.http import JsonResponse 
from django.http import FileResponse 
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt



import os  
import vtk
import json  
import base64
import numpy as np
import asyncio
import threading

from vtkmodules.util import numpy_support

from .utils.utilsParseData import parse_polydata, polydata_to_string
from .utils.utilsSegment import startSegment
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


# 返回读入obj获得的polydata和json
def returnPolyData(request):
    
    # 使用objImporter
    objImporter = vtk.vtkOBJImporter()
    # 当前工作目录在项目根目录
    objImporter.SetFileName('data/objData/00OMSZGW/00OMSZGW/00OMSZGW_lower.obj')
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
    # renWin.Render()
    renderer.ResetCamera()
    # iren.Start()# 开启渲染窗口

    # 获取polydata
    polydata = vtk.vtkPolyData()
    actor = actors.GetNextActor()
    polydata.DeepCopy(actor.GetMapper().GetInput())
    print(polydata)
    # ren = vtk.vtkRenderer()
    polyDataString = polydata_to_string(polydata)




    # 读入json
    with open('data/jsonData/00OMSZGW_lower.json', 'r') as file:  
        labelData = json.load(file)  
    return JsonResponse({'message': '成功以string接收polydata', 'polyData': polyDataString, 'labelData': labelData})


# 保存收到的labeljson到本地
@csrf_exempt
def saveLabel(request):
    if request.method == 'POST':  
        json_data = json.loads(request.body)  # 从请求中获取 JSON 数据  
        # 在这里可以将 JSON 数据保存在本地文件中，或者进行其他处理  
        # 例如：  
        with open('data/resultData/00OMSZGW_lower.json', 'w') as f:  
            json.dump(json_data, f)  
        print('labelData saved!')
        return JsonResponse({'message': 'JSON data saved successfully'})  
    else:  
        return JsonResponse({'error': 'Invalid request method'}, status=405)  
    

# done 目前收到的polydata面是对的，点全部丢失 可以试试传坐标
# 将收到的polydata保存为obj
@csrf_exempt
def savePolyDataAsObj(request):  
    if request.method == 'POST':  
        # polydata_as_string = request.FILES['polyData'].read().decode('utf-8')
        # polydata = parse_polydata(polydata_as_string)
        # # 例如：  
        # # 使用objExporter
        # print(polydata)
        # objExporter = vtk.vtkOBJExporter()
        # objExporter.SetFilePrefix('data/segObj/00OMSZGW_lower')
        # mapper = vtk.vtkPolyDataMapper()
        # mapper.SetInputData(polydata)
        # actor = vtk.vtkActor()
        # actor.SetMapper(mapper)
        # actor.GetProperty().SetSpecular(.3) 
        # actor.GetProperty().SetSpecularPower(30) 
        # ren = vtk.vtkRenderer()
        # ren.AddActor(actor)
        # renWin = vtk.vtkRenderWindow()
        # renWin.AddRenderer(ren)
        # renWin.SetSize(1000, 1000)

        # iren = vtk.vtkRenderWindowInteractor()
        # iren.SetRenderWindow(renWin)
        # iren.Initialize()
        # renWin.Render()
        # iren.Start()

        # objExporter.SetInput(renWin)
        # objExporter.Write()
        print('start save')
        json_data = json.loads(request.body) 
        # print(json_data)
        print(json_data['points'].keys())
        print(json_data['polys'].keys())
        pointsData = np.array(json_data['points']['values'])
        # print(pointsData.shape)
        
        # NumPy_data_shape = pointsData.shape
        # pointsData.reshape(int(pointsData.shape[0]/3), 3)
        # VTK_pointsdata = numpy_support.numpy_to_vtk(num_array=pointsData, deep=True)
        # pointsVtkdata = vtk.vtkDataArray({pointsData['values']})

        polysData = np.array(json_data['polys']['values'])
        # VTK_polysdata = numpy_support.numpy_to_vtk(num_array=polysData.ravel(), deep=True, array_type=vtk.VTK_FLOAT)

        points = vtk.vtkPoints()
        polys = vtk.vtkCellArray()
        for i in range(int(pointsData.shape[0]/3)):
            points.InsertNextPoint(pointsData[3*i], pointsData[3*i+1], pointsData[3*i+2])
        for i in range(int(polysData.shape[0]/4)):
            polys.InsertNextCell(polysData[4*i], [polysData[4*i+1], polysData[4*i+2], polysData[4*i+3]])
        # points.SetData(VTK_pointsdata)
        # polys.SetData(VTK_polysdata)
        polyData = vtk.vtkPolyData()
        polyData.SetPoints(points)
        polyData.SetPolys(polys)


        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputData(polyData)
        actor = vtk.vtkActor()
        actor.SetMapper(mapper)
        ren = vtk.vtkRenderer()
        ren.AddActor(actor)
        renWin = vtk.vtkRenderWindow()
        renWin.AddRenderer(ren)
        # iren = vtk.vtkRenderWindowInteractor()
        # iren.SetRenderWindow(renWin)
        # iren.Initialize()
        # renWin.Render()
        # iren.Start()

        objExporter = vtk.vtkOBJExporter()
        objExporter.SetFilePrefix('data/segObj/00OMSZGW/00OMSZGW/00OMSZGW_lower')
        objExporter.SetInput(renWin)
        objExporter.Write()
        startSegment('data/segObj/', id = '00OMSZGW')

        with open('data/resultData/00OMSZGW/00OMSZGW_lower.json', 'r') as file:  
            labelData = json.load(file)  

        return JsonResponse({'message': 'poly data saved and seg successfully','labelData': labelData})  
    else:  
        return JsonResponse({'error': 'Invalid request method'}, status=405)  
    

# 接收分割请求并分割
@csrf_exempt
def segmentBothTooth(request):  
    if request.method == 'POST':  

        print('start save')
        json_data = json.loads(request.body) 
        print(json_data.keys())
        print(json_data['upperPoints'].keys())
        print(json_data['upperPolys'].keys())
        id = json_data['id']
        print('id:', id)

        upperPointsData = np.array(json_data['upperPoints']['values'])
        upperPolysData = np.array(json_data['upperPolys']['values'])
        lowerPointsData = np.array(json_data['lowerPoints']['values'])
        lowerPolysData = np.array(json_data['lowerPolys']['values'])

        # 开启两个子线程分别保存上下牙
        threadUpper = threading.Thread(target=convertToPolyData(upperPointsData, upperPolysData, id, 'upper'))
        threadLower = threading.Thread(target=convertToPolyData(lowerPointsData, lowerPolysData, id, 'lower'))

        threadUpper.start()
        threadLower.start()

        threadUpper.join()
        threadLower.join()

        # path = 'data/segData/id/id/id_teethtype/obj'
        segPath = 'data/segObj/'
        startSegment(segPath, id)
        # openPath ='data/resultData/id/id_teethType.json'
        openPath = 'data/resultData/'+id+'/'+id
        with open(openPath+'_upper.json', 'r') as file:  
            upperLabelData = json.load(file)  
        with open(openPath+'_lower.json', 'r') as file:  
            lowerLabelData = json.load(file)  

        return JsonResponse({'message': 'both tooth saved successfully', 'upper': upperLabelData, 'lower': lowerLabelData})
        # return JsonResponse({'message': 'poly data saved and seg successfully','labelData': labelData})  
    else:  
        return JsonResponse({'error': 'Invalid request method'}, status=405)  
    
#  done 用子线程分别完成两个保存
@csrf_exempt
def convertToPolyData(pointsData, polysData, id, teethType):
        points = vtk.vtkPoints()
        polys = vtk.vtkCellArray()
        for i in range(int(pointsData.shape[0]/3)):
            points.InsertNextPoint(pointsData[3*i], pointsData[3*i+1], pointsData[3*i+2])
        for i in range(int(polysData.shape[0]/4)):
            polys.InsertNextCell(polysData[4*i], [polysData[4*i+1], polysData[4*i+2], polysData[4*i+3]])

        polyData = vtk.vtkPolyData()
        polyData.SetPoints(points)
        polyData.SetPolys(polys)

        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputData(polyData)
        actor = vtk.vtkActor()
        actor.SetMapper(mapper)
        ren = vtk.vtkRenderer()
        ren.AddActor(actor)
        renWin = vtk.vtkRenderWindow()
        renWin.AddRenderer(ren)

        objExporter = vtk.vtkOBJExporter()
        # filePrefix = 'data/segObj/id/id/id_teethType'
        filePrefix = 'data/segObj/' + id + '/' + id + '/' + id + '_' + teethType
        objExporter.SetFilePrefix(filePrefix)
        objExporter.SetInput(renWin)
        directory = 'data/segObj/' + id + '/' + id + '/'
        if not os.path.exists(directory):  # 检查目录是否存在  
            os.makedirs(directory)  # 如果目录不存在，则创建它 
        objExporter.Write()
