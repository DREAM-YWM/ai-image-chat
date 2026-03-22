import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import ezdxf
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import uvicorn
from PIL import Image
import pytesseract
from qcloud_cos import CosConfig, CosS3Client  # 腾讯云COS

# 初始化FastAPI
app = FastAPI(title="DXF分析后端服务")


# ----------------------
# 1. 健康检查接口（老师要求的基础接口）
# ----------------------
@app.get("/health", summary="健康检查")
def health_check():
    return {"code": 0, "message": "服务正常运行", "data": {"status": "ok"}}


# ----------------------
# 2. 调用AI模块的接口示例（满足老师「引用ai模块」的要求）
# ----------------------
@app.get("/call-ai", summary="调用AI模块接口")
def call_ai_module():
    try:
        # 从ai模块导入服务（根据实际文件名修改）
        from ai import ai_service
        # 调用AI模块的函数（示例：假设ai_service有一个get_ai_response函数）
        ai_result = ai_service.get_ai_response("测试输入")
        return {
            "code": 0,
            "message": "成功调用AI模块接口",
            "data": {"ai_response": ai_result}
        }
    except Exception as e:
        return {"code": 1, "message": f"调用AI模块失败: {str(e)}", "data": {}}


# ----------------------
# 3. DXF上传+解析接口（你的核心功能）
# ----------------------
@app.post("/upload-dxf", summary="上传DXF文件并解析")
async def upload_dxf(file: UploadFile = File(...)):
    try:
        # 1. 保存上传的DXF文件
        file_path = f"temp_{file.filename}"
        with open(file_path, "wb") as f:
            f.write(await file.read())

        # 2. 解析DXF文件（使用ezdxf）
        doc = ezdxf.readfile(file_path)
        msp = doc.modelspace()
        parse_text = f"DXF解析成功：共{len(list(msp))}个图元"

        # 3. 调用AI模块（示例：把解析结果传给AI）
        ai_response = ""
        try:
            from ai import ai_service
            ai_response = ai_service.get_ai_response(parse_text)
        except:
            ai_response = "AI模块暂不可用"

        # 4. 返回结果
        return JSONResponse(
            content={
                "code": 0,
                "message": "DXF上传+解析+AI调用成功",
                "data": {
                    "original_filename": file.filename,
                    "dxf_parse_info": parse_text,
                    "ai_response": ai_response
                }
            }
        )
    except Exception as e:
        return JSONResponse(
            content={"code": 1, "message": f"处理失败: {str(e)}", "data": {}},
            status_code=500
        )


# ----------------------
# 4. 启动服务
# ----------------------
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)