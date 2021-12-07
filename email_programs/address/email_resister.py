import os

def read_file(file_name):

    dict = {}

    with open(file_name,"r",encoding="utf-8") as f:
        for line in f:
            #分割できなかった時のエラー処理
            info = line.split(":")

            try:
                name = info[0]
                address = info[1].split("\n")[0]
            except IndexError:
                print("Index Error :ファイルが適切に処理されませんでした")
                name = "NULL"
                address = "NULL"
            
            dict[name] = address

    return dict
    

def update_file(dict,file_name):

    with open(file_name,"w",encoding="utf-8") as f:
        for name,address in dict.items():
            f.write(name + ":" + address + "\n")
        
"""
def show_info(info):
    for name,addr in info.items():
        print('{}:{}'.format(name,addr))

def show_addr(info):
    for name,addr in info.items():
        print("{}".format(addr))
"""
    
def add_info(file_name,first_name,last_name,address):
    info = read_file(file_name)
    name = last_name + " " + first_name
    #受け取った情報を追加
    info[name] = address
    #ファイルへ書き込み
    update_file(info,file_name)

    
def del_info(file_name,info,name):
    
    del info[name]
    #ファイルへ書き込み
    update(info,file_name)


        


