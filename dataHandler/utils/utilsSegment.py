import os

def startSegment(inputFilePath, id):
    print('start seg')
    # 获取当前工作目录

    current_dir = os.getcwd()

    print("当前工作目录：", current_dir)

    # 切换到指定目录

    new_dir = "../../Tgnet_inference\ToothGroupNetwork-challenge_branch"

    os.chdir(new_dir)

    print("切换后的工作目录：", os.getcwd())

    inputPath = '../../learn-django/myDjangoApp/' + inputFilePath + id + '/'
    outputPath = '../../learn-django/myDjangoApp/data/resultData/'+id+'/'
    if not os.path.exists(outputPath):  # 检查目录是否存在  
        os.makedirs(outputPath)  # 如果目录不存在，则创建它 
    cmd = 'python ./inference_final.py --input_path '+ inputPath +' --save_path '+ outputPath
    print(cmd)
    print('开始分割',id)
    # os.system('python ./inference_final.py --input_path ../../learn-django/myDjangoApp/data/segObj/00OMSZGW/ --save_path ../../learn-django/myDjangoApp/data/resultData/00OMSZGW/')
    os.system(cmd)

    os.chdir(current_dir)
    print('分割结束')