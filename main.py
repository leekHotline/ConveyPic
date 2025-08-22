from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import tempfile # 用于创建临时文件
import os # 用于处理文件路径和后缀名
import uvicorn # 导入uvicorn以便在脚本中直接启动服务

from image_converter import load_image_to_bgr

#初始化FastApi应用
app = FastAPI(
    title="图像格式统一转换服务",
    description="上传任意支持的图片格式，将其转换为OpenCv支持的BGR Numpy数组并返回基本信息",
    version='1.0.0'
)

@app.post('/convert_image')
async def conver_image_endpoint(file: UploadFile = File(...)):
    """
    接收上传的图片文件，进行格式转换，并返回图像基本信息。
    """
    # 算法函数需要一个文件路径 但是fastapi上次的是内存中的文件流
    # 将上传的文件流先保存在一个临时文件中
    try:
        suffix = os.path.splitext(file.filename)[1]

        # 创建一个带有正常后缀名称的文件 这样算法才能识别 不自动删除
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
            # 异步读取上传的文件内容
            contents = await file.read()
            if not contents:
                raise HTTPException(status_code=400, detail="上传的文件为空")

            # 将内容写入临时文件
            temp_file.write(contents)
            # 获取这个临时文件的完整路径
            temp_file_path = temp_file.name
        print(f"收到文件 '{file.filename}', 已保存到临时路径: {temp_file_path}")

        # 核心步骤 调用算法函数
        bgr_array = load_image_to_bgr(temp_file_path)
        # 算法执行完毕现在可以使用bgr_array 例如交给机器学习模型分析
        # model.predict(bgr_array)

        # 提取图像信息作为api的返回结果
        height, width, channels = bgr_array.shape

        # 返回json接口
        return JSONResponse(
            status_code=200,
            content={
                "message": "图片处理成功",
                "filename": file.filename,
                "image_info": {
                    "width": width,
                    "height": height,
                    "channels": channels
                }

            }
        )


    except (ValueError, IOError) as e:
        # 返回一个 400 错误码，表示客户端请求有问题
        raise HTTPException(status_code=400, detail=f"文件处理失败: {str(e)}")

    except Exception as e:
        # 返回一个 500 错误码，表示服务器内部出错了
        raise HTTPException(status_code=500, detail=f"服务器内部错误: {str(e)}")
    finally:
        # 无论成功或失败 要确保删除我们创建的临时文件
        if 'temp_file_path' in locals() and os.path.exists(temp_file_path):
            os.unlink(temp_file_path)
            print(f"已删除临时文件: {temp_file_path}")

if __name__ == "__main__":
    print("--- 启动后端服务 ---")
    print("--- 可以访问 http://127.0.0.1:8080/docs 查看API文档并进行测试 ---")
    # 启动uvicorn服务
    uvicorn.run(
         "main:app",  #格式为 文件名:fastapi实例名
         host= "0.0.0.0",  #允许局域网的其他设备访问
         port= 8080,
         reload=True # 开发模式 代码被修改时 服务自动重启
    )