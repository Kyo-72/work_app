TIME_OF_LESSONS = ['12:20','13:55','15:30','17:20','18:55','20:30'] 

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

        
