import os

def read_file():

    dict = {}
    os.chdir("./address")

    with open("email_address.txt","r",encoding="utf-8") as f:
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

    os.chdir("../")
    return dict
    

def update_file(dict):

    os.chdir("./address")

    with open("email_address.txt","w",encoding="utf-8") as f:
        for name,address in dict.items():
            f.write(name + ":" + address + "\n")

    os.chdir("../")

        

def show_info(info):
    for name,addr in info.items():
        print('{}:{}'.format(name,addr))

def show_addr(info):
    for name,addr in info.items():
        print("{}".format(addr))
    
def add_info(info):

    while True:
        
        print('追加する名前を入力してください(終了する場合は0):')
        name = input()
        if(name == '0'):
            break
        print('メールアドレスを入力してください')
        addr = input()
        info[name] = addr
    
def del_info(info):
    while True:
        print('削除する名前を入力してください(終了する場合は0)')
        name = input()
        if(name == '0'):
            break
        del info[name]

def alldel_shelf(f):
    print('本当に削除しますか？(y/n)')
    n = input()
    if(n == 'y'):
        for name in f:
            del f[name]
    else:
        print('通常モードに戻ります')

        
#email_address.txtからコーチ名とアドレスをdictで取得
info = read_file()

while 1:
    
    

    print('操作を選んでください\n')
    print('参照（0）')
    print('追加(1)')
    print('削除(2)')
    print('プログラムを終了(3)')
    print('メールアドレスのみを表示(4)')
    
    n = int(input())

    if n == 0:
        print('0')
        #参照
        show_info(info)
    elif n == 1:
        #追加
        add_info(info)
    elif n == 2:
        #削除
        del_info(info)
    elif n == 4:
        #アドレス表示
        show_addr(info)
    else:
        #操作をファイルに保存する
        update_file(info)

        break

    
