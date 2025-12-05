import uvicorn
from src.init_db import initialize_database


if __name__ == "__main__":
    # 初始化数据库表结构
    initialize_database()

    # 创建测试数据（可选，仅在开发环境中使用）
    #from src.init_db import create_test_data
    # create_test_data()

    # 启动 FastAPI 应用
    print("启动财务管理系统 API...")
    uvicorn.run(
        "src.api_interface:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # 开启热重载（开发模式）
        log_level="info",
        access_log=True
    )
