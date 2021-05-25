import os

'''
jpg文件的前两个字节为 pic_head[0], pic_head[1]
png为[2][3]
gif为[4][5]
'''
pic_head = [0xff, 0xd8, 0x89, 0x50, 0x47, 0x49]
decode_code = 0 # 解密码

#判断文件类型，并获取dat文件解密码
def get_code(file_path):    # file_path: dat文件路径

    dat_file = open(file_path, "rb")
    dat_read = dat_file.read(2)
    head_index = 0

    while head_index < len(pic_head):
        #使用第一个头信息字节来计算加密码
        code = dat_read[0] ^ pic_head[head_index]
        idf_code = dat_read[1] ^ code
        head_index = head_index + 1

        #第二个字节来验证解密码是否正确
        if idf_code == pic_head[head_index]:
            dat_file.close()
            return code
        head_index = head_index + 1

    #如果解码成功，则返回解密码，如果文件不是这三种格式则返回0
    print("not jpg, png, gif")
    return 0


def decrypt(file_name, file_path, output_file): #dat文件路径，生成文件路径
    #获取密码
    decode_code = get_code(file_path)
    dat_file = open(file_path, "rb")
    pic_name = output_file + ".jpg"
    pic_write = open(pic_name, "wb")
    #解码
    for dat_data in dat_file:
        for dat_byte in dat_data:
            pic_data = dat_byte ^ decode_code
            pic_write.write(bytes([pic_data]))
    print(file_name + "---解码成功")
    dat_file.close()
    pic_write.close()


def mkdir(path):
    path=path.strip()
    # 去除尾部 \ 符号
    path=path.rstrip("\\")
    # 判断路径是否存在
    isExists=os.path.exists(path)
    if not isExists:
        # 如果不存在则创建目录
        # 创建目录操作函数
        os.makedirs(path)
        print (path + ' 目录创建成功')
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        print (path + ' 目录已存在')
        return False


def find_datfile(dir_path):
    #获取dat文件目录下所有的文件
    files_list = os.listdir(dir_path)
    output_path = dir_path + "\output"
    #在原目录下新建一个output目录
    mkdir(output_path)

    cnt = 0
    succeed = 0
    #对每个文件获取文件名然后解码
    for file_name in files_list:
        #判断文件后缀是否为.dat
        cnt = cnt + 1
        file_type = file_name[-4:]
        if(file_type!=".dat"):
            print(file_name + '---文件不是.dat格式')
            continue
        file_path = dir_path + "\\" + file_name
        output_file = output_path + "\\" +file_name
        decrypt(file_name, file_path, output_file)
        succeed = succeed + 1

    print("==================")
    print("All done!")
    print ("目录下文件共", cnt, "个，成功解码", succeed, "个。")
    print("==================")


path = input("请输入微信dat文件的目录（绝对路径）:")
find_datfile(path)