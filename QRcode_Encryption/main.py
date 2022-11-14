import base64
from tkinter import filedialog
from PIL import Image, ImageTk

from MyDES import DES
import qrcode
import zxing
import tkinter as tk


# 把url制作成二维码, 指定路径和名称保存
def make_qrcode(url, name):
    origin_img = qrcode.make(url)
    origin_img.save(name)


# 提取二维码中的url
def extract_qrcode(img):
    reader = zxing.BarCodeReader()
    barcode = reader.decode(img)
    text = barcode.parsed
    return text


# 将原二维码中的内容用DES加密
def encrypt_url(key, url):
    D = DES()
    result = "V me 50 to get code: " + (base64.b64encode((D.run(key, url, 1)).encode("utf8"))).decode()
    return result


# 将一张二维码加密后生成新的二维码
def encrpt_qrcode1(key, img):
    url = extract_qrcode(img)
    new_url = encrypt_url(key=key, url=url)
    make_qrcode(url=new_url, name="encrypted.jpg")


# # 给定url生成加密后的二维码
# def encrpt_qrcode2(key, url):
#     make_qrcode(url=url, name="origin.jpg")
#     url = extract_qrcode("origin.jpg")
#     new_url = encrypt_url(key=key, url=url)
#     make_qrcode(url=new_url, name="encrypted.jpg")


# 解密并生成原始二维码
def decrypt_qrcode(key, img):
    D = DES()
    ciphertext = extract_qrcode(img).split()[-1]
    url = D.run(key, (base64.b64decode(ciphertext)).decode(), 0)
    make_qrcode(url=url, name="decrypted.jpg")


if __name__ == '__main__':
    # ========================================== GUI ===================================================
    root = tk.Tk()
    root.title("QRcode Encryption & Decryption")         # 界面的名称、尺寸、背景颜色
    root.geometry("800x500")
    root.configure(background="lightblue")

    def ENCRYPT():
        key = keytext.get()
        path = select_path.get()
        encrpt_qrcode1(key=key, img=path)
        img_open = Image.open("encrypted.jpg")  # 加密后的二维码图片
        img = ImageTk.PhotoImage(img_open.resize((200, 200)))  # 把图片缩放以下，不然太大了，放不下
        created_jpg.config(image=img)
        created_jpg.image = img  # 不加这一行会被python的垃圾回收机制错误回收，也可以把image设为global

    def DECRYPT():
        key = keytext.get()
        path = select_path.get()
        decrypt_qrcode(key=key, img=path)
        img_open = Image.open("decrypted.jpg")      # 解密后的二维码图片
        img = ImageTk.PhotoImage(img_open.resize((200, 200)))  # 把图片缩放以下，不然太大了，放不下
        created_jpg.config(image=img)
        created_jpg.image = img  # 不加这一行会被python的垃圾回收机制错误回收，也可以把image设为global

    # 将选择的图片显示在GUI
    def select_file():
        selected_file_path = filedialog.askopenfilename()  # 使用askopenfilename函数选择单个文件
        select_path.set(selected_file_path)
        img_open = Image.open(select_path.get())
        img = ImageTk.PhotoImage(img_open.resize((200, 200)))  # 把图片缩放以下，不然太大了，放不下
        origin_jpg.config(image=img)
        origin_jpg.image = img  # 不加这一行会被python的垃圾回收机制错误回收，也可以把image设为global


    Label1 = tk.Label(root, text="Key", font="Calibri", bg="lightblue").place(x=280, y=35)
    keytext = tk.Entry(root, width=30)
    keytext.place(x=320,y=40)

    Label2 = tk.Label(root, text="Created QRcode", font="Calibri", bg="lightblue").place(x=580, y=380)
    btn1 = tk.Button(root, text="Encrypt", command=ENCRYPT)
    btn1.place(x=390, y=180)

    btn2 = tk.Button(root, text="Decrypt", command=DECRYPT)
    btn2.place(x=390, y=270)

    Label3 = tk.Label(root, text="Origin QRcode", font="Calibri", bg="lightblue").place(x=113, y=380)

    Label4 = tk.Label(root, text="Choose jpg", font="Calibri", bg="lightblue").place(x=20, y=95)
    select_path = tk.StringVar()
    filename = tk.Entry(root, textvariable=select_path, width=30)
    filename.place(x=120,y=100)
    btn3 = tk.Button(root, text="Select", command=select_file)
    btn3.place(x=342, y=95)

    origin_jpg = tk.Label(root)
    origin_jpg.place(x=80, y=150)
    created_jpg = tk.Label(root)
    created_jpg.place(x=550, y=150)

    root.mainloop()
    # ========================================= GUI ================================================