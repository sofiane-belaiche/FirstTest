#!/usr/bin/python3
# -*- coding:utf-8 -*-
import os, json
import nltk
from flask import Flask,render_template, request # importation des class de flask

from nltk.tag import StanfordPOSTagger

app = Flask(__name__) 
os.system("clear")  

root_path="/home/e20160010106/projet teR NOUVEAU/StanfordTagguer/"
pos_tagger = StanfordPOSTagger(root_path + "/models/french.tagger", root_path + "/stanford-postagger.jar",encoding='utf8') #instance de la classe StanfordPOSTagger en UTF-8


def pos_tag(sentence):
    tokens = nltk.word_tokenize(sentence) #je transforme la phrase en tokens => si vous avez un texte avec plusieurs phrases, passez d'abord par nltk pour récupérer les phrases
    tags = pos_tagger.tag(tokens) #lance le tagging
    print(tags)
    return tags
 
@app.route('/')  # route qui a pour chemin /
def recherche_1(): 
   print('/recherche_1')
   return render_template('recherche_1.html') # renvoie la page HTML recherche_1.html


@app.route('/recherche/', methods=['POST','GET'])
def recherche():
   if request.method           == 'POST':
        criter = request.form['critere']
          
        premier = [] 
        second = [] 
        liste = [] 
        dicADJ = {}
        adjectif = {}  
        adverbe = {}
        troisieme = [] 
        forth = []  
        lesnoms = []
        lanegation = ["ne","n'"," non "," pas "] # pour la négation
        s = open("Data/coordination.txt" , "r") # un fichier de conjonctions de coordination
        separateurs = list(s)

        for elementt in separateurs:
            if elementt in criter:
                
                morceaux = criter.split(elementt)
            elif " et " in criter:
                morceaux = criter.split(" et ")  # ici ls phrases sont séparées par "et"
            else:
               
                morceaux = criter.split(",") # sinon  par une vrigule
        
        criteres = criter.split()
        
        crt = list(criteres)
        third = [] 
        dicADV = {} 
        lesAdjectifs= [] 
        lesAdverbs = []
        tagList = []
        noms = []
        listenoms = {}  
        firstRound = []
        secondRound = []
        thirdRound = []
        listeadverbs = []
        listeadjectifs = [] 
        fiveth = []     
        with open('Data/data.json') as json_data:  # ouverture de fichier des polarites pour les adjectifs
            data_dict = json.load(json_data)

        with open('Data/lexique.json') as data:  # ouverture de fichier lexique intensifieure pour les adverbes
            dictt = json.load(data)     

        with open('Data/verbes_etat.json') as verbes_etat:  # fichier des verbes d'etat
            verbes = json.load(verbes_etat)
        
        index = 0
        for index, morceau in enumerate(morceaux): # morceau et son index
            
            for v in lesAdjectifs:
                lesAdjectifs.remove(v) # suppression du contenu de la liste pour le 2émé morceau(phrase)
            for y in lesAdverbs:
                lesAdverbs.remove(y)  # //  //   //
            for vac in lesnoms:
                lesnoms.remove((vac)) # // //   //
                
            tagss=pos_tag(morceau) # fonction de l'etiquettage
           
            print("\nmorceau:", morceau, "tagss:", tagss)
            tagList.append(tagss) 
            
            for tag in tagss:
                
                if tag[1] == "A":
                    lesAdjectifs.append(tag[0])  # liste des adjectifs
                    listeadjectifs.append(tag[0])
                elif tag[1] == "ADV" and tag[0] != "pas" and tag[0] != "ne" and tag[0] != "non" :   
                    lesAdverbs.append(tag[0]) # liste des adverbes
                    listeadverbs.append(tag[0])
                   
                elif tag[1] == "N" :
                    lesnoms.append((index, tag[0]))
                    noms.append(tag[0] )  # liste des noms
                    
                
            for varr, nombre in data_dict.items():                    
                for val in lesAdjectifs:
                    if varr == val:
                        dicADJ.update({index:{varr:nombre}})  # dictionnaire de l'adjectif et sa valeur avec l'index
                        print("dicADJ===",dicADJ)
                                      
            for key, valeur in dictt.items():
                for value in lesAdverbs:
                    if key == value:
                        dicADV.update({index:{key:valeur}}) # dictionnaire de l'adverbe et sa valeur et son index
             
            for r , a in dicADJ.items():
                for tt , uu in a.items():
                    adjectif[r] = uu   #  un dictionnaire de l'index et la valeur de l'adjectif
                    print("adjectif est= ",adjectif)
            for tt, oo in dicADV.items():
                for aa, ww in oo.items():
                    adverbe[tt] = ww   # un dictionnare de l'index et la valeur de l'adverbe

                    
            total = 1
            totaladv = 1
            totalg = 0
            for ce, bb in adjectif.items(): 
                vv = int(bb)
                total = vv
                # print("le total est des adj :", vv)
            for yy, jj in adverbe.items():
                ff = int(jj)
                totaladv = ff
                # print("le total de adv est::",ff)
            for tt,bb in dicADV.items():
                
                for rr,bel in dicADJ.items():
                    if tt == rr: #si l'index == index on fait la multiplication des polarites
                        for ty in verbes.values(): #  les verbes d'etat
                            for bn in ty:
                                if bn in morceau:
                                    for sh in lanegation:
                                        if sh in morceau:
                        
                                            totalg = total * totaladv * -1 #  la négation et multiplication de la valeur de l'adjectif et adverbe
                                        elif " ne " in morceau:
                                            totalg = total * totaladv * -1
                                        else:
                                            totalg = total * totaladv
                    for sof in lesnoms:
           
                        for t, b in dicADJ.items():
                            # for rrr, ppp in dicADV.items():
                            if sof[0] == t: #si l'index de l'djectif == index de nom(pour la propagation) 
                                listenoms[sof[1]] = totalg  # on ajoute le nom et le total pour affichage
                                print(listenoms) 
                                # listenoms = list(set(listenoms)) supprime les doublons dans une liste
                                   
            for keys, values in dicADJ.items():
                for rt,nh in values.items():
                    if not lesAdverbs:
                        for rr in verbes.values(): # les verbes d'etat
                            for ht in rr:
                                if ht in morceau:
                                
                                    for nb in lanegation:
                                        if nb in morceau:
                                        
                                            totalg = total * -1   # la négation
                                        elif " ne " in morceau:
                                            totalg = total * -1
                                        else:
                                        
                                            totalg = total * 1
                                        
                                
                        for ta in lesnoms:
                            if ta[0] == keys: #  si l'index de nom == index de l'adjectif
                                listenoms[ta[1]]  = totalg
                                print(listenoms)
                                # resultats = list(listenoms) 
            for key, value in dicADV.items():
                for rtt,nhh in value.items():
                    if not lesAdjectifs:
                        for tt in verbes.values():
                            for te in tt:                       # tout ca c la partie des adverbes fonctionne comme la partie des adjectifs
                                if te in morceau:
                                    for tr in lanegation:
                                        if tr in morceau:
                                            totalg = totaladv * -1 
                                        elif " ne " in morceau:
                                            totalg = totaladv * -1   
                                        else:
                                            totalg = totaladv * 1
                        for tap in lesnoms:
                            if tap[0] == key:
                                listenoms[tap[1]]= totalg  
                                
            if index == 1:
                secondRound.append(totalg)
                
            
            if not lesAdjectifs:
                if not lesAdverbs:
                    for element in lesnoms:
                        if index == 0:
                            firstRound.append(element[1] )  # cette partie gére des phrases comme le jardin et la chambre sont propre
                           
            for tr in firstRound:
                for hg in secondRound:
                    # thirdRound.append((tr,hg))
                    # print("thirdRound ==",thirdRound)                
                    listenoms[tr] = hg 
            res = 0
            for key , value in adjectif.items():
                if key == 1:
                    bn = int(value)
                    premier.append(bn)
                elif key == 2:
                    gf = int(value)
                    troisieme.append(gf)
                elif key == 0:
                    hg = int(value)
                    second.append(hg)
                ht = 0
                for element in premier:   # cettepartie gére des phrases: comme  la chambre est belle , jolie , propre
                    gf = int(element)
                    for variable in second:
                        bc = int(variable)
                        if not lesnoms:
                            res = gf + bc
                            third.append(res)
                        for ek in noms:
                            for tr in third:
                                listenoms[ek] = tr 
                        for tr in troisieme:
                            bf = int(tr)
                            if not lesnoms:
                                ht = res + bf  
                                for kl in noms:
                                    listenoms[kl] = ht
                                            
            resultats = 0
            for cle , valeur in adverbe.items():
                if cle == 1:
                    n = int(valeur)
                    premier.append(n)
                elif cle== 2:
                    f = int(valeur)
                    troisieme.append(f)
                elif cle == 0:
                    g = int(valeur)
                    second.append(g)             # cette partie gére des phrases comme : la chambre est bien ,  jolie , super
                t = 0
                for element in premier:
                    gff = int(element)
                    
                         
                    for variable in second:
                        bcc = int(variable)
                        if not lesnoms:
                            res = gff + bcc
                            third.append(res)
                        for ek in noms:
                            for tr in third:
                                listenoms[ek] = tr 
                        for tr in troisieme:
                            bbb = int(tr)
                            if not lesnoms:
                                t = res + bbb  
                                for kl in noms:
                                    listenoms[kl] = t

                        
            jk = 0 
            kll = 0  
            nb = 0 
            kp = 0
            mp = 0 
            n = 0                                 
            for k , v in adjectif.items():
                for c , l in adverbe.items():
                
                    if k == 1 and c == 1:
                        if not lesnoms:
                            g = int(v)
                            m = int(l)
                            jk = g * m
                            forth.append(jk)
                            print("forth====",forth)
                            
                    if k == 0:
                        g = int(v)
                        fiveth.append(g) 
                        print("g=======",g)
                    ress = 0
                    for element in forth:
                        for variable in fiveth:
                            ress = element + variable
                            print("ress=====",ress)
                            for nom in noms:
                                listenoms[nom] = ress # cette partie pour les phrases comme , la chambre est propre , trés belle
                    if c == 0:
                        t = int(l)
                        fiveth.append(t)
                    re = 0
                    for var in forth:
                        for elem in fiveth:
                            re = var + elem
                            for nom in noms:
                                listenoms[nom] = re                 
            
                    if k == 0 and c == 0:
                        
                            u = int(v)
                            o = int(l)
                            nb = u * o
                    if k == 1:
                        tr = int(v)
                        kp = tr + nb
                        for nomm in noms:
                            listenoms[nomm] = kp  # cette partie gére des phrases comme la chambre est trop propre , jolie
                    if c == 1:
                        cv = int(l) 
                        for nom in noms:
                            if not lesnoms:
                                mp = nb + cv
                                listenoms[nom] = mp
            
        with open('Data/dic.json') as ontologie:  #  ouverture de fichier ontologie
            ff = json.load(ontologie)
            mm = dict(ff)
        if isinstance(ff,dict):
            i = 0    
            for hi,gi in ff.items(): #hi est une clé , et gi est une valeur 
                if hi == 'hôtel':
                    for m in gi:
                        
                        if isinstance(m,dict):
                            for l,k in m.items():
                                for car, ko in listenoms.items():
                        
                                    if car  == l:
                                        
                                        k.append(ko)
                                        i += ko                             # tous ca c'est un code pour parcourrir la hiérarchie du fichier ontologie
                                        
                                    for element in k:
                                        if car == element:
                                            for var in m.values():
                                                if not var:
                                                    var.append(totalg)
                                                    i += ko
                                                
                                    else:    
                                        for x in k:
                                            if isinstance(x,dict):
                                                for n,a in x.items():
                                                   
                                                    for v, nr in listenoms.items():
                                                        if v == n:
                                                            if not a:
                                                                a.append(nr)
                                                                i += nr
                                                        for element in a:
                                                            if v == element:
                                                                for variablle in x.values():
                                                                    if not variablle:
                                                                        variablle.append(totalg)
                                                                        i += nr
                                                        else:
                                                            for v in a:
                                                                if isinstance(v,dict):
                                                                    for c,w in v.items():
                                                                        for tar,ju in listenoms.items():
                                                                            if tar  == c:
                                                                                if not w:
                                                                                    w.append(ju)
                                                                                    i += ju
                                                                            for element in w:
                                                                                if tar == element:
                                                                                    for variable in v.values():
                                                                                        if not variable:
                                                                                            variable.append(totalg)   
                                                                                            i += ju
                                                                            else:
                                                                   
                                                                                for t in w: 
                                                                                    if isinstance(t,dict):
                                                                                        for cc,nn in t.items():   
                                                                                            for mar,nk in listenoms.items():
                                                                                                
                                                                                                if mar == cc:
                                                                                                    if not nn:
                                                                                                        nn.append(nk)
                                                                                                        i += nk
                                                                                                for element in nn:
                                                                                                    if mar == element:
                                                                                                        for varia in t.values():
                                                                                                            if not (varia): 
                                                                                                                varia.append(totalg)
                                                                                                                i += nk
       
       
       
       
                    
       
       
        # dict2 = {}                                                                            
        # current = {'pad': 0}
        # with open('dic.json') as dictio:
        #     fr = json.load(dictio)


        # def _readList(myList):
        #     for myItem in myList:
                
        #         if isinstance(myItem, dict):
        #             _readDict(myItem)


        # def _readDict(currentDict):
        #     for k, v in currentDict.items():
        #         if isinstance(v, list):
        #             print("{}{}".format('   ' * current['pad'], k,v))
        #             current['pad'] += 1
        #             _readList(v)
        #             current['pad'] -= 1
        #         else:
        #             print("{}{}={}".format('   ' * current['pad'], k, v))


        # _readDict(fr)
        # print(json.dumps(dict2))
                                                                                           
                                                                                        
                                                                                
                                                                               
                                                                                       
                                    
            

        return render_template('recherche_1.html', tagList=tagList,dicADJ=dicADJ,dicADV=dicADV,i=i, listenoms=listenoms, mm=mm,crt=crt,noms=noms, listeadjectifs=listeadjectifs,listeadverbs=listeadverbs,lesnoms=lesnoms)
                  
# else:
        # return render_template('recherche_1.html')
      
                  
app.run(debug=True)












