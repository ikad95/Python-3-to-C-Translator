import re

def idType(value):
        z=re.split("\* | + | - | / | % | \*\*",value)[0]
        if z in ids:
                return ids[z]
        try:
                float(z)
                try:
                        int(z)
                        return 'long long'
                except ValueError:
                        pass
                return 'double'
        except ValueError:
                return 'string'
def vmapX(x):
        #if(x==''):
         #       return 0
        pl=re.split('\(|\)',x)
        pl=[z for z in pl if z][0]
        #print x
        if str(x).isdigit() or x[0]=="\"" or x[0]=="\'" :
                return str(x)
        try:
                return vmap[x]
        except:
                return 0
def parseExp(exp):
        p=''
        n=re.split('[(|)|+|\-|\*\*|/|%|\*]',exp)
        n="".join(n)
        op = re.split('[a-zA-Z0-9]|==|<=|<|!=|>|>=|\"',n)
        op=[x for x in op if x]
        exp = re.split(" && | \|\| | ^ ",exp)
        iii=0
        for x in exp:
                tokens=re.split('(==|<=|<|!=|>|>=)',x)
                if(len(tokens)==1):
                        p+=parseArith(tokens[0])
                else:
                        p+= parseArith(tokens[0])+tokens[1]+parseArith(tokens[2])
                if(iii<len(exp)-1):
                        p+=op[iii]
                        iii+=1
        return p
def parseArith(exp):
        if(str(exp).isdigit()):
                return str(exp)
        p=''
        exp="".join(exp.split())
        n=re.split('[(|)|+|\-|\*\*|/|%|\*]',exp)
        op=re.split('[a-zA-Z0-9.]|"',exp)
        op=[x for x in op if x]
        iii=0
        try:
                if(op[0]!='' and '(' in op[0]):
                    p+=op[0]
                    op=op[1:]
        except:
                pass
        n = [z for z in n if z]
        for x in n:
                if(str(vmapX(x)).isdigit()):
                        p+=x
                else:
                        p+=str(vmapX(x))
                if(iii<len(n)-1):
                        p+=op[iii]
                        iii+=1
        while iii!=len(op):
                p+=op[iii]
                iii+=1
        return p
inp=open('toTranslate.py','r')
out=open('Translated.cpp','w')
out.write("#include <iostream>\n#include <vector>\n#include <algorithm>\n#define True 1\n#define False 0\n\nusing namespace std;\n\n")

loop=0
ids={}
vmap={}
tab=''
res=''
linecount=0
addNl=0

