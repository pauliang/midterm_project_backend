# Create your views here.
import pymysql
from django.http import JsonResponse


def test_doc(request):
    con=pymysql.connect(host="39.97.101.50", port=3306, user="root", password="rjgcxxq", database="xxqdb", charset="utf8")
    cur=con.cursor()
    id=request.POST['num']
    # msg=request.POST['msg']
    # sql="insert into doctest values("+str(id)+","+'"'+msg+'"'+")"
    # print(sql)
    # cur.execute(sql)
    # cur.connection.commit()
    sql="select msg from doctest where id="+str(id)
    cur.execute(sql)
    chars=""
    for row in cur:
        chars=row[0]
    con.close()
    return JsonResponse(chars,safe=False)


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
    id=request.POST['id']
    sql="select groupnum from Grouplist order by groupnum desc limit 1"
    cur.execute(sql)
    for row in cur:
        groupnum=row[0]+1
    cur=con.cursor()
    sql="insert into Grouplist values("+'"'+str(groupname)+'"'+','+str(groupnum)+","+str(groupsize)+','+'"'+str(groupintro)+'"'+","+str(id)+")"
    cur.execute(sql)
    cur=con.cursor()
    sql="insert into Joinlist values("+str(groupnum)+","+str(id)+",1,1)"
    cur.execute(sql)
    cur.connection.commit()
    con.close()
    if(cur!=None):return JsonResponse(1,safe=False)
    else:return JsonResponse(0,safe=False)


def join_group(request):
    con=pymysql.connect(host="39.97.101.50", port=3306, user="root", password="rjgcxxq", database="xxqdb", charset="utf8")
    cur=con.cursor()
    # username=request.POST['username']
    # id=get_num_by_name(username)
    id=request.POST['id']
    groupnum=request.POST['groupnum']
    sql="select count(*) from Joinlist where id="+str(id)+" and groupnum="+str(groupnum)
    cur.execute(sql)
    join=0
    for row in cur:
        join=row[0]
    if join==1:return JsonResponse(2,safe=False)
    sql="insert into Joinlist values("+str(groupnum)+","+str(id)+",0,0)"
    cur.execute(sql)
    # cur.connection.commit()
    sql ="update Grouplist set groupsize=groupsize+1 where groupnum="+str(groupnum)
    cur.execute(sql)
    send_notice(id, groupnum, 1)
    cur.connection.commit()
    con.close()
    if(cur!=None):return JsonResponse(1,safe=False)
    else:return JsonResponse(0,safe=False)


def quit_group(request):
    con=pymysql.connect(host="39.97.101.50", port=3306, user="root", password="rjgcxxq", database="xxqdb", charset="utf8")
    cur=con.cursor()
    # username=request.POST['username']
    # id=get_num_by_name(username)
    id=request.POST['id']
    groupnum=request.POST['groupnum']
    sql = "select count(*) from Joinlist where id=" + str(id) + " and groupnum=" + str(groupnum)
    cur.execute(sql)
    join = 1
    for row in cur:
        join = row[0]
    if join == 0: return JsonResponse(2, safe=False)
    sql="delete from Joinlist where id="+str(id)+" and groupnum="+str(groupnum)
    cur.execute(sql)
    # cur.connection.commit()

    sql="select id from Table_file where author_id="+str(id)+" and groupnum="+str(groupnum)
    cur.execute(sql)
    for row in cur:
        docnum=row[0]
        change_stat_func(docnum,-1)

    send_notice(id, groupnum, -1)
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
    for id in users:
        sql="update Joinlist set isadmin=1 where id="+str(id)+" and groupnum="+str(groupnum)
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
    for id in users:
        cur=con.cursor()
        sql="update Joinlist set isadmin=0 where id="+str(id)+" and groupnum="+str(groupnum)
        cur.execute(sql)
    cur.connection.commit()
    con.close()
    if(cur!=None):return JsonResponse(1,safe=False)
    else:return JsonResponse(0,safe=False)


def get_users(request):
    con=pymysql.connect(host="39.97.101.50", port=3306, user="root", password="rjgcxxq", database="xxqdb", charset="utf8")
    cur=con.cursor()
    groupnum=request.POST['groupnum']
    sql="select username,auth_user.id,isleader,isadmin from (auth_user join Joinlist on auth_user.id=Joinlist.id) where groupnum="+str(groupnum)
    cur.execute(sql)
    con.close()
    return JsonResponse(cur.fetchall(),safe=False)


