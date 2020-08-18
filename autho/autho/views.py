from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
import pymysql


def test(aloha):
    con=pymysql.connect(host="39.97.101.50", port=3306, user="root", password="rjgcxxq", database="xxqdb", charset="utf8")
    cur=con.cursor()
    cur.execute('select * from test')
    # for row in cur:
    #     print(row[0])
    con.close()
    return JsonResponse([[1,5,'ccn'],[6,7,8,9],[10]],safe=False)
    #return JsonResponse('hello!', safe=False)


def change_stat(request):
    con=pymysql.connect(host="39.97.101.50", port=3306, user="root", password="rjgcxxq", database="xxqdb", charset="utf8")
    cur=con.cursor()
    docnum=request.POST['docnum']
    stat=request.POST['stat']
    sql="update Table_file set stat="+str(stat)+" where id="+str(docnum)
    cur.execute(sql)
    cur.connection.commit()
    con.close()
    if cur!=None:return JsonResponse(1, safe=False)
    else:return JsonResponse(0, safe=False)


def set_user_auth(request):
    con=pymysql.connect(host="39.97.101.50", port=3306, user="root", password="rjgcxxq", database="xxqdb", charset="utf8")
    cur=con.cursor()
    id=request.POST['id']
    docnum=request.POST['docnum']
    stat=request.POST['stat']
    sql="select count(*) from Authlist where id="+str(id)+" and docnum="+str(docnum)
    cur.execute(sql)
    exist=0
    for row in cur:
        if row[0]!=0:exist=1
    cur=con.cursor()
    if exist==1:
        sql="update Authlist set stat="+str(stat)+" where id="+str(id)+" and docnum="+str(docnum)
    else:
        sql="insert into Authlist values("+str(id)+","+str(docnum)+","+str(stat)+")"
    cur.execute(sql)
    con.close()
    if cur!=None:return JsonResponse(1, safe=False)
    else:return JsonResponse(0, safe=False)


def match_auth(request):
    rarr=[0,0,0]
    con=pymysql.connect(host="39.97.101.50", port=3306, user="root", password="rjgcxxq", database="xxqdb", charset="utf8")
    cur=con.cursor()
    id=request.POST['id']
    id=int(id)
    docnum=request.POST['docnum']
    sql="select author_id from Table_file where id="+str(docnum)
    cur.execute(sql)
    aid=0
    for row in cur:
        aid=row[0]
    if aid==id:return JsonResponse([1,1,1],safe=False)
    sql="select stat from Table_file where id="+str(docnum)
    cur.execute(sql)
    docstat=-1
    for row in cur:
        docstat=row[0]
    sql = "select count(*) from Authlist where id=" + str(id) + " and docnum=" + str(docnum)
    sql += " and stat=" + str(docstat)
    cur=con.cursor()
    cur.execute(sql)
    for row in cur:
        bool=row[0]
    if bool==1:rarr=[1,1,1]
    else:
        if docstat<=-1:rarr=[0,0,0]
        elif docstat==0:rarr=[1,1,0]
        elif docstat==1:rarr=[1,0,0]
        elif docstat==3:
            sql="select groupnum from Table_file where id="+str(docnum)
            cur.execute(sql)
            for row in cur:
                g=row[0]
            sql="select * from Joinlist where groupnum="+str(g)+" and id="+str(id)
            cur.execute(sql)
            if cur.fetchone()!=None:rarr=[1,1,0]
    con.close()
    if cur!=None:return JsonResponse(rarr, safe=False)
    else:return JsonResponse(0, safe=False)


def set_doc_auth(request):
    con=pymysql.connect(host="39.97.101.50", port=3306, user="root", password="rjgcxxq", database="xxqdb", charset="utf8")
    cur=con.cursor()
    users=request.POST['users']
    docnum=request.POST['docnum']
    stat=request.POST['stat']
    a=change_stat_func(docnum,stat)
    b=1
    if users!="":
        users=users.split(",")
        for username in users:
            sql="select id from auth_user where username="+"'"+username+"'"
            cur.execute(sql)
            for row in cur:
                id=row[0]
            b*=set_user_auth_func(id,docnum,stat)
    con.close()
    if a and b:return JsonResponse(1,safe=False)
    else:JsonResponse(0,safe=False)


