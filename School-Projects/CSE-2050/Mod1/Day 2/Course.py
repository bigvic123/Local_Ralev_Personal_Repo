class CSE2050:
    teacher = " Lina " # class variable
    def __init__ (self, name, id):
        self.st_name = name
        self.st_id = id
        self.scores = []
        self.__student_num = 200 #private var var

    def add_score(self, score):
        self.scores.append(score)

    def get_info(self):
        return "Student name: " + self.st_name

    def __str__(self):
        return "Student name: "+ self.st_name + "student id: "+ str(self.st_id)

if __main__ == "__name__":
    st1 = CSE2050("John Smith", 456)
    print(st1.st_name)
    st1.add_score(100)
    st1.add_score(90)
    print(st1.get_scores)
    print(st1.get_info())

    st2 = CSE2050("Amma Walker", 444)
    
    str(st2)