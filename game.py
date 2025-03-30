import random
import math
import tkinter as tk

class Node:
    def __init__(self, value, ai_score, sp_score, parent=None, gaj_veicejs=None):
        self.value = value
        self.left = None  # Dalās ar 2
        self.middle = None  # Dalās ar 3
        self.right = None  # Dalās ar 4
        self.parent = parent
        self.ai_score = ai_score
        self.sp_score = sp_score
        self.gaj_veicejs = gaj_veicejs  # Kurš spēlētājs veica gājienu

    def isfinished(self):
        if self.value<=10: return True
        if (self.value%2!=0 and self.value%3!=0 and self.value%4!=0): return True
        return False

    def heristic(self):
        if self.ai_score>self.sp_score: return 1
        elif self.ai_score<self.sp_score: return -1
        elif self.ai_score==self.sp_score: return 0

    def childgeneration(self, recursive=False):
        """
        Ģenerē bērnus, ja iespējams dalīt skaitli ar 2, 3 vai 4.
        Atjauno punktus atkarībā no tā, vai rezultāts ir pāra vai nepāra skaitlis.
        Ja recursive=True, tad rekursīvi veido visus iespējamos spēles gājienus.
        """
        for divisor in [2, 3, 4]: 
            if self.value % divisor == 0:
                new_value = self.value // divisor
                new_ai_score = self.ai_score
                new_sp_score = self.sp_score
            
                
                # Punktu sistēma
                if new_value % 2 == 0:
                    if self.gaj_veicejs == "AI":
                        new_sp_score -= 1  # Atņem pretinieka punktus
                    else:
                        new_ai_score -= 1
                else:
                    if self.gaj_veicejs == "AI":
                        new_ai_score += 1  # Piešķir punktu sev
                    else:
                        new_sp_score += 1
                
                # Nosaka nākamo gājiena veicēju
                next_player = "AI" if self.gaj_veicejs == "SP" else "SP"
                
                # Izveido jaunu mezglu
                child = Node(new_value, new_ai_score, new_sp_score, self, next_player)
                
                # Pievieno bērnu koka struktūrai
                if divisor == 2:
                    self.left = child
                elif divisor == 3:
                    self.middle = child
                elif divisor == 4:
                    self.right = child
                
                # Rekursīvi izsauc childgeneration, ja nepieciešams
                if recursive and new_value > 10:
                    child.childgeneration(recursive=True)