for i in inp:
        if(i[:-1]=="#\\n"):
                addNl=1
                continue
        res+='\t'
        tabCount = i.count("\t")
        quotesCount=0
        spl= i.split("\"")
        for x in range(0,len(spl),2):
                spl[x]=spl[x].replace(" and "," && ")
                spl[x]=spl[x].replace(" or "," || ")
                #print(spl)
        temp=''
        for x in range(len(spl)):
                temp+=spl[x]+"\""
        i = temp[:-1]
                
        #indentation management start
        if loop>=1:
                if tabCount < loop: #if nesting ##dont trust
                        while tabCount < loop:
                                res+=("\n\t"+tab[1:]+"}\n\t"+tab[1:-1])
                                tab=tab[1:]
                                loop-=1
        i="".join(i.strip())
        i+='\n'
        #indentation management end
        
        #special ops

        zzz=i.split('.')
        try:
                if zzz[1][:-1]=="append(input())":
                        ids['temp']='long long'
                        res+=tab+"scanf(\"%lld\",&temp);\n\t"+tab+zzz[0]+'.push_back(temp);\n'
                elif zzz[1][:len("append(")]=="append(":
                        res+=tab+vmapX(zzz[0])+'.push_back('+parseArith(zzz[1][len("append("):-2])+');\n'
                elif zzz[1][:len('sort(reverse=True)')]=="sort(reverse=True)":
                        res+=tab+"sort("+vmapX(zzz[0])+".end(),"+vmapX(zzz[0])+".begin());\n"
                elif zzz[1][:len('sort(')]=="sort(":
                        res+=tab+"sort("+vmapX(zzz[0])+".begin(),"+vmapX(zzz[0])+".end());\n"
                continue
                          
        except: pass
        #special ops end
		
        #def start
        if i[:len('def')]=="def":
            def_start = 1
            print("def found")
        #def end

        #print start
        tt=''
        if i[:len('print')]=="print":
                if(i[len("print")]==" "):
                        ws=0
                        while(i[5+ws]==" "):
                                ws+=1
                        i=i.replace(" ","",ws)
                if i[5:6]=="(":  #print()
                        if i[6:7]!="\'" and i[6:7]!="\"": #print(x)
                                pr=i[6:-2]
                                if re.split(r'[*+-/%]',i[len("print("):-2])[0] in ids:
                                        pr=re.split(r'[*+-/%]',i[len("print("):-2])[0]
                                try:
                                        pr=pr.split('[')
                                        pr=pr[0]
                                        if ids[vmap[pr]]=='long long':
                                                tt='%lld'
                                        elif ids[vmap[pr]]=='long long[]':
                                                tt='%lld'
                                        elif ids[vmap[pr]]=='double':
                                                tt='%lf'
                                        elif ids[vmap[pr]]=='string':
                                                tt="%s"
                                except:
                                        pass
                                if(tt!="%s"):
                                        if vmapX(i[6:-2]):
                                                #long longs and doubles
                                                res+=(tab+"printf("+"\"" +tt+ "\","+vmapX(i[6:-2])+")" +';'+"\n")
                                        else:
                                                #arrays
                                                arr=(i[6:-2]).split('[')
                                                if(len(arr)==1):
                                                        res+=tab+"printf(\"%lld\","+parseArith(i[6:-2])+");\n"
                                                        if(addNl==1):
                                                                res+="\t"+tab+"printf(\"\\n\");\n"
                                                        continue
                                                res+=tab+"cout<<"+vmapX(arr[0])+"["+vmapX(arr[1].split(']')[0])+"];\n"
                                else:
                                        #strings
                                        res+=tab+"cout<<"+parseArith(i[6:-2])+";\n"
                        else: #print('')
                                res+=(tab+"printf("+"\"" +i[7:-3]+ "\")" +';'+"\n")
                if(addNl==1):
                        res+="\t"+tab+"printf(\"\\n\");\n"     
                continue
        #print end

        #id creator, assignment and comparison start
        sp=i[:-1].replace(" ","")
        f=i
        i=i.replace(" ","")
        for x in range(len(sp)):
                if sp[x]=='=':
                        if sp[x+1]=='=' or sp[x-1]=='!' or sp[x-1]=='<' or sp[x-1]=='>':
                                #res+=tab+sp+";\n"
                                break
                        # handle x+=y type of events
                        y= re.split(r'[*+-/%]',i[:x])
                        if len(y)>1:
                                res+=tab+vmap[y[0]]+i[x-1]+"="+parseArith(i[x+1:-1])+";\n"
                                break
                        # handle x+=y type of events end
                        y=y[0]
                        if i[x+1:-1]=='[]':
                                ids[i[:x]+"_vec"]='long long[]'        ##Check if already exists if so modify
                                vmap[i[:x]]=i[:x]+"_vec"
                                res+="\n"
                        elif i[x+1:x+7]=='str(input(':
                                ids[i[:x]+"_str"]='string'
                                vmap[i[:x]]=i[:x]+"_str"
                                res+=tab+"getline(cin,"+ vmap[i[:x]]+");\n"
                        elif i[x+1:len("input(")+x+1]=='input(':
                                ids[i[:x]+"_lon"]='long long'
                                vmap[i[:x]]=i[:x]+"_lon"
                                res+=tab+"scanf(\"%lld\",&"+ vmap[i[:x]]+");\n"
                        elif i[x+1:x+13]=='float(input(':
                                ids[i[:x]+"_dou"]='double'
                                vmap[i[:x]]=i[:x]+"_dou"
                                res+=tab+"scanf(\"%lf\",&"+ vmap[i[:x]]+");\n"
                        elif i[x-1]=="]":
                                m=i.split('[')
                                n=m[1].split(']')
                                res+=tab+vmapX(m[0])+"["+parseArith(n[0])+"]"+n[1][:-1]+";\n"
                        else:
                                if i[x+1]=='\'' or i[x+1]=='\"':
                                        if i[x-1]!='+':
                                                ids[i[:x]+"_"+str(idType(i[x+1:]))[:3]]=str(idType(i[x+1:]))
                                                vmap[i[:x]]=i[:x]+"_"+str(idType(i[x+1:]))[:3]
                                                res+=tab+vmap[i[:x]]+"=\""+i[x+2:-2]+"\";\n"
                                        elif i[x-1]=='+':
                                                res+=tab+vmap[i[:x]]+"=\""+i[x+2:-2]+"\";\n"
                                elif i[x+1].isdigit()==True:
                                        ids[y[:x]+"_"+str(idType(i[x+1:]))[:3]]=str(idType(i[x+1:]))
                                        vmap[i[:x]]=i[:x]+"_"+str(idType(i[x+1:]))[:3]
                                        res+=tab+vmap[i[:x]]+"="+i[x+1:-1]+";\n"
                                else :
                                        plL=re.split('\(|\)',i[x+1:-1])
                                        plL=[z for z in plL if z][0]
                                        plL = re.split(r'[*+-/%]',plL)
                                        for pl in plL:
                                                if vmapX(pl) in ids:
                                                        if ids[vmap[pl]]=='double' or ids[vmap[pl]]=='long long' or ids[vmap[pl]]=='string':
                                                                vmap[i[:x]]=i[:x]+"_"+ids[vmap[pl]][:3]
                                                                ids[vmap[i[:x]]]=ids[vmap[pl]]
                                                                #print parseArith(i[x+1:-1])
                                                                res+=tab+(vmap[i[:x]])+"="+parseArith(i[x+1:-1])+";\n"                   #############
                                                                break
                                                        else:
                                                                pass
                                        else:
                                                try:
                                                        ids[vmap[i[:x]]] = idType(vmap[i[x+1:-1]])
                                                except:
                                                        pass
                                                res+=tab+i[:-1]+";\n"
                                                
        #id creator, assignment and comparison end

        #for loop start
        i=f
        if i[:len('for')]=="for":
                f=i.split(" ")
                if vmapX(f[3][6:-3]) in ids:
                        vmap[f[1]]=f[1]+"_lon"
                        ids[vmap[f[1]]]=ids[vmap[f[3][6:-3]]]
                else:
                        vmap[f[1]]=f[1]+"_lon"
                        ids[vmap[f[1]]]="long long"#str(idType(f[3][6:-3]))
                res+=(tab+"for("+vmap[f[1]]+"=0;"+vmap[f[1]]+"<"+parseArith(f[3][6:-3])+";"+vmap[f[1]]+"++)"+"\n"+tab+"\t{\n")
                loop+=1
                tab+='\t'
        #for loop end

        #while loop start
        if i[:len('while')]=="while":
                res+=tab+"while("+parseExp((i[len('while('):-3]))+")\n\t"+tab+"{\n"
                loop+=1
                tab+='\t'
                continue
        #while loop end

        #if else statement start
        if i[:len('if')] == "if":
                i=i.replace("("," ",1)
                i=i[::-1]
                i=i.replace(")","",1)
                i=i[::-1]
                #print i[len('if('):-2]
                #print parseExp(i[len('if('):-2])
                res+=tab+"if("+parseExp(i[len('if('):-2])+")\n\t"+tab+"{\n"
                loop+=1
                tab+='\t'
                i=i[len('if')+1:-2] #experimental
        if i[:len('elif')]=="elif":
                i=i.replace("("," ",1)
                i=i[::-1]
                i=i.replace(")","",1)
                i=i[::-1]
                res+=tab+'else if('+parseExp(i[len('elif')+1:-2])+')\n\t'+tab+"{\n"
                loop+=1
                tab+='\t'
        if i[:len('else')] == "else":
                i=i.replace("("," ",1)
                i=i[::-1]
                i=i.replace(")","",1)
                i=i[::-1]
                res+=tab+"else"+parseExp(i[len('else')+1:-2])+"\n\t"+tab+"{\n"
                loop+=1
                tab+='\t'
        #if else statement end

        


        #break & continue
        if i[:-1]=="break" or i[:-1]=="continue":
                res+=tab+i[:-1]+";\n"
        #break & continue end

        
        
while loop!=0:
        res+=("\n\t"+tab[1:]+"}\n")
        tab=tab[1:]
        loop-=1
res+=("\treturn 0;\n}\n")

out.write("int main()\n{\n")
for key,value in ids.items():
        if value=='long long[]':
                out.write("\tvector<long long> "+key+';\n')
        elif value!='char':
                out.write("\t"+value+" "+key+";\n")
        else:
                out.write("\t"+value+" "+key+"[BUFF];\n")
out.write('\n\n')
out.write(res)
out.close()