def get_groups(request):
    con = pymysql.connect(host="39.97.101.50", port=3306, user="root", password="rjgcxxq", database="xxqdb",charset="utf8")
    cur = con.cursor()
    id = request.POST['id']
    sql = "select groupname,Grouplist.groupnum,groupsize,groupintro from (Grouplist join Joinlist on Grouplist.groupnum=Joinlist.groupnum) where Joinlist.id=" + str(id)
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
    con = pymysql.connect(host="39.97.101.50", port=3306, user="root", password="rjgcxxq", database="xxqdb",charset="utf8")
    cur = con.cursor()
    id=request.POST['id']
    groupnum=request.POST['groupnum']
    groupname=""
    sql="select groupname from Grouplist wehre groupnum="+str(groupnum)
    cur.execute(sql)
    for row in cur:
        groupname=row[0]
    content="您已被管理员移出团队 "+groupname+"."
    sql = "insert into Noticelise values(," + str(id) + ",'" + content + "',now(),0)"
    cur.execute(sql)
    cur.connection.commit()
    con.close()
    return JsonResponse(quit_group_func(id,groupnum),safe=False)


def dismiss_group(request):
    con=pymysql.connect(host="39.97.101.50", port=3306, user="root", password="rjgcxxq", database="xxqdb", charset="utf8")
    cur=con.cursor()
    groupnum=request.POST['groupnum']
    sql="select id from Joinlist where groupnum="+str(groupnum)
    cur.execute(sql)
    for row in cur:
        id=row[0]
        quit_group_func(id,groupnum)
    sql="delete from Grouplist where groupnum="+str(groupnum)
    cur.execute(sql)
    cur.connection.commit()
    con.close()
    return JsonResponse(1,safe=False)


def send_invitation(request):
    con=pymysql.connect(host="39.97.101.50", port=3306, user="root", password="rjgcxxq", database="xxqdb", charset="utf8")
    cur=con.cursor()
    sendid=request.POST['id']
    groupnum=request.POST['groupnum']
    receivename=request.POST['receivename']
    receiveid=get_num_by_name(receivename)
    sql="insert into Msglist values("+str(sendid)+","+str(receiveid)+","+str(groupnum)+",0,now())"
    cur.execute(sql)
    cur.connection.commit()
    con.close()
    return JsonResponse(1,safe=False)


def get_invitation_a(request):
    con=pymysql.connect(host="39.97.101.50", port=3306, user="root", password="rjgcxxq", database="xxqdb", charset="utf8")
    cur=con.cursor()
    id=request.POST['id']
    sql="select auth_user.username,Grouplist.groupnum,Msglist.groupname,Msglist.ishandle,mtime from ((auth_user join Msglist on auth_user.id=Msglist.sendid) join Grouplist on Msglist.groupnum=Grouplist.groupnum) where Msglist.receiveid="+str(id)
    cur.execute(sql)
    con.close()
    return JsonResponse(cur.fetchall(),safe=False)


def get_invitation_b(request):
    con=pymysql.connect(host="39.97.101.50", port=3306, user="root", password="rjgcxxq", database="xxqdb", charset="utf8")
    cur=con.cursor()
    id=request.POST['id']
    sql="select auth_user.username,Grouplist.groupnum,Msglist.groupname,Msglist.ishandle,mtime from ((auth_user join Msglist on auth_user.id=Msglist.receiveid) join Grouplist on Msglist.groupnum=Grouplist.groupnum) where Msglist.sendid="+str(id)
    cur.execute(sql)
    con.close()
    return JsonResponse(cur.fetchall(),safe=False)


def handle_invitation(request):
    con=pymysql.connect(host="39.97.101.50", port=3306, user="root", password="rjgcxxq", database="xxqdb", charset="utf8")
    cur=con.cursor()
    id=request.POST['id']
    groupnum=request.POST['groupnum']
    op=request.POST['op']
    sql="update Msglist set ishandle="+str(op)+" where receiveid="+str(id)+" and groupnum="+str(groupnum)
    cur.execute(sql)
    if op==1:
        join_group_func(id,groupnum)
    cur.connection.commit()
    con.close()
    return JsonResponse(1,safe=False)


# def send_message(request):
#     con=pymysql.connect(host="39.97.101.50", port=3306, user="root", password="rjgcxxq", database="xxqdb", charset="utf8")
#     cur=con.cursor()
#     id=request.POST['id']
#     groupnum=request.POST['groupnum']
#     sql="insert into Msglist values("+str(id)+",,"+str(groupnum)+",0)"
#     cur.execute(sql)
#     cur.connection.commit()
#     con.close()
#     return JsonResponse(1,safe=False)
#
#
# def get_send_message(request):
#     con=pymysql.connect(host="39.97.101.50", port=3306, user="root", password="rjgcxxq", database="xxqdb", charset="utf8")
#     cur=con.cursor()
#     id=request.POST['id']
#     op=request.POST['op']
#     if op==1:sql="select groupname,ishandle from (Grouplist join Msglist where Grouplist.groupnum=Msglist.groupnum) and sendid="+str(id)
#     elif op==2:sql="select username,groupname,ishandle from (Grouplist join Msglist on Grouplist.groupnum=Msglist.groupnum) join auth_user on Msglist.receiveid=auth_user.id and sendid="+str(id)
#     cur.execute(sql)
#     con.close()
#     return JsonResponse(cur.fetchall(),safe=False)


