from PIL import Image
import io
import base64
import imagesData



def decode_base64_to_image(base64_string):
    image_data = base64.b64decode(base64_string)
    image = Image.open(io.BytesIO(image_data))
    return image

if __name__ == "__main__":
    base64_string = imagesData.default_png  # 将Base64字符串替换为你的实际Base64字符串

    decoded_image = decode_base64_to_image(base64_string)
    decoded_image.show()  # 在默认图像查看器中显示解码后的图像