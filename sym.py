
from sys import argv
import os
import fnmatch

#from symbol_table import*

def symlit(n):
	n=n.split(",")
	p=''
	for i in range(0,len(n)):
		if i!=len(n)-1:
			k=hex(int(n[i]))
			p=p+str(k)+','
		if i==len(n)-1:
			k=hex(int(n[i]))
			p=p+str(k)
	return p


def hex_convert(no):
	str1=hex(no)
	return(str1)



def lit(fr1,fw1):
	direc=['dd','db']
	lit=[]
	count=1
	cons=['mov','add','sub']
	reg=['al','bl','cl','dl','ah','bh','ch','dh','ax','bx','cx','dx','sp','bp','si','di','eax','ebx','ecx','edx','esi','edi','esp','ebp']
	lit_count=1
	fw1.write("Literal Table\n\n")
	fw1.write("\tLine_no\t\tLit_no\t\tHex_no\t\tLiteral_Symbol\t\tType\n\n")

	for line in fr1.readlines():
		s=line.split()
		for i in range(0,len(s)):
			if s[i] == 'dd':
				b=s[i+1]
				
			if s[i] in cons:
				n=s[i+1].split(',')
				kn=n[1].split('[')
				if kn[0] in reg:
					continue
				if kn[0] =='dword':
					continue
				else:
					
					if kn[0].isdigit():
						if kn[0] not in lit:
							lit.append(kn[0])
							fw1.write("\t"+str(count)+"\t\t"+'lit#'+str(lit_count)+"\t\t"+hex_convert(int(kn[0]))+"\t\t"+kn[0]+"\t\t\treg,img"+"\n")
							lit_count+=1 								
					else:
						if kn[0] in sym:
							if kn[0] not in lit:
								lit.append(kn[0])
								fw1.write("\t"+str(count)+"\t\t"+'lit#'+str(lit_count)+"\t\t"+symlit(sym[kn[0]])+"\t\t"+n[1]+"\t\t\treg,img"+"\n")
								lit_count+=1
			
		count+=1







def sym_tab(fw,fr,sym,size,cont,sym_no,line_count):
	
	fw.write('--Symbol Table--\n')
	fw.write('line_number		sym_no		symbol		def/undef	section		size		values   \n')
	for line in fr.readlines():
		sp=line.split()
		s="sym_"
		for i in range(0,len(sp)):
			if sp[i]=='dd':
				if sp[i-1] not in sym:
					sym[sp[i-1]]=sp[i+1]
					k=sp[i+1].split(',')
					size=len(k)*4
					fw.write('\t'+str(line_count)+'\t\t'+(s+str(sym_no))+'\t\t'+sp[i-1]+'\t\tD\t\tdata\t\t'+str(size)+'\t'+line+'\n')
					sym_no+=1

					break
			if sp[i]=='db':
				if sp[i-1] not in sym:
					sym[sp[i-1]]=sp[i+1]
					k=sp[i+1]
					k=k.split("'")
					kp=k[1]
					size=len(kp)*1
					fw.write('\t'+str(line_count)+'\t\t'+(s+str(sym_no))+'\t\t'+sp[i-1]+'\t\tD\t\tdata\t\t'+str(size)+'\t'+line+'\n')
					sym_no+=1

			if sp[i]=='resb':
				if sp[i-1] not in sym:
					sym[sp[i-1]]=1
					size=1
					fw.write('\t'+str(line_count)+'\t\t'+(s+str(sym_no))+'\t\t'+sp[i-1]+'\t\tD\t\tbss\t\t'+str(size)+'\t\t'+'-'+'\n\n')
					sym_no+=1

			if sp[i]=='resd':
				if sp[i-1] not in sym:
					sym[sp[i-1]]=1
					size=4
					fw.write('\t'+str(line_count)+'\t\t'+(s+str(sym_no))+'\t\t'+sp[i-1]+'\t\tD\t\tbss\t\t'+str(size)+'\t\t'+'-'+'\n\n')
					sym_no+=1
			
			if sp[i]=='main:':
				if sp[i-1] not in sym:
					sym[sp[i-1]]=1
					size='-'
					fw.write('\t'+str(line_count)+'\t\t'+(s+str(sym_no))+'\t\t'+'main'+'\t\tU\t\ttext\t\t'+size+'\t\t'+'-'+'\n\n')
					sym_no+=1

			if sp[i]=='printf':
				if sp[i-1] not in sym:
					sym[sp[i-1]]=1
					size='-'
					fw.write('\t'+str(line_count)+'\t\t'+(s+str(sym_no))+'\t\t'+sp[i-1]+'\t\tU\t\ttext\t\t'+size+'\t\t'+'-'+'\n\n')
					sym_no+=1

			if sp[i]=='scanf':
				if sp[i-1] not in sym:
					sym[sp[i-1]]=1
					size='-'
					fw.write('\t'+str(line_count)+'\t\t'+(s+str(sym_no))+'\t\t'+sp[i-1]+'\t\tU\t\ttext\t\t'+size+'\t\t'+'-'+'\n\n')
					sym_no+=1

			if sp[i]=='printf,scanf':
				s=sp[i].split(',')
	
				if s[0] not in sym:
					sym[sp[i-1]]=1
					size='-'
					fw.write('\t'+str(line_count)+'\t\t'+(s+str(sym_no))+'\t\t'+s[0]+'\t\tU\t\ttext\t\t'+size+'\t\t'+'-'+'\n\n')
					sym_no+=1

				if s[1] not in sym:
					sym[sp[i-1]]=1
					size='-'
					fw.write('\t'+str(line_count)+'\t\t'+(s+str(sym_no))+'\t\t'+s[1]+'\t\tU\t\ttext\t\t'+size+'\t\t'+'-'+'\n\n')
					sym_no+=1


		line_count+=1
	return sym

def inter_code(filenmae):
	with open(filename,"r") as file:
		s=[]
		if fnmatch.fnmatch(filename, '*.asm'):
			inter_file=os.path.splitext(filename)[0]
			li=[inter_file,'i']
			inter_file=".".join(li)
			f=1
			with open(inter_file,"w") as fd:
				for line in file:
					if "dd" in line:
						l1=line.split()
						for i in range(len(lit_name)):
							if l1[2] in lit_actualval[i]:	
								l1[2]=lit_name[i]
								l2=str(" ".join(l1))
								fd.write(l2)
								fd.write('\n')
								break
					elif "db" in line:
						l1=line.split('"')
						#print(l1)
						for i in range(len(lit_name)):
							if l1[1] in lit_actualval[i]:	
								l1[1]=lit_name[i]
								fd.write('"'.join(l1))
								break
					elif "main" in line:
						fd.write(line)
						after_main1(line,file,fd)
						break
				
					else:
						fd.write(line)

fr1=open('test1.asm','r')
fw1=open('lit_tab.lst','w')

lit(fr1,fw1)


fr=open('test1.asm','r')
fw=open('sym_table.lst','w')
size=1
cont=['main','printf']
sym_no=1
line_count=1
sym={}

sym_tab(fw,fr,sym,size,cont,sym_no,line_count)
filename="test1.asm"
#inter_code(filename)


