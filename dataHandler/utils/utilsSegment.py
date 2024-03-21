import os

def startSegment(inputFilePath):
    print('start seg')
    # 获取当前工作目录

    current_dir = os.getcwd()

    print("当前工作目录：", current_dir)

    # 切换到指定目录

    new_dir = "../../Tgnet_inference\ToothGroupNetwork-challenge_branch"

    os.chdir(new_dir)

    print("切换后的工作目录：", os.getcwd())

    os.system('python ./inference_final.py --input_path ../../learn-django/myDjangoApp/data/objData/00OMSZGW/ --save_path ../../learn-django/myDjangoApp/data/resultData/00OMSZGW/')

    os.chdir(current_dir)
    print('end seg')