def get_num_by_name(username):
    con=pymysql.connect(host="39.97.101.50", port=3306, user="root", password="rjgcxxq", database="xxqdb", charset="utf8")
    cur=con.cursor()
    sql="select id from auth_user where username="+username
    cur.execute(sql)
    for row in cur:
        id=row[0]
    con.close()
    return id


def quit_group_func(id,groupnum):
    con=pymysql.connect(host="39.97.101.50", port=3306, user="root", password="rjgcxxq", database="xxqdb", charset="utf8")
    cur=con.cursor()
    # username=request.POST['username']
    # id=get_num_by_name(username)
    # id=request.POST['id']
    # groupnum=request.POST['groupnum']
    sql = "select count(*) from Joinlist where id=" + str(id) + " and groupnum=" + str(groupnum)
    cur.execute(sql)
    join = 1
    for row in cur:
        join = row[0]
    if join == 0: return JsonResponse(2, safe=False)
    sql="delete from Joinlist where id="+str(id)+" and groupnum="+str(groupnum)

    cur.execute(sql)
    # cur.connection.commit()

    sql = "select id from Table_file where author_id=" + str(id) + " and groupnum=" + str(groupnum)
    cur.execute(sql)
    for row in cur:
        docnum = row[0]
        change_stat_func(docnum, -1)

    send_notice(id, groupnum, -1)

    #还需要再对文档的归属和权限作品进行处理
    sql = "update Grouplist set groupsize=groupsize-1 where groupnum=" + str(groupnum)
    print(sql)
    cur.execute(sql)
    cur.connection.commit()
    con.close()
    if(cur!=None):return JsonResponse(1,safe=False)
    else:return JsonResponse(0,safe=False)


def join_group_func(id,groupnum):
    con=pymysql.connect(host="39.97.101.50", port=3306, user="root", password="rjgcxxq", database="xxqdb", charset="utf8")
    cur=con.cursor()
    # username=request.POST['username']
    # id=get_num_by_name(username)
    # id=request.POST['id']
    # groupnum=request.POST['groupnum']
    sql="select count(*) from Joinlist where id="+str(id)+" and groupnum="+str(groupnum)
    cur.execute(sql)
    join=0
    for row in cur:
        join=row[0]
    if join==1:return JsonResponse(2,safe=False)
    sql="insert into Joinlist values("+str(groupnum)+","+str(id)+",0,0)"
    cur.execute(sql)
    # cur.connection.commit()
    sql ="update Grouplist set groupsize=groupsize+1 where groupnum="+str(groupnum)
    send_notice(id,groupnum,1)
    cur.execute(sql)
    cur.connection.commit()
    con.close()
    if(cur!=None):return JsonResponse(1,safe=False)
    else:return JsonResponse(0,safe=False)


def change_stat_func(docnum,stat):
    con=pymysql.connect(host="39.97.101.50", port=3306, user="root", password="rjgcxxq", database="xxqdb", charset="utf8")
    cur=con.cursor()
    sql="delete from Authlist where docnum="+str(docnum)
    cur.execute(sql)
    sql="update Table_file set stat="+str(stat)+" where docnum="+str(docnum)
    cur.execute(sql)
    cur.connection.commit()
    con.close()
    if cur!=None:return 1
    else:return 0


def send_notice(id,groupnum,op):
    con=pymysql.connect(host="39.97.101.50", port=3306, user="root", password="rjgcxxq", database="xxqdb", charset="utf8")
    cur=con.cursor()
    username=""
    groupname=""
    if op==1:opc="加入"
    elif op==-1:opc="退出"
    sql="select username from auth_user where id="+str(id)
    cur.execute(sql)
    for row in cur:
        username=row[0]
    sql = "select groupname from Grouplist where groupnum=" + str(groupnum)
    cur.execute(sql)
    for row in cur:
        groupname = row[0]
    content=username+" 已"+opc+"团队 "+groupname+"."
    sql="insert into Noticelise values(,"+str(id)+",'"+content+"',now(),0)"
    cur.execute(sql)
    cur.connection.commit()
    con.close()
    return 1