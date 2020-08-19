import pymysql
from jnpr.junos import Device
from jnpr.junos.utils.config import Config

#ket noi toi mysql
def get_mysql(table_name):
	connection=pymysql.connect('10.255.254.236','nguyennd','bh6k8mfmnpk5','SCTV')
	try:
		with connection.cursor() as cursor:
			# insert a user
			sql = "SELECT * from  "+ table_name
			cursor.execute(sql)
			data= cursor.fetchall()
			#print(data)
	finally:
		connection.close()
	return data
def del_mysql(name):
	connection=pymysql.connect('10.255.254.236','nguyennd','bh6k8mfmnpk5','SCTV')
	try:
		with connection.cursor() as cursor:
			# insert a user
			sql = "DELETE FROM  " + name
			cursor.execute(sql)
			# commit
			connection.commit()
	finally:
		connection.close()
#ket noi toi thiet bi juniper
def get_configuration(host,pre,command):
	dev = Device(host, user = 'nguyennd', password = 'bh6k8mfmnpk5bkh', port = '22')
	try:
		dev.open()
		content=dev.cli(command)
	except:
		print(host+'can not connect to device')
		content='can not connect to device'
	finally:
		dev.close()
	#return content
	file_name=pre+".txt"
	file=open(file_name,'w')
	file.write(content)
	file.close()
def filter(file_name,table):
	a=open(file_name+'.txt','r')
	data=a.readlines()
	for line in data:
		chuoi=line.split()
		if len(chuoi)>4:	
			if line.find('prefix-list')!=-1 and line.find('deactivate') ==-1:
				b=line.split()
				insert_mysql(b[3],b[4],table)
			elif line.find('prefix-list')!=-1 and line.find('deactivate') !=-1:
				b=line.split()
				de= "Deactivate-"+b[4]
				insert_mysql(b[3],de,table)
		else :
			if line.find('prefix-list')!=-1 and line.find('deactivate') ==-1:
				b=line.split()
				b.append('None')
				insert_mysql(b[3],b[4],table)
			
			
def insert_mysql(name,prefix,table):
	connection=pymysql.connect('10.255.254.236','nguyennd','bh6k8mfmnpk5','SCTV')
	try:
		with connection.cursor() as cursor:
			# insert a user
			sql = "INSERT INTO " + table + "(`name`,`prefix`) VALUES (%s, %s)"
			cursor.execute(sql,(name,prefix))
			# commit
			connection.commit()
	finally:
		connection.close()


def insert_mysql_new(name,prefix,stt,router,table,row_01,row_02,row_03,row_04):
	connection=pymysql.connect('10.255.254.236','nguyennd','bh6k8mfmnpk5','SCTV')
	try:
		with connection.cursor() as cursor:
			# insert a user
			sql = "INSERT INTO " + table + "("+row_01+", "+row_02+","+row_03+","+row_04+") VALUES ( %s,%s,%s,%s)"
			cursor.execute(sql,(name,prefix,stt,router))
			# commit
			connection.commit()
	finally:
		connection.close()
def cut_string(chuoi):
	data=chuoi.split('--')
	suma=''
	if len(data)>1:
		for x in range(len(data)):
			a=x+1
			for z in range(a,len(data)):
				if data[x]==data[z]:
					data[x]='mot'
					data[z]='hai'
		for k in range(len(data)):
			suma+=data[k]+'--'
	else:
		suma=chuoi
	return suma
		

policy_name=get_mysql('policy_prefix')
print(len(policy_name))
for n in range(len(policy_name)):
	print(policy_name[n][1])
	delete=del_mysql(policy_name[n][1])
del_mysql('policy_prefix_detail')
prefix_info=get_mysql('peering_info')
print(len(prefix_info))
for i in range(len(prefix_info)):
	cmd='show configuration policy-options prefix-list '+prefix_info[i][6]+' | display set'
	print(cmd)
	get_configuration(prefix_info[i][3],prefix_info[i][6],cmd)
for m in range(len(prefix_info)):
	cat=prefix_info[m][6].split('-')
	name=prefix_info[m][2].split('-')
	print(prefix_info[m][2])
	if len(cat)<4:
		cat.append(name[0])
		#print(cat[3])
		table='List_'+cat[2]+'_'+cat[3]
		print(table)
		filter(prefix_info[m][6],table)
		#insert_mysql_new(m,table,'policy_prefix','id','policy')
	else :
		cat.append(name[0])
		table_01='List_'+cat[2]+'_'+cat[3]
		print(table_01)		
		filter(prefix_info[m][6],table_01)
		#insert_mysql_new(m,table_01,'policy_prefix','id','policy')
print('fillter-data------------------------------------------------------')
for j in range(len(policy_name)):
	prefix_detail=get_mysql(policy_name[j][1])
	print(policy_name[j][1])
	name=prefix_detail[0][0]
	sumary=''
	for y in range(len(prefix_detail)):
		sumary+=prefix_detail[y][1]+"--"
	#sumary_01=cut_string(sumary)
	print(sumary)
	insert_mysql_new(name,sumary,j,prefix_info[j][2],'policy_prefix_detail','policy','prefix','stt','router')

#ts=get_mysql('List_HURRICANE_1127')
#name_01=prefix_detail[0][0]
#su=''
#for z in range(len(ts)):
#	su+=ts[z][1]+"--"
#tr=cut_string(su)
#print(tr)	