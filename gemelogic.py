import random
import math

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

    def skaitlaizv(self):
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


    def generate_root(self,spelesac):
        """Ģenerē saknes mezglu ar nejauši izvēlētu skaitli, kas dalās ar 2, 3 un 4."""
        while True:
            value = self.skaitlaizv()
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


if __name__ == "__main__":
    spelessac=str(input("KAS SĀKS SPĒLI, AI OR SP"))
    game = Game(spelessac)

    algorithm=int(input("1)Alfa-Beta    2)Minimax"))
    print(f"Saknes vērtība: {game.root.value}")
    match algorithm:
        case 1:
            print("alfabeta")
            while not game.curentpoz.isfinished():
                if game.curentpoz.gaj_veicejs=="AI":
                    _, game.curentpoz=game.alfabeta(game.curentpoz,99,-math.inf,math.inf,True)
                    # if (game.curentpoz.left is not None): game.curentpoz = game.curentpoz.left 
                    # elif(game.curentpoz.middle is not None): game.curentpoz = game.curentpoz.middle
                    # elif(game.curentpoz.right is not None): game.curentpoz = game.curentpoz.right
                    print("AI: " + str(game.curentpoz.value))
                    print(game.curentpoz.ai_score) 
                    print(game.curentpoz.sp_score)
                    
                else:
                    choice=input("Choose to divide bewteen 2, 3, 4 for number: " + str(game.curentpoz.value) + ": ")
                    if game.curentpoz.value%int(choice)==0:
                        if int(choice)==2: game.curentpoz=game.curentpoz.left
                        if int(choice)==3: game.curentpoz=game.curentpoz.middle
                        if int(choice)==4: game.curentpoz=game.curentpoz.right

                    print("sp: " + str(game.curentpoz.value))
                    print(game.curentpoz.ai_score) 
                    print(game.curentpoz.sp_score)
        case 2:
            print("minimax")
            while not game.curentpoz.isfinished():
        
                if game.curentpoz.gaj_veicejs=="AI":
                    _, game.curentpoz=game.minimaxfunc(game.curentpoz,99,True)
                    # if (game.curentpoz.left is not None): game.curentpoz = game.curentpoz.left 
                    # elif(game.curentpoz.middle is not None): game.curentpoz = game.curentpoz.middle
                    # elif(game.curentpoz.right is not None): game.curentpoz = game.curentpoz.right
                    print("AI: " + str(game.curentpoz.value))
                    print(game.curentpoz.ai_score) 
                    print(game.curentpoz.sp_score)

                else:
                    choice=input("Choose to divide bewteen 2, 3, 4 for number: " + str(game.curentpoz.value) + ": ")
                    if game.curentpoz.value%int(choice)==0:
                        if int(choice)==2: game.curentpoz=game.curentpoz.left
                        if int(choice)==3: game.curentpoz=game.curentpoz.middle
                        if int(choice)==4: game.curentpoz=game.curentpoz.right

                    print("sp: " + str(game.curentpoz.value))
                    print(game.curentpoz.ai_score) 
                    print(game.curentpoz.sp_score)

        case _ :
            print("wrong")
    print("Spēle beidzās!")
    print("Spēlētāja punkti: "+str(game.curentpoz.sp_score)+"  AI punkti: "+str(game.curentpoz.ai_score))
    if game.curentpoz.ai_score>game.curentpoz.sp_score: print("AI wins")
    elif game.curentpoz.ai_score<game.curentpoz.sp_score: print("sp wins")
    else: print("Neizšķirts!")
    