class Game:
    def __init__(self,spelessacejs="AI"):
        self.root = self.generate_root(spelessacejs)
        self.root.childgeneration(recursive=True)
        self.curentpoz=self.root
        
    def generate_numb(self):
        numbers=[]
        while len(numbers)<5:
            num=random.randint(20000, 30000)
            if num%3==0 and num%2==0 and num%4==0:
                numbers.append(num)

        return numbers

    #def skaitlaizv(self):
        skaitļi=self.generate_numb()
        print("uzģenerētie skaitļi:")
        for i in range(1,6):
            print(i,") ", skaitļi[i-1])
        izveletaopcija=int(input("izvēlaties opciju: "))
        while izveletaopcija>5 or izveletaopcija<1:
            izveletaopcija=int(input("izvēlaties pareizu opciju ''1 2 3 4 5'' :"))
        izveletaisskaitlis=skaitļi[izveletaopcija-1]
        print(izveletaisskaitlis)
        return izveletaisskaitlis
    def skaitlaizv(self):
        uniVar.set("Choose starting number")
        izveletaisskaitlis1=tk.DoubleVar()
        skaitļi=self.generate_numb()
        rand1=tk.Button(root,text=skaitļi[0], width=15, bd=10, bg="black", fg="white",command=lambda:(izveletaisskaitlis1.set(skaitļi[0])))
        rand2=tk.Button(root,text=skaitļi[1], width=15, bd=10, bg="black", fg="white",command=lambda:(izveletaisskaitlis1.set(skaitļi[1])))
        rand3=tk.Button(root,text=skaitļi[2], width=15, bd=10, bg="black", fg="white",command=lambda:(izveletaisskaitlis1.set(skaitļi[2])))
        rand4=tk.Button(root,text=skaitļi[3], width=15, bd=10, bg="black", fg="white",command=lambda:(izveletaisskaitlis1.set(skaitļi[3])))
        rand5=tk.Button(root,text=skaitļi[4], width=15, bd=10, bg="black", fg="white",command=lambda:(izveletaisskaitlis1.set(skaitļi[4])))
        rand1.place(x=WIDTH/6.66,y=HEIGHT/2)
        rand2.place(x=WIDTH/3.33,y=HEIGHT/2)
        rand3.place(x=WIDTH/2.22,y=HEIGHT/2)
        rand4.place(x=WIDTH/1.66,y=HEIGHT/2)
        rand5.place(x=WIDTH/1.33,y=HEIGHT/2)
        root.wait_variable(izveletaisskaitlis1)
        rand1.place_forget()
        rand2.place_forget()
        rand3.place_forget()
        rand4.place_forget()
        rand5.place_forget()
        izveletaisskaitlis=int(izveletaisskaitlis1.get())
        print(izveletaisskaitlis)
        return izveletaisskaitlis

    def generate_root(self,spelesac):
        """Ģenerē saknes mezglu ar nejauši izvēlētu skaitli, kas dalās ar 2, 3 un 4."""
        while True:
            value =self.skaitlaizv()
            return Node(value, 0, 0, None, spelesac)
        

    def alfabeta(self,pozit, depth,alpha,beta, isMaximising=True):
        if depth==0 or pozit.isfinished():
            return pozit.heristic(), pozit

        children=[child for child in [pozit.left, pozit.middle, pozit.right] if child is not None]
        best_move = children[0]

        if isMaximising:
            bestscore=-math.inf
            for child in children:
                score,move=self.alfabeta(child, depth-1,alpha,beta,False)
                bestscore=max(score, bestscore)
                alpha=max(alpha,score)
                if beta<=alpha:
                    break
                if (score > bestscore): best_move = move
            return bestscore, best_move
        else:
            bestscore= +math.inf
            for child in children:
                score,move=self.alfabeta(child, depth-1,alpha,beta,True)
                bestscore=min(score, bestscore)
                beta=min(beta,score)
                if beta<=alpha:
                    break
                if (score < bestscore): best_move = move
            return bestscore, best_move

    
    def minimaxfunc(self,pozit, depth, isMaximising=True):
        if depth==0 or pozit.isfinished():
            return pozit.heristic(), pozit

        children=[child for child in [pozit.left, pozit.middle, pozit.right] if child is not None]
        best_move = children[0]

        if isMaximising:
            bestscore=-math.inf
            for child in children:
                score,move=self.minimaxfunc(child, depth-1,False)
                bestscore=max(score, bestscore)
                if (score > bestscore): best_move = move
            return bestscore, best_move
        else:
            bestscore= +math.inf
            for child in children:
                score,move=self.minimaxfunc(child, depth-1,True)
                bestscore=min(score, bestscore)
                if (score < bestscore): best_move = move
            return bestscore, best_move
        



def restart():
    spelessac.set(None)
    algorithm.set(None)
    aiScore.place_forget()
    spScore.place_forget()
    reStart.place_forget()
    aiVar.set("AI score"+"\n"+"0")
    spVar.set("Sp score"+"\n"+"0")

    game=None


    destroy_buttons()
    start_game()
 
    
    



