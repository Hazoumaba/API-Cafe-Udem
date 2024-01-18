###############################################################################
## Programme qui éxecute une API simple en Python permettant d'envoyer 
## des requêtes aux cafés étudiants de l'UdeM
###############################################################################
## Auteur: Ben Amor Hazem
## Date: 29/04/2023
## Email: hazem.ben.amor@umontreal.ca
###############################################################################
#Nb:Le code est fait sans le module re(regex) car 70% du programme est fait 
#avant les examens finales c'est à dire avant le dernier email du professeur
###############################################################################
 

#Importation des modules nécessaires
import datetime #Ce module sert à afficher la date exacte qui sera pratique dans la 2eme requete du staff
import json
#Ce module permet d'ouvrir un fichier 
def read_file(path):
    file = open(path,"rt")
    content = file.read()
    return content
#Ce module permet d'écrire dans un fichier 
def write_file(path,content):
    file = open(path,"wb")
    file.write(content.encode("utf-8"))
#Ce module permet d'initialiser le programme c'est à dire permet l'utilisateur de se connecter 
def initialisation():
    repeat=True 
    cond=False
    while repeat:  #Simple controle de donnée qui permet d'entrer une maticule et mot de passe valides
        matricule=input("Entrez votre matricule : ")
        mdp=input("Entre votre mot de passe : ")
        content=read_file("comptes.csv")
        with open("comptes.csv","rt") as fichier:   #Cette instruction permet de lire un fichier ligne par ligne et remplir un tableau au fur et a mesure en suivant 
                                                    #le symbole |
            for ligne in fichier:
                if (ligne.find(matricule)!=-1) and (len(matricule)==len((ligne[0:(ligne.find("|"))].strip()))):
                    tab=(ligne.split("|"))
                    for i in range(len(tab)):
                        tab[i]=tab[i].strip()
                    cond=True
        if (cond==False) or (tab[3]!=mdp):#SI la condition est fausse il faut réentrer les données
            print("Vérifier vos données")
            cond=False
            repeat=True
        elif tab[6]=="0": 
            print("Ce compte n'est plus actif. Veuillez contacter les administrateurs pour modifier le statut du compte")
            exit()
        else:
            repeat=False
    return tab
#Ce module permet de tranformer un dictionnaire en une liste 
def getList(dict):
    list = []
    for key in dict.keys():
        list.append(key)
    return list
         
#Ce module permet d'afficher les données sous forme tabulaire 
def affiche(tab):
    msg=""
    for i in range (len(tab)):
        msg=msg+tab[i]+"\n"
    return msg
#Ce module permet de traiter la 1ere et la 2eme requete du role public
def req1_2(req,contenu,tab1):#tab1=initialisation()
    tab=[]
    #La liste ci dessous contient tout les categories possibles
    listcat=["boisson","boisson_chaude","cafe","the","chocolat","boisson_froide","sandwich","regulier","wrap","fruit","viennoiserie","pain","chausson","croissant","muffin"]
    cond1=(req=="GET /api/menu/items")  #condition sur la requete 1
    cond2=((req[req.find("/menu/")+6:req.find("/items")]) in listcat) #condition sur la requete 2
    #Ces conditions ci dessous permettent de distinguer entre les requetes
    if cond1:
        cond=True
    elif cond2 :
        cat=(req[req.find("/menu/")+6:req.find("/items")])
        tab=[]
    #La boucle ci dessous permettent d'accéder au éléments du menu.json et remplir le tableau tab avec les données requises pour la requete seulement 
    for l in range(len(contenu)):
        a=getList(contenu)[l]
        for z in range(len((contenu[a]))):
            b=getList(contenu[a])[z]
            for k in range (len((contenu[a][b]))) :
                if (req!="GET /api/menu/items"):        #tout les conditons permettent de distinguer entre les requetes 1 et 2
                    cond=(a==cat)
                if isinstance(contenu[a][b],list) and cond:
                    tab.append((str(contenu[a][b][k]["id"]))+" | "+contenu[a][b][k]["nom"])
                elif isinstance(contenu[a][b],list):
                    continue  
                else:
                    c=getList(contenu[a][b])[k]
                    for j in range (len((contenu[a][b][c]))):
                        if (req!="GET /api/menu/items"):
                            cond=(a==cat or b==cat or c==cat)
                        if isinstance(contenu[a][b][c],list) and cond :
                            tab.append((str(contenu[a][b][c][j]["id"])+" | "+contenu[a][b][c][j]["nom"]))
                        elif isinstance(contenu[a][b][c],list):
                            continue
                        else:
                            d=getList(contenu[a][b][c])[j]
                            for i in range(len(contenu[a][b][c][d])):
                                if (req!="GET /api/menu/items"):
                                    cond=(a==cat or b==cat or c==cat or d==cat)
                                if cond:
                                    tab.append((str(contenu[a][b][c][d][i]["id"]))+" | "+contenu[a][b][c][d][i]["nom"])
        
    return affiche(tab) #c'est le module déclaré toute en haut 


