import shelve

def show_shelf(f):
    for name,addr in f.items():
        print('{}:{}'.format(name,addr))

def show_addr(f):
    for name,addr in f.items():
        print("{}".format(addr))
    
def add_shelf(f):

    while True:
        
        print('追加する名前を入力してください(終了する場合は0):')
        name = input()
        if(name == '0'):
            break
        print('メールアドレスを入力してください')
        addr = input()
        f[name] = addr
    
def del_shelf(f):
    while True:
        print('削除する名前を入力してください(終了する場合は0)')
        name = input()
        if(name == '0'):
            break
        del f[name]

def alldel_shelf(f):
    print('本当に削除しますか？(y/n)')
    n = input()
    if(n == 'y'):
        for name in f:
            del f[name]
    else:
        print('通常モードに戻ります')

shelf_file = shelve.open('email')

while 1:
    

    print('操作を選んでください\n')
    print('参照（0）')
    print('追加(1)')
    print('削除(2)')
    print('プログラムを終了(3)')
    print('メールアドレスのみを表示(4)')
    print('keyを全て削除(112233)')

    n = int(input())
    
    if n == 0:
        print('0')
        show_shelf(shelf_file)
    elif n == 1:
        add_shelf(shelf_file)
    elif n == 2:
        del_shelf(shelf_file)
    elif n == 4:
        show_addr(shelf_file)
    elif n == 112233:
        alldel_shelf(shelf_file)
    else:
        break


    
shelf_file.close()   