def set_group_auth(request):
    con=pymysql.connect(host="39.97.101.50", port=3306, user="root", password="rjgcxxq", database="xxqdb", charset="utf8")
    cur=con.cursor()
    docnum=request.POST['docnum']
    groupnum=request.POST['groupnum']
    change_stat_func(docnum,2)
    sql="select id from Joinlist where groupnum="+str(groupnum)
    cur.execute(sql)
    for row in cur:
        id=row[0]
        set_user_auth_func(id,docnum,2)
    con.close()
    return JsonResponse(1,safe=False)


def set_admin_auth(request):
    con=pymysql.connect(host="39.97.101.50", port=3306, user="root", password="rjgcxxq", database="xxqdb", charset="utf8")
    cur=con.cursor()
    docnum=request.POST['docnum']
    groupnum=request.POST['groupnum']
    change_stat_func(docnum,3)
    sql="select id from Joinlist where isadmin=1 and groupnum="+str(groupnum)
    cur.execute(sql)
    for row in cur:
        id=row[0]
        set_user_auth_func(id,docnum,3)
    con.close()
    return JsonResponse(1,safe=False)


def change_owner(request):
    con=pymysql.connect(host="39.97.101.50", port=3306, user="root", password="rjgcxxq", database="xxqdb", charset="utf8")
    cur=con.cursor()
    id=request.POST['id']
    sql="update Table_file set groupnum=-1 where id="+str(id)
    change_stat_func(id,-1)
    cur.execute(sql)
    cur.connection.commit()
    con.close()
    return JsonResponse(1,safe=False)


def change_owner_b(request):
    con=pymysql.connect(host="39.97.101.50", port=3306, user="root", password="rjgcxxq", database="xxqdb", charset="utf8")
    cur=con.cursor()
    id=request.POST['id']
    groupnum=request.POST['groupnum']
    sql="update Table_file set groupnum="+str(groupnum)+" where id="+str(id)
    cur.execute(sql)
    sql="delete from Table_file where id="+str(id)
    cur.execute(sql)
    change_stat_func(id, 2)
    sql = "select id from Joinlist where groupnum=" + str(groupnum)
    cur.execute(sql)
    for row in cur:
        uid = row[0]
        set_user_auth_func(uid, id, 2)

    cur.execute(sql)
    cur.connection.commit()
    con.close()
    return JsonResponse(1,safe=False)


def change_stat_func(docnum,stat):
    con=pymysql.connect(host="39.97.101.50", port=3306, user="root", password="rjgcxxq", database="xxqdb", charset="utf8")
    cur=con.cursor()
    sql="update Table_file set stat="+str(stat)+" where id="+str(docnum)
    cur.execute(sql)
    cur.connection.commit()
    con.close()
    if cur!=None:return 1
    else:return 0


def set_user_auth_func(id,docnum,stat):
    con=pymysql.connect(host="39.97.101.50", port=3306, user="root", password="rjgcxxq", database="xxqdb", charset="utf8")
    cur=con.cursor()
    sql="select count(*) from Authlist where id="+str(id)+" and docnum="+str(docnum)
    cur.execute(sql)
    exist=0
    for row in cur:
        if row[0]!=0:exist=1
    cur=con.cursor()
    if exist==1:
        sql="update Authlist set stat="+str(stat)+" where id="+str(id)+" and docnum="+str(docnum)
    else:
        sql="insert into Authlist values("+str(id)+","+str(docnum)+","+str(stat)+")"
    cur.execute(sql)
    cur.connection.commit()
    con.close()
    if cur!=None:return 1
    else:return 0