#Ce module permet de traiter la 3eme requete du role public et role staff
def req3(req,contenu):  
    if req[0:3]=="PUT": #Cette condition est utilisé car ce module est utile dans la requete 3 du role staff pour distiguer entre les 2 requetes
        id1=(req[req.find("/items/")+7:req.find("disponible")])
    else:
        id1=(req[req.find("/items/")+7::])
    for l in range(len(contenu)):
        a=getList(contenu)[l]
        for z in range(len((contenu[a]))):
            b=getList(contenu[a])[z]
            for k in range (len((contenu[a][b]))):
                if isinstance(contenu[a][b],list):
                    if (contenu[a][b][k]["id"])==int(id1):
                        if req[0:3]=="PUT":
                            if req[req.find("=")+1::]=="0":
                                contenu[a][b][k]["disponible"]="false"
                            else:
                                contenu[a][b][k]["disponible"]="true"
                            with open("menu.json", "w", encoding='utf8') as f:
                                json.dump(contenu, f)                           #L'instruction principale pour Mettre à jour la valeur du champ 'disponible' d'un item donné.
                        msg=str(contenu[a][b][k]["id"])+" | "+str(contenu[a][b][k]["nom"])+" | "+str(contenu[a][b][k]["prix"])+" | "+("disponible" if str(contenu[a][b][k]["disponible"])=="True" else "non disponible")
                        prix=str(contenu[a][b][k]["prix"])
                        nom=str(contenu[a][b][k]["nom"])

                else:
                    c=getList(contenu[a][b])[k]
                    for j in range (len((contenu[a][b][c]))):
                        if isinstance(contenu[a][b][c],list):
                            if (contenu[a][b][c][j]["id"])==int(id1):
                                if req[0:3]=="PUT":
                                    if req[req.find("=")+1::]=="0":
                                        contenu[a][b][c][j]["disponible"]="false"
                                    else:
                                        contenu[a][b][c][j]["disponible"]="true"
                                    with open("menu.json", "w", encoding='utf8') as f:
                                        json.dump(contenu, f)
                                nom=str(contenu[a][b][c][j]["nom"])
                                prix=str(contenu[a][b][c][j]["prix"])
                                msg=str(contenu[a][b][c][j]["id"])+" | "+str(contenu[a][b][c][j]["nom"])+" | "+str(contenu[a][b][c][j]["prix"])+" | "+("disponible" if str(contenu[a][b][c][j]["disponible"])=="True" else "non disponible")
                   
                        else:
                            d=getList(contenu[a][b][c])[j]
                            for i in range(len(contenu[a][b][c][d])):
                                if (contenu[a][b][c][d][i]["id"])==int(id1):
                                    if req[0:3]=="PUT":
                                        if req[req.find("=")+1::]=="0":
                                            contenu[a][b][c][d][i]["disponible"]="false"
                                        else:
                                            contenu[a][b][c][d][i]["disponible"]="true"
                                        with open("menu.json", "w", encoding='utf8') as f:
                                            json.dump(contenu, f)                           
                                    nom=str(contenu[a][b][c][d][i]["nom"])
                                    prix=str(contenu[a][b][c][d][i]["prix"])
                                    msg=str(contenu[a][b][c][d][i]["id"])+" | "+str(contenu[a][b][c][d][i]["nom"])+" | "+str(contenu[a][b][c][d][i]["prix"])+" | "+("disponible" if str(contenu[a][b][c][d][i]["disponible"])=="True" else "non disponible")
    return msg,prix,nom

