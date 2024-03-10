import json  
import os  

# 获取当前工作目录  
current_directory = os.getcwd()  
print(current_directory)  
# 读取 JSON 文件  
with open('data/jsonData/00OMSZGW_lower.json', 'r') as file:  
    data = json.load(file)  
  
# 打印读取的数据  
print(len(data['labels'])) 