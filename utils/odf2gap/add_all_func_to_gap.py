# *-* coding=utf-8 *-* 
import xmlrpclib, sys, settings, re, pprint

username = settings.username
pwd = settings.pwd
dbname = settings.dbname

def connect():
    # Get the uid
    sock_common = xmlrpclib.ServerProxy ('http://localhost:8069/xmlrpc/common')
    uid = sock_common.login(dbname, username, pwd)

    #replace localhost with the address of the server
    sock = xmlrpclib.ServerProxy('http://localhost:8069/xmlrpc/object')
    return sock, uid

def borrar(sock, uid):
    buscar = []
    cod = sock.execute(dbname, uid, pwd, 'gap_analysis', 'search', buscar)
    for i in cod:
        sock.execute(dbname, uid, pwd, 'gap_analysis', 'unlink', cod)

def actualizar(sock, uid):
    cod = buscar(sock, uid, "all")
    fields = ['name', 'code', 'type', 'user_type']
    for i in cod:
        func = sock.execute(dbname, uid, pwd, 'gap_analysis', 'read', i, fields)

        values = {'attr': 'value', 'attr' : 'value'}
        
        modificar(sock, uid, i, values)

def modificar(sock, uid, ids, values):
    account_id = sock.execute(dbname, uid, pwd, 'gap_analysis', 'write', ids, values)

def buscar(sock, uid, code):
    if code == "":
        attr = []
    else:
        attr = code 
    cod = sock.execute(dbname, uid, pwd, 'gap_analysis', 'search', attr)
    return cod

def listar(sock, uid, code):
    gaps = []
    fields = []
    if code == "":
        attr = []
    else:
        attr = [('name','=', code)]
    cod = buscar(sock, uid, attr) 
    for i in cod:
        gap = sock.execute(dbname, uid, pwd, 'gap_analysis', 'read', i, fields)
        gaps.append(gap)
    return gaps

def crear_gap_lines(sock, uid, gap_name):
    line_id = 0
    functionalities = listar_gap_func(sock, uid, '')
    gap = listar(sock, uid, gap_name)

    for f in functionalities:
        line = {
            'category': f['category'][0],
            'code': False,
            'contributors': False,
            'critical': 4,
            'duration_wk': 0.0,
            'effort': False,
            'functionality': f['id'],
            'gap_id': gap[0]['id'],
            'id': line_id,
            'keep': True,
            'openerp_fct': False,
            'phase': '1',
            'seq': False,
            'testing': 0.0,
            'to_project': True,
            'total_cost': 0.0,
            'total_time': 0.0,
            'unknown_wk': False,
            'workloads': []
        }

        id_gap_line = sock.execute(dbname, uid, pwd, 'gap_analysis.line', 'create', line)
        line_id += 1

def buscar_gap_lines(sock, uid, code):
    if code == "":
        attr = []
    else:
        attr = code 
    cod = sock.execute(dbname, uid, pwd, 'gap_analysis.line', 'search', attr)
    return cod

def listar_gap_lines(sock, uid, code):
    lines = []
    fields = []
    if code == "":
        attr = []
    else:
        attr = [('gap_id','=', code)]
    cod = buscar_gap_lines(sock, uid, attr) 
    for i in cod:
        line = sock.execute(dbname, uid, pwd, 'gap_analysis.line', 'read', i, fields)
        lines.append(line)
    return lines

def buscar_gap_func(sock, uid, code):
    if code == "":
        attr = []
    else:
        attr = code 
    cod = sock.execute(dbname, uid, pwd, 'gap_analysis.functionality', 'search', attr)
    return cod

def listar_gap_func(sock, uid, code):
    functionalities = []
    fields = []
    if code == "":
        attr = []
    else:
        attr = [('gap_id','=', code)]
    cod = buscar_gap_func(sock, uid, attr) 
    for i in cod:
        types = sock.execute(dbname, uid, pwd, 'gap_analysis.functionality', 'read', i, fields)
        functionalities.append(types)
    return functionalities

def main():
    (sock, uid) = connect()

    #listar(sock, uid, 'cantv.com.ve')
    #listar_gap_lines(sock, uid, '1')
    #listar_gap_func(sock, uid, '')
    crear_gap_lines(sock, uid, "cantv.com.ve")#Inserta todas las funcionalidades al GAP con nombre cantv.com.ve

main()