def start_game():
    start.place_forget()
    uniVar.set("Choose who is starting")
    Ai = tk.Button(root, text="AI", width=15, bd=10, bg="black", fg="white",command=lambda: (spelessac.set("AI"),Sp.place_forget(),Ai.place_forget()))
    Ai.place(x=WIDTH/2.5, y=HEIGHT/2)

    Sp = tk.Button(root, text="SP", width=15, bd=10, bg="black", fg="white",command=lambda: (spelessac.set("SP"),Sp.place_forget(),Ai.place_forget()))         
    Sp.place(x=WIDTH/1.81, y=HEIGHT/2) 
    root.wait_variable(spelessac)

    gameproc()


def gameproc():
        #spelessac=str(input("KAS SĀKS SPĒLI, AI OR SP: "))
   
   
    global game 
    game= Game(spelessac.get())

   

    uniVar.set("Choose algorithm:")
    algMIN.place(x=WIDTH/3, y=HEIGHT/2)
    algALFA.place(x=WIDTH/1.9, y=HEIGHT/2)

    #algorithm=int(input("1)Alfa-Beta    2)Minimax"))

def alfaBeta():
    """Palaiž algoritmu un veic pirmo gājienu"""
    print("alfabeta")
    algALFA.place_forget()
    algMIN.place_forget()
    
    aiScore.place(x=WIDTH/10,y=HEIGHT/6)
    spScore.place(x=WIDTH/1.35,y=HEIGHT/6)
    uniVar.set("Skaitlis: "+str(game.curentpoz.value))
    
    # Pievienojam nelielu aizkavi pirms pirmā process_turn() izsaukuma
    root.after(300, process_turn)

def process_turn():
    """Apstrādā AI vai spēlētāja gājienu"""
    if game.curentpoz.isfinished():
        aiVar.set("AI score"+"\n"+str(game.curentpoz.ai_score))
        spVar.set("Sp score"+"\n"+str(game.curentpoz.sp_score))
        if game.curentpoz.ai_score > game.curentpoz.sp_score: 
            uniVar.set("Ai won!")
        elif game.curentpoz.ai_score < game.curentpoz.sp_score: 
            uniVar.set("Spēlētājs uzvarēja!")
        else: 
            uniVar.set("Neizšķirts!")
        reStart.place(x=WIDTH/2.1,y=HEIGHT/2)

        return

    print("Pašreizējais gājējs:", game.curentpoz.gaj_veicejs)

    if game.curentpoz.gaj_veicejs == "AI":
        print("AI veic gājienu...")
        _, game.curentpoz = game.alfabeta(game.curentpoz, 99, -math.inf, math.inf, True)
        print("AI izvēlējās:", game.curentpoz.value)
        aiVar.set("AI score"+"\n"+str(game.curentpoz.ai_score))
        spVar.set("Sp score"+"\n"+str(game.curentpoz.sp_score))
        uniVar.set("Skaitlis: "+str(game.curentpoz.value))
        
        root.after(600, process_turn)  # Pēc nelielas aizkaves veicam nākamo gājienu
    else:
        print("Gaida spēlētāja gājienu...")
        create_buttons()

def create_buttons():
    """Izveido izvēles pogas spēlētājam"""
    global leftBtn, middleBtn, rightBtn

    leftBtn = tk.Button(root, text="/2", width=15, bd=10, bg="black", fg="white",
                        command=lambda: player_choice(game.curentpoz.left))
    middleBtn = tk.Button(root, text="/3", width=15, bd=10, bg="black", fg="white",
                          command=lambda: player_choice(game.curentpoz.middle))
    rightBtn = tk.Button(root, text="/4", width=15, bd=10, bg="black", fg="white",
                         command=lambda: player_choice(game.curentpoz.right))

    leftBtn.place(x=WIDTH/4, y=300)
    middleBtn.place(x=WIDTH/2, y=300)
    rightBtn.place(x=WIDTH/1.3, y=300)

def player_choice(new_position):
    """Apstrādā spēlētāja izvēli"""
    if new_position:
        game.curentpoz = new_position

        uniVar.set("Skaitlis: "+str(game.curentpoz.value))
        destroy_buttons()
        root.after(600, process_turn)  # Pēc izvēles veicam nākamo gājienu

