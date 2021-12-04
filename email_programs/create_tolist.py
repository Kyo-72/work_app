import shelve
import error_email

test = {'清野 恭平':63,'hoge':23}

#shelveファイルを参照してメールアドレスのリストを返す関数.未登録ならエラーメールを送信する

def Create_ToList(d):

    
    shelf_file = shelve.open('email')
    #送信先リスト
    name_list = []
    #メールアドレス未登録者リスト
    no_name_list = []
    

    for name in d:
        #名前とメアドが登録されていればname_listに追加
        try:
            name_list.append( str( shelf_file[name] ) )
        #名前とメアドが登録されていなければno_name_listに追加
        except KeyError:
            no_name_list.append( str(name))
        
    shelf_file.close()

    #print(name_list)
    #print(no_name_list)
    if(len( no_name_list ) != 0):
        error_email.ErrorMail(1,no_name_list)
        

    return name_list



