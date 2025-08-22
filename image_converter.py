# 安装必要的库如 : pip install numpy opencv-python Pillow pillow-heif cairosvg
import cv2
import numpy
import numpy as np
from PIL import Image
import pillow_heif # pillow_heif会自动注册HEIC格式到Pillow中
import cairosvg
import  io

# 让Pillow去识别heic格式 使用统一的Image.open()来处理
pillow_heif.register_heif_opener()

# 设定支持的格式
# opencv原生支持的格式通常处理速度是最快的
OPENCV_NATIVE_FORMATS = ('.png','.jpg','.jpeg','.bmp','.tif','.tiff')
# pillow支持但是OpenCv可能不支持的格式
PILLOW_EXTRA_FORMATS = ('.webp', '.gif', '.heic')
# 需要特殊库处理的格式
SPECIAL_FORMATS = ('.svg')

def load_image_to_bgr(file_path: str) -> np.ndarray:
    """ 加载多种格式的图片文件，并统一转化为OpenCv支持的BGR格式的numpy数组
     入参 字符串类型的图片文件路径 file_path
     回参 bgr格式的图像数据 np.ndarray:BGR
     异常 如果文件格式不支持 或者 文件无法读取
     """

    #文件路径名小写 以方便进行 后缀名称匹配
    lower_path = file_path.lower()

    try:
        # 如果后缀是opencv原生支持的格式 直接使用imread
        if lower_path.endswith(OPENCV_NATIVE_FORMATS):
            image = cv2.imread(lower_path)
            # cv2.imread 默认就是bgr的格式
            # 如果为空 证明读取报错
            if image is None:
                raise IOError(f"OpenCv无法读取该文件地址的文件:{file_path}")
            print(f"成功使用opencv加载{file_path}下的文件")
            return image
        # 如果后缀是pillow支持的格式 直接使用image包打开图片
        elif lower_path.endswith(PILLOW_EXTRA_FORMATS):
            # 读取路径下的图片
            with Image.open(file_path) as img:
                if img.mode not in ('RGB', 'RGBA'):
                    img = img.convert('RGB')
                # 确保图片是RGB / RGBA 模式 方便转换
                # 将pillow图像转换为numpy数组 格式为rgb
                rgb_image = numpy.array(img)
                # 如果是rgba 去掉阿尔法通道 即去掉透明度 保留红绿蓝三原色
                # shape是numpy的一个重要属性 告诉数组的维度和大小
                # 对于图像来说 shape返回一个元组 包含三个值 (0 高度，1 宽度，2 通道值) 检查通道值有没有等于4 代表有透明度
                if rgb_image.ndim == 3 and rgb_image.shape[2] == 4:
                    bgr_image = cv2.cvtColor(rgb_image, cv2.COLOR_RGBA2BGR)
                else:
                    bgr_image = cv2.cvtColor(rgb_image, cv2.COLOR_RGB2BGR)
                print(f"使用pillow加载了{file_path}的文件,并成功转化为了BGR格式")
                return bgr_image

        elif lower_path.endswith(SPECIAL_FORMATS[0]):
            png_bytes = cairosvg.svg2png(url=file_path)
            #使用cairosvg将SVG渲染为png字节流
            #从字节流中读取图像数据
            image_stream = io.BytesIO(png_bytes)
            # 使用OpenCv从内存中解码图像
            # cv2.IMREAD_UNCHANGED 可以保留透明通道 暂时不需要
            image = cv2.imdecode(np.frombuffer(image_stream.read(), np.uint8), cv2.IMREAD_COLOR)
            if image is None:
                raise IOError(f"无法从渲染后的SVG解码图像: {file_path}")
            print(f"使用cairosvg加载{file_path}文件并将其转化为BGR格式")
            return image

        else:
            raise ValueError(f"不支持的文件格式:{file_path}")

    except Exception as e:
        print(f"错误的加载文件:{file_path}: {e}")
        raise

# 示例用法 真实的图片路径
if __name__ == '__main__':

    # 定义输入路径
    input_path = r"D:\develop\gitee\pytorch-tutorial\ConveyPic\static\history.jpg"
    # 定义输出路径
    output_path = r"D:\develop\gitee\pytorch-tutorial\ConveyPic\static\history_processed.jpeg"



    try:
        #调用核心函数
        bgr_array = load_image_to_bgr(input_path)
        print(f"加载成功! 数组形状:{bgr_array.shape}, 数据类型:{bgr_array.dtype}")

        #保存处理结果
        cv2.imwrite(output_path, bgr_array)
        print(f"处理结果已经保存到:{output_path}")

        # 弹窗显示图片以供预览
        cv2.imshow("处理的图片", bgr_array)
        print("按空格或回车键关闭预览窗口...")
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    except Exception as e:
        print(f"处理失败:{e}")