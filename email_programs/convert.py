TIME_OF_LESSONS = ['12:15','13:50','15:25','17:10','18:45','20:20'] 

#授業開始時間から授業数を割り出し、bitで管理(返り値は0～63)
def Convert_To_Bit(list):

    lesson_bit = 0
    
    for i in list:

        for j in range(6):
        
            if(i == TIME_OF_LESSONS[j]):
                #print('ditected{}'.format(j))
                lesson_bit = lesson_bit | (1 << j)
    #print(lesson_bit)
    return lesson_bit

        
