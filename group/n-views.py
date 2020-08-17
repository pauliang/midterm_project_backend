# Create your views here.
import pymysql
from django.http import JsonResponse


def test_post(request):
    con=pymysql.connect(host="39.97.101.50", port=3306, user="root", password="rjgcxxq", database="xxqdb", charset="utf8")
    cur=con.cursor()
    sql="select * from Testlist"
    cur.execute(sql)
    con.close()
    return JsonResponse(cur.fetchall(),safe=False)


def create_group(request):
    con=pymysql.connect(host="39.97.101.50", port=3306, user="root", password="rjgcxxq", database="xxqdb", charset="utf8")
    cur=con.cursor()
    groupname=request.POST['groupname']
    groupsize=1
    groupintro=request.POST['groupintro']
    usernum=request.POST['usernum']
    sql="select groupnum from Grouplist order by groupnum desc limit 1"
    cur.execute(sql)
    for row in cur:
        groupnum=row[0]+1
    cur=con.cursor()
    sql="insert into Grouplist values("+'"'+str(groupname)+'"'+','+str(groupnum)+","+str(groupsize)+','+'"'+str(groupintro)+'"'+","+str(usernum)+")"
    cur.execute(sql)
    cur=con.cursor()
    sql="insert into Joinlist values("+str(groupnum)+","+str(usernum)+",1,1)"
    cur.execute(sql)
    cur.connection.commit()
    con.close()
    if(cur!=None):return JsonResponse(1,safe=False)
    else:return JsonResponse(0,safe=False)


def join_group(request):
    con=pymysql.connect(host="39.97.101.50", port=3306, user="root", password="rjgcxxq", database="xxqdb", charset="utf8")
    cur=con.cursor()
    # username=request.POST['username']
    # usernum=get_num_by_name(username)
    usernum=request.POST['usernum']
    groupnum=request.POST['groupnum']
    sql="select count(*) from Joinlist where usernum="+str(usernum)+" and groupnum="+str(groupnum)
    cur.execute(sql)
    join=0
    for row in cur:
        join=row[0]
    if join==1:return JsonResponse(2,safe=False)
    sql="insert into Joinlist values("+str(groupnum)+","+str(usernum)+",0,0)"
    cur.execute(sql)
    # cur.connection.commit()
    sql ="update Grouplist set groupsize=groupsize+1 where groupnum="+str(groupnum)
    cur.execute(sql)
    cur.connection.commit()
    con.close()
    if(cur!=None):return JsonResponse(1,safe=False)
    else:return JsonResponse(0,safe=False)


def quit_group(request):
    con=pymysql.connect(host="39.97.101.50", port=3306, user="root", password="rjgcxxq", database="xxqdb", charset="utf8")
    cur=con.cursor()
    # username=request.POST['username']
    # usernum=get_num_by_name(username)
    usernum=request.POST['usernum']
    groupnum=request.POST['groupnum']
    sql = "select count(*) from Joinlist where usernum=" + str(usernum) + " and groupnum=" + str(groupnum)
    cur.execute(sql)
    join = 1
    for row in cur:
        join = row[0]
    if join == 0: return JsonResponse(2, safe=False)
    sql="delete from Joinlist where usernum="+str(usernum)+" and groupnum="+str(groupnum)
    cur.execute(sql)
    # cur.connection.commit()
    #还需要再对文档的归属和权限作品进行处理
    sql = "update Grouplist set groupsize=groupsize-1 where groupnum=" + str(groupnum)
    print(sql)
    cur.execute(sql)
    cur.connection.commit()
    con.close()
    if(cur!=None):return JsonResponse(1,safe=False)
    else:return JsonResponse(0,safe=False)


def set_admin(request):
    con=pymysql.connect(host="39.97.101.50", port=3306, user="root", password="rjgcxxq", database="xxqdb", charset="utf8")
    cur=con.cursor()
    users=request.POST['users']
    groupnum=request.POST['groupnum']
    users=users.split(',')
    for usernum in users:
        sql="update Joinlist set isadmin=1 where usernum="+str(usernum)+" and groupnum="+str(groupnum)
        cur.execute(sql)
    cur.connection.commit()
    con.close()
    if(cur!=None):return JsonResponse(1,safe=False)
    else:return JsonResponse(0,safe=False)


