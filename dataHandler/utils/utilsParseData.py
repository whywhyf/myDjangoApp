import base64
import vtk
import os
import tempfile

# 将polydata对象转换为Base64编码的XML字符串，用于发送给前端
def polydata_to_string(polydata):
    '''
    将vtkPolyData对象转换为Base64编码的XML字符串,用于发送给前端。

    :param polydata: vtkPolyData对象,包含要转换的数据。
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


def parse_polydata(polydata_string):
    '''
    解析输入的 PolyData 字符串并返回相应的 vtkPolyData 对象。

    :param polydata_string: 包含 PolyData 信息的字符串
    :type polydata_string: str
    :return: 与输入字符串对应的 vtkPolyData 对象
    :rtype: vtkPolyData
    '''
    # 由于 vtkXMLPolyDataReader 期望一个文件，我们需要先将字符串写入一个临时文件
    temp = tempfile.NamedTemporaryFile(delete=False)
    temp.write(polydata_string.encode('utf-8'))
    temp.close()

    # 创建一个 vtkXMLPolyDataReader
    reader = vtk.vtkXMLPolyDataReader()
    reader.SetFileName(temp.name)
    reader.Update()

    # 删除临时文件
    os.unlink(temp.name)

    # 从 reader 中获取 polydata
    polydata = reader.GetOutput()

    # 现在你可以使用 polydata 进行进一步的处理
    # ...

    return polydata