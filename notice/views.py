from django.shortcuts import render

# Create your views here.
import pymysql
from django.http import JsonResponse


def get_notice(request):
    con=pymysql.connect(host="39.97.101.50", port=3306, user="root", password="rjgcxxq", database="xxqdb", charset="utf8")
    cur=con.cursor()
    id=request.POST['id']
    sql="select content,ntime from Noticelist where receiveid="+str(id)
    cur.execute(sql)
    con.close()
    return JsonResponse(cur.fetchall(),safe=False)