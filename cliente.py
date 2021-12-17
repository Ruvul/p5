from __future__ import print_function

import logging

import grpc
import usuarios_pb2
import usuarios_pb2_grpc

def Entrar(stub):
    print("Inicio de sesion:")
    name=input("Inserte el nombre de usuario: ")
    passw = input("Inserte la contraseña: ")
    respuesta=stub.Login(usuarios_pb2.SolicitudLogin(nombre=name, contra=passw))
    print("Respuesta recibida: " + respuesta.conf)

    if respuesta.codigo=="1":
        exit()
    else:
        return name

def Home(stub,nombre):
    print("Verificando directorio home...")
    name=nombre
    respuesta = stub.VerifHome(usuarios_pb2.SolicitudHome(nombre=name))
    return respuesta.ruta


def Crear(stub,ruta):
    print("CREATE:")
    name = input("Inserte el nombre del archivo a crear: ")
    respuesta=stub.Create(usuarios_pb2.SolicitudCreate(nombre=name,ruta=ruta))
    print("Respuesta recibida: " + respuesta.conf)

def Leer(stub,ruta):
    print("READ:")
    name = input("Inserte el nombre del archivo a leer: ")
    #respuesta=stub.Read(usuarios_pb2.SolicitudRead(nombre=name,ruta=ruta))
    #cont=respuesta.contenido
    print("Respuesta recibida. Contenido del archivo:")
    print("")
    for respuesta in stub.Read(usuarios_pb2.SolicitudRead(nombre=name,ruta=ruta)):
        print(respuesta.contenido)
    print("Archivo leido correctamente!")
    #print(cont)

def Escribir(stub,ruta):
    print("WRITE:")
    name = input("Inserte el nombre del archivo a editar: ")
    cont= input("Inserte el contenido del archivo: ")
    respuesta = stub.Write(usuarios_pb2.SolicitudWrite(nombre=name, contenido=cont,ruta=ruta))
    print("Respuesta recibida: " + respuesta.conf)

def Renombrar(stub,ruta):
    print("RENAME:")
    nombreViejo=input("Inserte el nombre del archivo a renombrar: ")
    nombreNuevo=input("Inserte el nuevo nombre del archivo: ")
    respuesta = stub.Rename(usuarios_pb2.SolicitudRename(nombreOld=nombreViejo, nombreNew=nombreNuevo,ruta=ruta))
    print("Respuesta recibida: " + respuesta.conf)

def Borrar(stub,ruta):
    print("REMOVE:")
    name = input("Inserte el nombre del archivo a borrar: ")
    respuesta = stub.Remove(usuarios_pb2.SolicitudRemove(nombre=name,ruta=ruta))
    print("Respuesta recibida: " + respuesta.conf)

def CreaDirect(stub,ruta):
    print("MKDIR:")
    nombre2=input("Inserte el nombre del directorio a crear: ")
    respuesta = stub.Mkdir(usuarios_pb2.SolicitudMkdir(nombre=nombre2, ruta=ruta))
    print("Respuesta recibida: " + respuesta.conf)

def BorraDirect(stub,ruta):
    print("MKDIR:")
    nombre2 = input("Inserte el nombre del directorio a borrar: ")
    respuesta = stub.Rmdir(usuarios_pb2.SolicitudRmdir(nombre=nombre2, ruta=ruta))
    print("Respuesta recibida: " + respuesta.conf)

def ScanDirect(stub,ruta):
    print("READDIR:")
    #ruta2 = input("Inserte la ruta del directorio a escanear: ")
    print("Respuesta recibida. Contenido del directorio:")

    for respuesta in stub.Readdir(usuarios_pb2.SolicitudReaddir(ruta=ruta)):
        print(respuesta.item)

def run():

    with grpc.insecure_channel('localhost:50051') as channel:
        stub = usuarios_pb2_grpc.SistemaStub(channel)

        usuario=Entrar(stub)
        ruta=Home(stub,usuario)
        print(ruta)
        #Crear(stub,ruta)
        #Leer(stub,ruta)
        #Escribir(stub,ruta)
        Renombrar(stub,ruta)
        Borrar(stub, ruta)
        CreaDirect(stub,ruta)
        BorraDirect(stub,ruta)
        ScanDirect(stub,ruta)



if __name__ == '__main__':
    logging.basicConfig()
    run()