#shelveファイルを参照してメールアドレスのリストを返す関数.未登録ならエラーメールを送信する
from email_programs import error_email

def Create_ToList(d,address,gmail_address,gmail_pass):

    
    
    #送信先リスト
    name_list = []
    #メールアドレス未登録者リスト
    no_name_list = []

    #データベース

    for name in d:
        #名前とメアドが登録されていればname_listに追加
        try:
            name_list.append( str( address[name] ) )
        #名前とメアドが登録されていなければno_name_listに追加
        except KeyError:
            no_name_list.append( str(name))
        
    

    print(name_list)
    print(no_name_list)
    if(len( no_name_list ) != 0):
       error_email.ErrorMail(1,no_name_list,gmail_address,gmail_pass)
        

    return name_list