#Ce module permet de traiter la 4eme requete du role public
def req4(req,contenu,tab): 
    reqbase="GET /api/menu/items/" #requete de base avant changement
    prixtot=""  #prix totale de tout les items 
    x=str(datetime.datetime.now())  #Pour ajouter la date instantanée
    req1=req[req.find("/commandes")+11::]
    c=(req[req.find("/commandes")+11::]).replace(" ",",")   #Cette instruction sert à changer chaque espace par un virgule
    for i in range(req1.count("x")):    #suivant le nombre d'items  #cette boucle permet de derterminer le prix totale de la commande 
        a=req1[0:req1.find("x")]
        reqbase=reqbase+a                   #Pour faire appel a la requete 3
        msg,prix,nom=req3(reqbase,contenu)  #appel a la requete 3 pour connaitre les les informations de chaque item 
        req1=req1[req1.find(" ")+1::]
        reqbase=reqbase[0:reqbase.find(a)]  
        prixtot=prixtot+prix+"/"
    prixtot=prixtot[0:len(prixtot)-1]
    with open("commandes.csv", 'r') as f: #pour connairtre le numéro de la nouvelle commande
        a=0
        for ligne in f:
            a+=1            #numéro de la commande
    with open("commandes.csv", 'a') as f:
        content=("\n"+str(a)+"  | "+tab[0]+" | "+c+" | "+(x[0:x.find(" ")]))+" | "+prixtot #somme ou bien chqaue item avec son propre prix
        f.write(content)    #l'ecriture finale dans le fichier 

#Ce module permet de traiter la 1ere requete du role staff
def req1_staff():
    tab=[]
    with open("commandes.csv", 'r') as f: 
        for ligne in f:
            x=ligne.split(" | ")
            ind=x[4].find("/")
            if ind !=-1:
                x[4]=str((float(x[4][0:ind]))+(float(x[4][ind+1::])))
            if (((x[4])[0:len((x[4]))-1])+"\n"!=(x[4])):    #condition pour afficher le nombre juste comme prix
                tab.append((x[0],x[3],(x[4])+"$"))      
            else :
                tab.append((x[0],x[3],(x[4])[0:len((x[4]))-1]+"$"))
    return tab
#Ce module permet de traiter la 2eme requete du role staff
def req2_staff(req,contenu):#req="GET /api/commandes/2"
    id=req[req.find("commandes/")+10::]
    with open("commandes.csv", 'r') as f:
        n=0
        for ligne in f:
            n+=1
            x=ligne.split(" | ")
            if n==int(id):
                commandef=(x[2])
                commande=(x[2])
        tab=req1_staff()
        tab1=tab[int(id)-1]
    for i in range(commande.count("x")):
        ind=commande[0:commande.find("x")]
        commande=commande[(commande.find(",")+1)::]
        msg,prix,nom=req3(("GET /api/menu/items/"+ind),contenu) #pour ajouter les données nécessaires dans le tuple selon la mise en forme nécessaire
        commandef=commandef.replace(ind,nom)
        commandef=commandef.replace("x","*")    
    tab1=tab1+(commandef,)
    return tab1
#Ce module permet d'appliquer tout les conditions sur les requetes 
def conditions(req):
    listcat=["boisson","boisson_chaude","cafe","the","chocolat","boisson_froide","sandwich","regulier","wrap","fruit","viennoiserie","pain","chausson","croissant","muffin"]
    with open("commandes.csv", 'r') as f:
        n=0
        for ligne in f:
            n+=1    #pour connaitre le nombre de commandes
    cond1=(req=="GET /api/menu/items")
    cond2=((req[req.find("/menu/")+6:req.find("/items")]) in listcat)#######
    cond3=((req[req.find("/items/")+7::]).isdigit()==True and ((req[0:req.find("/items/")+7])=="GET /api/menu/items/") and (1<=int(req[req.find("/items/")+7::])<=40))
    cond4=((req.find("POST /api/commandes")!=-1))#######
    cond5=(req=="GET /api/commandes")
    cond6=(((req[0:req.find("/commandes/")+11])=="GET /api/commandes/") and (1<=int(req[req.find("/commandes/")+11::])<=n))
    cond7=((req[req.find("/items/")+7:req.find("disponible")-1]).isdigit()==True) and ((1<=int(req[req.find("/items/")+7:req.find("disponible")-1])<=40) and (req.find("PUT /api/menu/items/")!=-1) and ((req[req.find("/items/")+9::]=="disponible=0") or (req[req.find("/items/")+9::]=="disponible=1")))
    return cond1,cond2,cond3,cond4,cond5,cond6,cond7

