# QRcode Encryption

## Language & Environment

（1）Language

     Python
     
（2）Environment

     Python version：python 3.8
     
     IDE：PyCharm Professional 2020

## Introduction
The QR code is actually the encryption of a URL. Sometimes we want to share a URL through QR code, such as our own personal homepage or WeChat, 
but it is easy for unrelated people to get this URL through mass sending. This project can encrypt the url contained in the QR code through the DES encryption algorithm. 
Only through a specific key can the content be cracked, thus protecting the user's privacy.
     
## Usage

The selected pictures and generated pictures will be saved in the project directory and displayed in the GUI.

### To encrypt
1. Run main.py
2. Input a key
3. Click ```Select``` to choose a QRcode picture(jpg file which contains an url) that you want to encrypt.
4. Click ```Encrypt``` to generate an encrypted QRcode(the url was encrypted)

![image](https://user-images.githubusercontent.com/80464792/201864037-cbdd7c89-6b85-4e68-aa99-9eabf8b49b9e.png)
![image](https://user-images.githubusercontent.com/80464792/201864125-eb7f253c-d704-4abb-9cd9-85d9c9276bbe.png)


### To decrpte
1. Run main.py
2. Input the same key
3. Click ```Select``` to choose the encrypted QR code picture
4. Click ```Decrypt``` to generate the origin QR code

![image](https://user-images.githubusercontent.com/80464792/201864156-d1dda31c-bd07-4084-af02-59494d48e101.png)

