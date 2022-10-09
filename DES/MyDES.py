import base64
import tkinter as tk

# 初始置换IP
IP = [58, 50, 42, 34, 26, 18, 10, 2,
      60, 52, 44, 36, 28, 20, 12, 4,
      62, 54, 46, 38, 30, 22, 14, 6,
      64, 56, 48, 40, 32, 24, 16, 8,
      57, 49, 41, 33, 25, 17, 9, 1,
      59, 51, 43, 35, 27, 19, 11, 3,
      61, 53, 45, 37, 29, 21, 13, 5,
      63, 55, 47, 39, 31, 23, 15, 7]

# 32位密钥通过置换-->48位
E = [32, 1, 2, 3, 4, 5,
     4, 5, 6, 7, 8, 9,
     8, 9, 10, 11, 12, 13,
     12, 13, 14, 15, 16, 17,
     16, 17, 18, 19, 20, 21,
     20, 21, 22, 23, 24, 25,
     24, 25, 26, 27, 28, 29,
     28, 29, 30, 31, 32, 1]

                                        # Key 初始置换选择1
                                        # 去除64位密钥中作为奇偶校验位的第 8、16、24、32、40、48、56、64位
CP_1 = [57, 49, 41, 33, 25, 17, 9,
        1, 58, 50, 42, 34, 26, 18,
        10, 2, 59, 51, 43, 35, 27,
        19, 11, 3, 60, 52, 44, 36,
        63, 55, 47, 39, 31, 23, 15,
        7, 62, 54, 46, 38, 30, 22,
        14, 6, 61, 53, 45, 37, 29,
        21, 13, 5, 28, 20, 12, 4]

                                        # KEY 置换选择2
CP_2 = [14, 17, 11, 24, 1, 5, 3, 28,
        15, 6, 21, 10, 23, 19, 12, 4,
        26, 8, 16, 7, 27, 20, 13, 2,
        41, 52, 31, 37, 47, 55, 30, 40,
        51, 45, 33, 48, 44, 49, 39, 56,
        34, 53, 46, 42, 50, 36, 29, 32]

                                         # 密钥生成的移位次数表
SHIFT = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]

                                        # SBOX
