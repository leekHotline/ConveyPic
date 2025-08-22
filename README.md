<div align="center">
  <img src="https://raw.githubusercontent.com/your-username/ConveyPic/main/assets/logo.png" alt="ConveyPic Logo" width="150"/>
  <h1>ConveyPic 🖼️✨</h1>
  <p>
    <strong>一个通用、高效的图像格式转换工具，可将多种图片格式（包括 HEIC, WebP, SVG）无缝转换为 OpenCV 支持的 NumPy 数组，并提供一个轻量级的 FastAPI 接口。</strong>
  </p>

  <p>
    <!-- Badges -->
    <a href="https://python.org">
      <img src="https://img.shields.io/badge/Python-3.9+-blue?logo=python&logoColor=yellow" alt="Python Version">
    </a>
    <a href="#">
      <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License">
    </a>
    <a href="#">
      <img src="https://img.shields.io/badge/status-active-brightgreen.svg" alt="Project Status">
    </a>
    <a href="https://github.com/your-username/ConveyPic/pulls">
      <img src="https://img.shields.io/badge/PRs-welcome-orange.svg" alt="PRs Welcome">
    </a>
  </p>
</div>

---

## 🚀 核心功能 (Core Features)

- **🖼️ 广泛的格式支持**: 无需关心输入格式，无论是常见的 `JPG/PNG`，现代的 `WebP`，苹果设备的 `HEIC`，还是矢量图 `SVG`，都能统一处理。
- **⚡ 高性能转换**: 优先使用原生 `OpenCV` 进行高速处理，并无缝回退到高效的 `Pillow` 库，确保性能与兼容性的完美平衡。
- **🧩 统一输出**: 无论输入是什么，始终输出标准的 `OpenCV BGR NumPy` 数组，方便直接送入您的计算机视觉模型或处理流程。
- **☁️ API驱动**: 内置一个基于 **FastAPI** 的轻量级API服务，开箱即用，轻松集成到您的任何应用中。
- **📄 交互式文档**: 启动服务后，自动获得一个漂亮的 **Swagger UI** 交互式API文档页面 (`/docs`)，无需手写文档即可在线测试。

## 🛠️ 技术栈 (Tech Stack)

![OpenCV](https://img.shields.io/badge/OpenCV-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white)
![Pillow](https://img.shields.io/badge/Pillow-943282?style=for-the-badge)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Uvicorn](https://img.shields.io/badge/Uvicorn-9C27B0?style=for-the-badge)
![NumPy](https://img.shields.io/badge/NumPy-4D77CF?style=for-the-badge&logo=numpy&logoColor=white)

## 📦 安装 (Installation)

1.  **克隆仓库**:
    ```bash
    git clone https://github.com/your-username/ConveyPic.git
    cd ConveyPic
    ```

2.  **创建并激活虚拟环境 (推荐)**:
    ```bash
    python -m venv venv
    # Windows
    .\venv\Scripts\activate
    # macOS/Linux
    source venv/bin/activate
    ```

3.  **安装依赖**:
    ```bash
    pip install -r requirements.txt
    ```

## 🎮 快速开始 (Quick Start)

启动API服务非常简单：

```bash
python main.py
