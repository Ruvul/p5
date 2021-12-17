#from __future__ import print_function

import logging
from concurrent import futures
from concurrent.futures import Future
from concurrent.futures import ThreadPoolExecutor
import requests
import threading

import grpc
import usuarios_pb2
import usuarios_pb2_grpc
import os

usuarios=["Sofia","Eduardo","Juan"]
contra="123"

class Sistema(usuarios_pb2_grpc.SistemaServicer):
    """Missing associated documentation comment in .proto file."""

    def Login(self, request, context):
        if not usuarios.__contains__(request.nombre):
            return usuarios_pb2.RespuestaLogin(conf="Datos invalidos", codigo="1")
        elif request.contra!=contra:
            return usuarios_pb2.RespuestaLogin(conf="Datos invalidos", codigo="1")
        else:
            return usuarios_pb2.RespuestaLogin(conf="Login exitoso! Hola %s!"% request.nombre, codigo="0")

    def VerifHome(self, request, context):
        usuario = request.nombre
        direct = "home" + usuario
        print(direct)
        lista = os.listdir("C:/Users/Allan/Desktop/Redes 2/p5")
        print(lista)
        if not lista.__contains__(direct):
            path = os.path.join("C:/Users/Allan/Desktop/Redes 2/p5", direct)
            os.mkdir(path)
            rut = "C:/Users/Allan/Desktop/Redes 2/p5/" + direct
            return usuarios_pb2.RespuestaHome(ruta=rut)
        else:
            rut = "C:/Users/Allan/Desktop/Redes 2/p5/" + direct
            #print(ruta)
            return usuarios_pb2.RespuestaHome(ruta=rut)

    def Create(self, request, context):
        nombre_f=request.nombre
        ruta_f=request.ruta
        path=os.path.join(ruta_f, nombre_f)
        f = open(path, "wb")
        f.close()
        return usuarios_pb2.RespuestaCreate(conf="El archivo %s fue creado exitosamente!" % request.nombre)


    def Read(self, request, context):
        nombre_f=request.nombre
        ruta_f = request.ruta
        path = os.path.join(ruta_f, nombre_f)
        f = open(path, "rb")
        t1 = f.readlines()
        print("Archivo leido correctamente!")
        f.close()
        t=[]
        i=0
        while i<t1.__len__():
            temp=t1[i].decode("utf-8")
            t.append(temp)
            i+=1
        #print(t)
        i = 0
        while i < t.__len__()-1:
            t[i] = t[i].strip("\r\n")
            i += 1
        #print(t)
        for linea in t:
            texto=linea
            yield usuarios_pb2.RespuestaRead(contenido=texto)

    def Write(self, request, context):
        nombre_f=request.nombre
        ruta_f = request.ruta
        #print(ruta_f)
        path = os.path.join(ruta_f, nombre_f)
        f = open(path, "w")
        f.write(request.contenido)
        f.close()
        #print("Archivo modificado correctamente!")
        return usuarios_pb2.RespuestaWrite(conf="Archivo modificado correctamente!")

    def Rename(self, request, context):
        nombre_old=request.nombreOld
        nombre_new= request.nombreNew
        ruta_f = request.ruta
        path1 = os.path.join(ruta_f, nombre_old)
        path2 = os.path.join(ruta_f, nombre_new)
        os.rename(path1,path2)
        return usuarios_pb2.RespuestaRename(conf="Archivo renombrado correctamente!")

    def Remove(self, request, context):
        nombre_f=request.nombre
        ruta_f = request.ruta
        path = os.path.join(ruta_f, nombre_f)
        lista = os.listdir(ruta_f)
        if not lista.__contains__(nombre_f):
            return usuarios_pb2.RespuestaRemove(conf="El archivo no existe!")
        else:
            os.remove(path)
        return usuarios_pb2.RespuestaRemove(conf="Archivo borrado correctamente!")

    def Mkdir(self, request, context):
        directorio=request.nombre
        padre=request.ruta
        path=os.path.join(padre,directorio)
        lista = os.listdir(padre)
        if lista.__contains__(directorio):
            return usuarios_pb2.RespuestaMkdir(conf="El directorio ya existe!")
        else:
            os.mkdir(path)
        return usuarios_pb2.RespuestaMkdir(conf="Directorio creado correctamente!")

    def Rmdir(self, request, context):
        directorio=request.nombre
        padre=request.ruta
        path=os.path.join(padre,directorio)
        lista = os.listdir(padre)
        if not lista.__contains__(directorio):
            return usuarios_pb2.RespuestaMkdir(conf="El directorio no existe!")
        else:
            os.rmdir(path)
        return usuarios_pb2.RespuestaRmdir(conf="Directorio borrado correctamente!")

    def Readdir(self, request, context):
        padre=request.ruta
        lista=os.listdir(padre)

        for i in lista:
            ls = i
            yield usuarios_pb2.RespuestaReaddir(item=ls)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    usuarios_pb2_grpc.add_SistemaServicer_to_server(Sistema(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()