def cancel_admin(request):
    con=pymysql.connect(host="39.97.101.50", port=3306, user="root", password="rjgcxxq", database="xxqdb", charset="utf8")
    cur=con.cursor()
    users=request.POST['users']
    groupnum=request.POST['groupnum']
    users=users.split(',')
    for usernum in users:
        cur=con.cursor()
        sql="update Joinlist set isadmin=0 where usernum="+str(usernum)+" and groupnum="+str(groupnum)
        cur.execute(sql)
    cur.connection.commit()
    con.close()
    if(cur!=None):return JsonResponse(1,safe=False)
    else:return JsonResponse(0,safe=False)


def get_users(request):
    con=pymysql.connect(host="39.97.101.50", port=3306, user="root", password="rjgcxxq", database="xxqdb", charset="utf8")
    cur=con.cursor()
    groupnum=request.POST['groupnum']
    sql="select username,Userlist.usernum,isleader,isadmin from (Userlist join Joinlist on Userlist.usernum=Joinlist.usernum) where groupnum="+str(groupnum)
    cur.execute(sql)
    con.close()
    return JsonResponse(cur.fetchall(),safe=False)


def get_groups(request):
    con = pymysql.connect(host="39.97.101.50", port=3306, user="root", password="rjgcxxq", database="xxqdb",charset="utf8")
    cur = con.cursor()
    usernum = request.POST['usernum']
    sql = "select groupname,Grouplist.groupnum,groupsize,groupintro from (Grouplist join Joinlist on Grouplist.groupnum=Joinlist.groupnum) where Joinlist.usernum=" + str(usernum)
    cur.execute(sql)
    con.close()
    return JsonResponse(cur.fetchall(), safe=False)


def search_groups(request):
    con = pymysql.connect(host="39.97.101.50", port=3306, user="root", password="rjgcxxq", database="xxqdb",charset="utf8")
    cur = con.cursor()
    key = request.POST['key']
    sql = "select groupname,Grouplist.groupnum,groupsize,groupintro from Grouplist where groupname like '%"+key+"%'"
    cur.execute(sql)
    con.close()
    return JsonResponse(cur.fetchall(), safe=False)


def kick_out_user(request):
    usernum=request.POST['usernum']
    groupnum=request.POST['groupnum']
    return JsonResponse(quit_group_func(usernum,groupnum),safe=False)


def dismiss_group(request):
    con=pymysql.connect(host="39.97.101.50", port=3306, user="root", password="rjgcxxq", database="xxqdb", charset="utf8")
    cur=con.cursor()
    groupnum=request.POST['groupnum']
    sql="select usernum from Joinlist where groupnum="+str(groupnum)
    cur.execute(sql)
    for row in cur:
        usernum=row[0]
        quit_group_func(usernum,groupnum)
    sql="delete from Grouplist where groupnum="+str(groupnum)
    cur.connection.commit()
    con.close()
    return JsonResponse(1,safe=False)


# def send_message(request):



def get_num_by_name(username):
    con=pymysql.connect(host="39.97.101.50", port=3306, user="root", password="rjgcxxq", database="xxqdb", charset="utf8")
    cur=con.cursor()
    sql="select usernum from Userlist where username="+username
    cur.execute(sql)
    for row in cur:
        usernum=row[0]
    con.close()
    return usernum


def quit_group_func(usernum,groupnum):
    con=pymysql.connect(host="39.97.101.50", port=3306, user="root", password="rjgcxxq", database="xxqdb", charset="utf8")
    cur=con.cursor()
    # username=request.POST['username']
    # usernum=get_num_by_name(username)
    # usernum=request.POST['usernum']
    # groupnum=request.POST['groupnum']
    sql = "select count(*) from Joinlist where usernum=" + str(usernum) + " and groupnum=" + str(groupnum)
    cur.execute(sql)
    join = 1
    for row in cur:
        join = row[0]
    if join == 0: return JsonResponse(2, safe=False)
    sql="delete from Joinlist where usernum="+str(usernum)+" and groupnum="+str(groupnum)
    cur.execute(sql)
    # cur.connection.commit()
    #还需要再对文档的归属和权限作品进行处理
    sql = "update Grouplist set groupsize=groupsize-1 where groupnum=" + str(groupnum)
    print(sql)
    cur.execute(sql)
    cur.connection.commit()
    con.close()
    if(cur!=None):return JsonResponse(1,safe=False)
    else:return JsonResponse(0,safe=False)