S_BOX = [

    [[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
     [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
     [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
     [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13],
     ],

    [[15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
     [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
     [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
     [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9],
     ],

    [[10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
     [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
     [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
     [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12],
     ],

    [[7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
     [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
     [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
     [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14],
     ],

    [[2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
     [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
     [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
     [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3],
     ],

    [[12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
     [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
     [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
     [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13],
     ],

    [[4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
     [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
     [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
     [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12],
     ],

    [[13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
     [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
     [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
     [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11],
     ]
]

                                         # P盒置换
P = [16, 7, 20, 21, 29, 12, 28, 17,
     1, 15, 23, 26, 5, 18, 31, 10,
     2, 8, 24, 14, 32, 27, 3, 9,
     19, 13, 30, 6, 22, 11, 4, 25]

                                         # 初始逆置换
IP_1 = [40, 8, 48, 16, 56, 24, 64, 32,
        39, 7, 47, 15, 55, 23, 63, 31,
        38, 6, 46, 14, 54, 22, 62, 30,
        37, 5, 45, 13, 53, 21, 61, 29,
        36, 4, 44, 12, 52, 20, 60, 28,
        35, 3, 43, 11, 51, 19, 59, 27,
        34, 2, 42, 10, 50, 18, 58, 26,
        33, 1, 41, 9, 49, 17, 57, 25]


def string_to_bit_array(text):  # 字符串-->bit数组
    array = list()
    for char in text:
        binval = binvalue(char, 8)  # 获得每个字符的二进制
        array.extend([int(x) for x in list(binval)])
    return array

def binvalue(val, bitsize):  # 以给定大小的字符返回二进制值
    binval = bin(val)[2:] if isinstance(val, int) else bin(ord(val))[2:]
    if len(binval) > bitsize:
        raise Exception("binary value larger than the expected size")
    while len(binval) < bitsize:  # 不满8位用0补齐
        binval = "0" + binval
    return binval


def nsplit(s, n):                        # 将列表拆分为大小为'n'的子列表
    return [s[k:k + n] for k in range(0, len(s), n)]


def bit_array_to_string(array):          # bit数组-->字符串
    res = ''.join([chr(int(y, 2)) for y in [''.join([str(x) for x in bytes]) for bytes in nsplit(array, 8)]])
    return res


ENCRYPT = 1
DECRYPT = 0


class DES():
    def __init__(self):
        self.password = None  # 存放初始key
        self.text = None      # 存放明文
        self.keys = list()    # 存放key值列表集合

    def run(self, key, text, action):

        self.password = key
        self.text = text

        if action == ENCRYPT:
            self.addPadding()

        text_blocks = nsplit(self.text, 8)
        self.generatekeys()   # 生成密钥

        result = list()

        for block in text_blocks:               # 遍历所有数据块
            block = string_to_bit_array(block)
            block = self.permutation(block, IP)      # 数据块的初始置换
            L, R = nsplit(block, 32)                 # 数据块分片(L0 和 R0)

            tmp = None
            for i in range(16):                 # 16轮迭代
                R_E = self.permutation(R, E)         # R0的扩展 32bit-->48bit

                if action == ENCRYPT:
                    tmp = self.XOR(self.keys[i], R_E)
                else:
                    tmp = self.XOR(self.keys[15-i], R_E)

                tmp = self.sbox_zip(tmp)        # S盒代换 48bit-->32bit
                tmp = self.permutation(tmp, P)  # P盒置换
                tmp = self.XOR(L, tmp)          # 和L0进行异或
                L = R
                R = tmp
            result += self.permutation(R+L, IP_1)      # 这里是R+L 因为前面交换过了 被坑惨了！！！

        final_res = bit_array_to_string(result)
        if action == DECRYPT:
            return self.removePadding(final_res)            # 如果在解密 删除填充
        else:
            return final_res

    def permutation(self, block, table):     # 所有的置换
        return [block[x-1] for x in table]   # 初始置换、32位密钥扩展到48位等

    def XOR(self, l1, l2):                          # 两列表异或,返回结果列表
        return [x ^ y for x, y in zip(l1, l2)]

    def shift(self, g, d, n):                       # 每轮key值产生所需的函数
        return g[n:] + g[:n], d[n:] + d[:n]

    def addPadding(self):                           # 使用 PKCS5 进行数据的填充,不管是否是BlockSize的整数倍都需要进行填充
        pad_len = 8 - (len(self.text) % 8)
        self.text += pad_len * chr(pad_len)

    def removePadding(self, data):                  # 删除纯文本的填充
        pad_len = ord(data[-1])
        return data[:-pad_len]

    def generatekeys(self):                         # 子密钥生成 16轮迭代所以需要16个子密钥
        self.keys = []
        key = string_to_bit_array(self.password)
        key = self.permutation(key, CP_1)                   # 置换选择1 初始化key 压缩为56bit
        C, D = nsplit(key, 28)                              # 密钥分片 (C0, D0)
        for i in range(16):                                 # 16轮循环,因为要生成16个子密钥
            C, D = self.shift(C, D, SHIFT[i])               # C0,D0分别进行移位操作
            tmp = C + D                                     # 合并 28bit+28bit-->56bit
            self.keys.append(self.permutation(tmp, CP_2))   # 置换选择2 56bit-->48bit

    def sbox_zip(self, tmp):
        lst = nsplit(tmp, 6)
        result = list()
        for i in lst:  # 48位比特 对于每6位比特
            row = int(str(i[0]) + str(i[-1]), 2)  # 首尾拼接的二进制数 转换为十进制 即行数
            col = int(str(i[1]) + str(i[2]) + str(i[3]) + str(i[4]), 2)  # 中间四位二进制数 转换为十进制 即列数
            res = S_BOX[lst.index(i)][row][col]
            bin_num = binvalue(res, 4)
            result += [int(x) for x in bin_num]
        return result


if __name__ == '__main__':
    # =========================================MyDES GUI===================================================
    root = tk.Tk()
    root.title("MyDES GUI")         # 界面的名称、尺寸、背景颜色
    root.geometry("800x500")
    root.configure(background="lightblue")

    def ENCRYPT():
        key = keytext.get()
        text = plaintext.get("1.0", tk.END).strip('\n')    # 去掉结尾的换行符 否则会占一个字符
        D = DES()
        C = (base64.b64encode((D.run(key, text, ENCRYPT)).encode("utf8"))).decode()  # 加密
        answertext.delete(1.0, tk.END)
        answertext.insert(tk.INSERT, C)

    def DECRYPT():
        key = keytext.get()
        text = plaintext.get("1.0", tk.END).strip('\n')
        D = DES()
        answertext.delete(1.0, tk.END)
        answertext.insert(tk.INSERT, D.run(key, (base64.b64decode(text)).decode(), DECRYPT))  # 解密

    def clear1():  # 清除plaintext文本框
        plaintext.delete(1.0, tk.END)

    def clear2():  # 清除ciphertext文本框
        answertext.delete(1.0, tk.END)


    Label1 = tk.Label(root, text="Key", font="Calibri", bg="lightblue").place(x=280, y=35)
    keytext = tk.Entry(root, width=30)
    keytext.place(x=320,y=40)

    plaintext = tk.Text(root, width=60, height=8)
    plaintext.place(x=220, y=100)
    Label2 = tk.Label(root, text="Plain Text", font="Calibri", bg="lightblue").place(x=128, y=130)
    btn1 = tk.Button(root, text="Encrypt", command=ENCRYPT)
    btn1.place(x=280, y=240)

    btn2 = tk.Button(root, text="Decrypt", command=DECRYPT)
    btn2.place(x=530, y=240)

    Label3 = tk.Label(root, text="Cipher Text", font="Calibri", bg="lightblue").place(x=113, y=325)
    answertext = tk.Text(root, width=60, height=8)
    answertext.place(x=220, y=300)

    btn3 = tk.Button(root, text="Clear", command=clear1).place(x=700, y=140)
    btn4 = tk.Button(root, text="Clear",command=clear2).place(x=700, y=345)


    root.mainloop()
    # ========================================MyDES GUI================================================