def destroy_buttons():
    """Noņem izvēles pogas pēc izvēles izdarīšanas"""
    leftBtn.place_forget()
    middleBtn.place_forget()
    rightBtn.place_forget()

def minMax():
    """Palaiž Minimax algoritmu un veic pirmo gājienu"""
    print("MINMAX")
    algALFA.place_forget()
    algMIN.place_forget()

    aiScore.place(x=WIDTH/10,y=HEIGHT/6)
    spScore.place(x=WIDTH/1.35,y=HEIGHT/6)
    uniVar.set("Skaitlis: "+str(game.curentpoz.value))

    
    
    # Pievienojam nelielu aizkavi pirms pirmā process_minmax_turn() izsaukuma
    root.after(600, process_minmax_turn)    

def process_minmax_turn():
    """Apstrādā AI vai spēlētāja gājienu Minimax algoritmam"""
    if game.curentpoz.isfinished():
        aiVar.set("AI score"+"\n"+str(game.curentpoz.ai_score))
        spVar.set("Sp score"+"\n"+str(game.curentpoz.sp_score))
        if game.curentpoz.ai_score > game.curentpoz.sp_score: 
            uniVar.set("AI uzvarēja!")
        elif game.curentpoz.ai_score < game.curentpoz.sp_score: 
            uniVar.set("Spēlētājs uzvarēja!")
        else: 
            uniVar.set("Neizšķirts!")
        reStart.place(x=WIDTH/2.1,y=HEIGHT/3)
        return

    print("Pašreizējais gājējs:", game.curentpoz.gaj_veicejs)

    if game.curentpoz.gaj_veicejs == "AI":
        print("AI veic gājienu...")
        _, game.curentpoz = game.minimaxfunc(game.curentpoz, 99, True)
        print("AI izvēlējās:", game.curentpoz.value)

        aiVar.set("AI score"+"\n"+str(game.curentpoz.ai_score))
        spVar.set("Sp score"+"\n"+str(game.curentpoz.sp_score))
        uniVar.set("Skaitlis: "+str(game.curentpoz.value))
        
        root.after(600, process_minmax_turn)  # Pēc nelielas aizkaves veicam nākamo gājienu
    else:
        print("Gaida spēlētāja gājienu...")
        create_buttons()




if __name__ == "__main__":
    
    root = tk.Tk()
    root.title("Game")
    root.geometry('1500x600')
    spelessac=tk.StringVar()
    algorithm=tk.IntVar()
    WIDTH=1500
    HEIGHT=600
    canvas = tk.Canvas(root, width=WIDTH,height=HEIGHT,bg="black")
    canvas.place(x=-1,y=0)
    uniVar=tk.Variable()
    label=tk.Label(root,textvariable=uniVar,bg="black",font=("Terminal",24),fg="white")

    label.place(x=WIDTH/3, y=HEIGHT/6)
    
    aiVar=tk.Variable()
    aiVar.set("AI Score")
    spVar=tk.Variable()
    spVar.set("SP Score")
    algMIN = tk.Button(root,text="MINMAX",width=15,bd=10,bg="black",fg="white",command=lambda:(minMax()))
    algALFA = tk.Button(root,text="Alfa-Beta",width=15,bd=10,bg="black",fg="white",command=lambda:(alfaBeta()))

    aiScore=tk.Label(root,textvariable=aiVar,bg="black",font=("Terminal",30),fg="white")
    spScore=tk.Label(root,textvariable=spVar,bg="black",font=("Terminal",30),fg="white")
    reStart=tk.Button(root,text='Restart',width=15,bd=10,bg="black",fg="white",command=lambda:restart())


    start=tk.Button(root,text='Start',width=15,bd=10,bg="black",fg="white",command=start_game)
    start.place(x=WIDTH/2.1,y=HEIGHT/2)
    
    



    
    
    



   
    root.mainloop()
    




