# -*- coding: utf-8 -*-
import requests
import json

api_key = 'app-blQDV3X4gAKHm7wrRsBWKN1Q'  # 替换为你的工作流API密钥

def upload_file(file_path, user):
    upload_url = "http://localhost:8080/v1/files/upload"
    headers = {
        "Authorization": f'Bearer {api_key}',
    }

    try:
        print("上传文件中...")
        with open(file_path, 'rb') as file:
            files = {
                'file': (file_path, file, 'image/{}'.format(file_path.rsplit('.', 1)[-1].lower()))  # 确保文件以适当的MIME类型上传
            }
            data = {
                "user": user,
                "type": "image"
            }

            response = requests.post(upload_url, headers=headers, files=files, data=data)
            if response.status_code == 201:  # 201 表示创建成功
                print("文件上传成功")
                return response.json().get("id")  # 获取上传的文件 ID
            else:
                print(f"文件上传失败，状态码: {response.status_code}")
                print(response.text)
                return None
    except Exception as e:
        print(f"发生错误: {str(e)}")
        return None


def run_workflow(file_id, user, response_mode="blocking"):
    workflow_url = "http://localhost:8080/v1/workflows/run"
    headers = {
        "Authorization": f'Bearer {api_key}',
        "Content-Type": "application/json"
    }

    data = {
        "inputs": {
            "ticket_file": {
                "transfer_method": "local_file",
                "upload_file_id": file_id,
                "type": "image"
            }
        },
        "response_mode": response_mode,
        "user": user
    }

    try:
        print("运行工作流...")
        response = requests.post(workflow_url, headers=headers, json=data)
        if response.status_code == 200:
            print("工作流执行成功")
            return response.json()
        else:
            print(f"工作流执行失败，状态码: {response.status_code}")
            print(response.text)
            return {"status": "error", "message": f"Failed to execute workflow, status code: {response.status_code}"}
    except Exception as e:
        print(f"发生错误: {str(e)}")
        return {"status": "error", "message": str(e)}


# 使用示例
file_path = '火车票.jpg'  # 增值税普通发票.png、增值税普通发票.png 、、火车票纸质.jpg
user = 'zouwei'     # 任意输入

# 上传文件
file_id = upload_file(file_path, user)
if file_id:
    print("file_id:", file_id)
    # 文件上传成功，继续运行工作流
    result = run_workflow(file_id, user)
    print(result['data']['outputs']['text'])
else:
    print("文件上传失败，无法执行工作流")
