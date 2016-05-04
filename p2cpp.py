import re

def idType(value):
        z=re.split("\* | + | - | / | %",value)[0]
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


inp=open('toTranslate.py','r')
out=open('Translated.cpp','w')
out.write("#include <iostream>\n#include <vector>\n\nusing namespace std;\n\n")

loop=0
ids={}
tab=''
res=''
linecount=0
god=1
for i in inp:
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
                if i[:len(tab)]==tab: #if no nesting
                        i="".join(i.strip())
                        i+='\n'
                        
                elif tabCount < loop: #if nesting ##dont trust
                        while tabCount < loop:
                                res+=("\n"+tab[1:]+"}\n")
                                tab=tab[1:]
                                loop-=1
        i="".join(i.strip())
        i+='\n'
        #indentation management end
#print start
        tt=''
        

        if i[:len('print')]=="print":
                if(i[len("print")]==" "):
                        i=i.replace(" ","",1)
                if i[5:6]=="(":  #print()
                        if i[6:7]!="\'" and i[6:7]!="\"": #print(x)
                                pr=i[6:-2]
                                if re.split(r'[*+-/%]',i[len("print("):-2])[0] in ids:
                                        pr=re.split(r'[*+-/%]',i[len("print("):-2])[0]
                                try:
                                        pr=pr.split('[')
                                        pr=pr[0]
                                        if ids[pr]=='long long':
                                                tt='%lld'
                                        elif ids[pr]=='long long[]':
                                                tt='%lld'
                                        elif ids[pr]=='double':
                                                tt='%f'
                                        elif ids[pr]=='string':
                                                tt="%s"
                                except:
                                        pass
                                if(tt!="%s"):
                                        res+=(tab+"printf("+"\"" +tt+ "\","+i[6:-2]+")" +';'+"\n") #i[6:-2] original
                                else:
                                        res+=tab+"cout<<"+i[6:-2]+";\n"
                        else: #print('')
                                res+=(tab+"printf("+"\"" +i[7:-3]+ "\")" +';'+"\n")
                continue
        #print end

        #id creator and assignment and comparison start
        sp=i[:-1].replace(" ","")
        f=i
        i=i.replace(" ","")     
        for x in range(len(sp)):
                if sp[x]=='=':
                                #ids(sp[:x])=idType((sp[x+1:-1]))
                                
                        if sp[x+1]=='=' or sp[x-1]=='!' or sp[x-1]=='<' or sp[x-1]=='>':
                                #res+=tab+sp+";\n"
                                break
                        y=sp[:x].replace("*","")
                        y=sp[:x].replace("%","")
                        y=sp[:x].replace("/","")
                        y=sp[:x].replace("-","")
                        y=sp[:x].replace("+","")
                        
                        #if(len(i[x+1:-1].split("*"))==2):
                        #       ids(i[:x])=idType(i[x+1:-1].split("*")[0])
                        if i[x+1:-1]=='[]':
                                ids[i[:x]]='long long[]'
                                ##########
                        elif i[x+1:x+7]=='str(input(':
                                ids[i[:x]]='string'
                                res+=tab+"getline(cin,"+ i[:x]+");\n"
                        elif i[x+1:len("input(")+x+1]=='input(':
                                ids[i[:x]]='long long'
                                res+=tab+"scanf(\"%lld\",&"+ i[:x]+");\n"
                        elif i[x+1:x+13]=='float(input(':
                                ids[i[:x]]='double'
                                res+=tab+"scanf(\"%f\",&"+ i[:x]+");\n"
                        else:
                                if i[x+1]=='\'' or i[x+1]=='\"':
                                        if i[x-1]!='+':
                                                ids[i[:x]]=str(idType(i[x+1:]))
                                                res+=tab+i[:x]+"=\""+i[x+2:-2]+"\";\n"  #'strcpy('+i[:x]+','+"\""+i[x+2:-2]+"\""+');\n'
                                        elif i[x-1]=='+':
                                                res+=tab+i[:x]+"=\""+i[x+2:-2]+"\";\n"
                                elif i[x+1].isdigit()==True:
                                        ids[y[:x]]=str(idType(i[x+1:]))
                                        res+=tab+sp+";\n"
                                else :
                                        pl = re.split(r'[*+-/%]',i[x+1:-1])[0]
                                        if pl in ids:
                                                if ids[pl]=='double' or ids[pl]=='long long' or ids[pl]=='string':
                                                        ids[i[:x]]=ids[pl]
                                                        res+=tab+i[:-1]+";\n"
                                                else:
                                                        pass
                                        else:
                                                try:
                                                        ids[i[:x]] = idType(i[x+1:-1])
                                                except:
                                                        pass
                                                res+=tab+i[:-1]+";\n"
                                                






        #id creator and assignment and comparison end

        #for loop start
        i=f
        if i[:len('for')]=="for":
                f=i.split(" ")
                if f[3][6:-3] in ids:
                        ids[f[1]]=ids[f[3][6:-3]]
                else:
                        ids[f[1]]=str(idType(f[3][6:-3]))
                res+=(tab+"for("+f[1]+"=0;"+f[1]+"<"+f[3][6:-3]+";"+f[1]+"++)"+"\n"+tab+"{\n")
                loop+=1
                tab+='\t'
        #for loop end

        #while loop start
        if i[:len('while')]=="while":
                res+=tab+"while("+i[len('while')+1:-3]+")\n"+tab+"{\n"
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
                res+=tab+"if("+i[len('if')+1:-2]+")\n"+tab+"{\n"
                loop+=1
                tab+='\t'
                i=i[len('if')+1:-2] #experimental
        if i[:len('elif')]=="elif":
                i=i.replace("("," ",1)
                i=i[::-1]
                i=i.replace(")","",1)
                i=i[::-1]
                res+=tab+'else if('+i[len('elif')+1:-2]+')\n'+tab+"{\n"
                loop+=1
                tab+='\t'
        if i[:len('else')] == "else":
                i=i.replace("("," ",1)
                i=i[::-1]
                i=i.replace(")","",1)
                i=i[::-1]
                res+=tab+"else"+i[len('else')+1:-2]+"\n"+tab+"{\n"
                loop+=1
                tab+='\t'
        #if else statement end

        


        #break & continue
        if i[:-1]=="break" or i[:-1]=="continue":
                res+=tab+i[:-1]+";\n"+tab
        #break & continue end

    #special ops

        #out.write("$$",zzz,"$$")
        zzz=i.split('.')
        try:
                if zzz[1][:-1]=="append(int(input()))":
                        ids['temp']='long long'
                        res+=tab+"scanf(\"%lld\",&temp);\n"+tab+zzz[0]+'.push_back(temp);\n'
                elif zzz[1][:len("append(")]=="append(":
                        res+=tab+zzz[0]+'.push_back('+zzz[1][len("append("):-1]+';\n'
        
        except: pass                
while i[0:len(tab)]!=tab:
        res+=("\n"+tab[1:]+"}\n")
        tab=tab[1:]
        loop-=1
res+=("return 0;\n}\n")

out.write("int main()\n{\n")
for key,value in ids.items():
        if value=='long long[]':
                out.write("vector<long long> "+key+';\n')
        elif value!='char':
                out.write(value+" "+key+";\n")
        else:
                out.write(value+" "+key+"[BUFF];\n")
out.write('\n')
out.write(res)
out.close()