#Ceci est le module principale 
def main():
    tab=initialisation()
    with open("menu.json", "r", encoding='utf8') as f:
        contenu = (json.load(f))
    req=input("Entrez votre requête : ")
    cond1,cond2,cond3,cond4,cond5,cond6,cond7=conditions(req)
    if tab[5]=="public":    #requetes du role public
        while (cond1==False and cond2==False and cond3==False and cond4==False ):
            req=input("Entrez une requête valide : ") 
            cond1,cond2,cond3,cond4,cond5,cond6,cond7=conditions(req)
    elif tab[5]=="staff":   #requete du role staff
        while (cond5==False and cond6==False and cond7==False):
            req=input("Entrez une requête valide : ") 
            cond1,cond2,cond3,cond4,cond5,cond6,cond7=conditions(req)

#éxecution de la requete qui convient selon les conditions 
    if cond1 or cond2:
        msg=req1_2(req,contenu,tab)  
        print(msg)
    elif cond3:
        msg,prix,nom=req3(req,contenu) 
        print(msg)
    elif cond4:
        req4(req,contenu,tab)
    elif cond5:
        tab1=req1_staff()
        affiche(tab1)
    elif cond6:
        tab1=req2_staff(req,contenu) 
        print(tab1)
    elif cond7:
        msg,prix,nom=req3(req,contenu)
#Ce module permet de verifier si une chaine peut etre un nombre float ou non
def isfloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False

#Ce module contient tout les tests unitaires
def test():
    #5 Tests Unitaires pour la fonction initialisation()
    tab=initialisation()
    assert (tab[5]!=0 and tab[5]!=1) , " Le compte doit etre actif ou non actif "
    assert (tab[4]!="public" and tab[4]!="staff") , " Le role doit etre public ou bien staff "
    assert type(tab)!="list" , "La fonction doit donner un tableau comme sortie"
    assert tab[3].find("@umontreal.ca")==-1 or tab[3].find("@umontreal.ca")==0 , "L'adresse email doit etre valide"
    assert (tab[3].find(tab[2]+"."+tab[1]))==-1 , "l'adresse email et le nom et le prénom ne ressemble pas "
    #################################################################################################################
    with open("menu.json", "r", encoding='utf8') as f:
        contenu = (json.load(f))
    msg,prix,nom=req3("GET /api/menu/items/1",contenu)
    tab2=msg.split(" | ")
    #-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
    #5 Tests unitaires pour la fonction req3(req,contenu)
    assert (prix.find("$")==-1 or isfloat(prix[0:prix.find("$")])==False),"Le prix n'est pas juste"
    assert nom.isalpha()==False,"La format du nom n'est pas valide"
    assert id !=1,"id non disponible"
    assert tab2[len(tab2)-1]=="disponible" ,"La disponibilité de l'article n'est pas juste "
    assert len(tab2)==4,"Nombre d'éléments affichés n'est pas juste"
    #################################################################################################################
    #5 Tests unitaires pour la fonction conditions(req)
    cond1,cond2,cond3,cond4,cond5,cond6,cond7=conditions("GET /api/menu/cafe/items")
    assert cond2==True ,"Le contole de la requete 'GET /api/menu/{categorie}/items:' n'est pas valide"
    cond1,cond2,cond3,cond4,cond5,cond6,cond7=conditions("GET /api/menu/items")
    assert cond1==True,"Le controle de la requete 'GET /api/menu/items' n'est pas valide"
    cond1,cond2,cond3,cond4,cond5,cond6,cond7=conditions("GET /api/menu/items/1")
    assert cond3==True,"Le controle de la requete 'GET /api/menu/items/{identifiant}' n'est pas valide"
    cond1,cond2,cond3,cond4,cond5,cond6,cond7=conditions("POST /api/commandes 3x1 4x2")
    assert cond4==True,"Le controle de la requete 'POST /api/commandes [items]' n'est pas valide"
    cond1,cond2,cond3,cond4,cond5,cond6,cond7=conditions("GET /api/commandes")
    assert cond5==True,"Le controle de la requete 'GET /api/commandes' n'est pas valide"

#test()

main()


    















             











