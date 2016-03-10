#---------------Horarios Para Colegios.-----------------------

import random
from random import *
from copy import deepcopy
nbloques = 8
semana = ["Lu", "Ma", "Mi", "Ju", "Vi"]
blocktrue = [True, True, True, True, True, True, True, True]
blockfalse = [False, False, False, False, False, False, False, False]


# Primero se crean carga y crusos como elementos para operar, son leidos desde 
# un archivo llamado "carga.dat"

def leer_carga_y_cursos():
	carga = {}
	fijos = {}
	cursos = []
	datos = file("carga.dat", "r")

	for line in datos:

		temp = []

		for a in line.split():
			temp.append(a)
	
		for i in range(1,len(temp)/2):
			#if temp[0] not in carga: 
			#	carga[temp[0]]= {}
	   		if temp[1] not in carga:
				carga[temp[1]]= {}
				if temp[0]=="Fijo":
					fijos[temp[1]]= {}
	   		if temp[2*i] not in carga[temp[1]]:
				carga[temp[1]][temp[2*i]] = 0
				if temp[0]=="Fijo":
					fijos[temp[1]][temp[2*i]]= 0

	   		carga[temp[1]][temp[2*i]] = int(temp[2*i+1])

			if temp[0] == "Fijo":	   
	   			fijos[temp[1]][temp[2*i]] = int(temp[2*i+1])

	   		if temp[2*i] not in cursos:
				cursos.append(temp[2*i])
	     
	datos.close()

	return carga, cursos, fijos

#Leer la disponibilidad horaria de los profesores.

def leer_disponibilidad_profes():
        profesor = {}
        datos = file("disponible.dat", "r")

        for line in datos:

                temp = []

                for a in line.split():
                        temp.append(a)

                for i in range(1,len(temp)/2):
                        if temp[1] not in profesor:
                                profesor[temp[1]] = {}
                        if temp[2*i] not in profesor[temp[1]]:
                                profesor[temp[1]][temp[2*i]] = []
                        profesor[temp[1]][temp[2*i]].append(temp[2*i+1])

        datos.close()

        return profesor

carga, cursos, fijos = leer_carga_y_cursos()
carga_inicial = deepcopy(carga)

def leer_disponibilidad_bool():
        profesor = {}
        for line in open("disponible.dat", "r"):
                temp = []
                for a in line.split():	temp.append(a)
              	if temp[1] not in profesor:	
			profesor[temp[1]] = {}
		for dia in semana:	
			profesor[temp[1]][dia] = deepcopy(blocktrue)

        for line in open("disponible.dat", "r"):

                temp = []
                for a in line.split():	temp.append(a)
                for i in range(1,len(temp)/2):
			dia = temp[2*i]
			bloque = temp[2*i+1]
			profe = temp[1]
			if bloque == "todo":
				profesor[profe][dia] = deepcopy(blockfalse)
			else:
				profesor[profe][dia][int(bloque)-1] = False

	for prof in carga:
		if prof not in profesor:
			profesor[prof] = {}
			for dia in semana:
				profesor[prof][dia] = deepcopy(blocktrue)		

        return profesor



def profesores_de_curso():
	prof_de_curso = {}
	for curso in cursos:
		   	for profe in carga:
        			if curso in carga[profe]:
		 			if curso not in prof_de_curso:
		 				prof_de_curso[curso] = []
					prof_de_curso[curso].append(profe)	
	return prof_de_curso


profdecurso = profesores_de_curso()

def horas_disp():
	horas_disp = {}
        for profe in disponible:
                if profe not in fijos:
                        cont = 0
                        for dia in disponible[profe]:
                                for j in range(8):
                                        if disponible[profe][dia][j]:
                                                cont += 1
                                        else:
                                                pass

                        horas_disp[profe] = cont
                else:
                        pass

        for profe in carga:
                if profe not in horas_disp and profe not in fijos:
                        horas_disp[profe] = 40
	
	return horas_disp


disponible = leer_disponibilidad_bool()
#profdecurso = profesores_de_curso()
#carga_inicial = deepcopy(carga)
horas_disp = horas_disp()

def mostrar_horario(horarios):
        for ano in horarios:
                        print " "
                        print "Curso:  ", ano
                        print " "
                        print "       Lu         Ma          Mi        Ju         Vi"
                        print " "
                        for n in range(8):

                                texto = str(n+1)
                                texto += " "
                                for dia in semana:
                                        texto += "  "
                                        texto += str(horarios[ano][dia][n])
                                        texto += "  "
                                print texto

def carga_horaria():
        for profe in carga:
                if profe not in fijos:
                        cont = 0
                        for curso in carga[profe]:
                                cont += carga[profe][curso]
                        print "Profesor:        ", profe, "     Horas Total Semana:", cont
                        print " "
                else:
                        pass

def horas_cursos():

        for curso in cursos:
                cont = 0
                for profe in profdecurso[curso]:
                        cont += carga[profe][curso]
                print "Curso:   ", curso, "     Horas Semana:   ", cont


def carga_curso(curso_ask):
        print curso_ask
        for profe in profdecurso[curso_ask]:
                print "Profesor:        ", profe, "     ",carga_inicial[profe][curso_ask]


def prof_dh(carga, dia, hora, horarios):
        carga_temp = deepcopy(carga)
        prof_dia_hora = []
        for curso_temp in carga_temp:
                prof_dia_hora.append(horarios[curso_temp][dia][hora])
        return prof_dia_hora


def cambio(horarios, n):
        desorden = 0
        while desorden<n:
                curso = choice(cursos)
                dia1, dia2 = choice(semana), choice(semana)
                hora1, hora2 = randint(0,7), randint(0,7)
                profe1 = horarios[curso][dia1][hora1]
                profe2 = horarios[curso][dia2][hora2]
		if profe1 != "0" and profe2 != "0":
                	if disponible[profe1][dia2][hora2] and disponible[profe2][dia1][hora1] and profe1 not in prof_dh(carga[profe1], dia2, hora2, horarios) and profe2 not in prof_dh(carga[profe2], dia1, hora1, horarios):
                        	horarios[curso][dia1][hora1] = profe2
                        	horarios[curso][dia2][hora2] = profe1
                        	desorden += 1

def cambio_2(horarios, n):
        desorden = 0
        while desorden<n:
                curso = choice(cursos)
                dia1, dia2 = choice(semana), choice(semana)
                hora1, hora2 = randint(0,7), randint(0,7)
                profe1 = horarios[curso][dia1][hora1]
                profe2 = horarios[curso][dia2][hora2]
                if hora1%2==0:  profe1_2 = horarios[curso][dia1][hora1+1]
                else:   profe1_2 = horarios[curso][dia1][hora1-1]
                if hora2%2==0:  profe2_2 = horarios[curso][dia2][hora2+1]
                else:   profe2_2 = horarios[curso][dia2][hora2-1]
                if hora1%2==0 and hora2%2==0:
                        if disponible[profe1][dia2][hora2] and disponible[profe1_2][dia2][hora2+1] and disponible[profe2][dia1][hora1] and disponible[profe2_2][dia1][hora1+1] and profe1 not in prof_dh(carga[profe1], dia2, hora2, horarios) and profe1_2 not in prof_dh(carga[profe1_2], dia2, hora2+1, horarios) and profe2 not in prof_dh(carga[profe2], dia1, hora1, horarios) and profe2_2 not in prof_dh(carga[profe2_2],dia1,hora1+1, horarios):
                                horarios[curso][dia1][hora1] = profe2
                                horarios[curso][dia1][hora1+1] = profe2_2
                                horarios[curso][dia2][hora2] = profe1
                                horarios[curso][dia2][hora2+1]=profe1_2
                                desorden += 1
                elif hora1%2==0 and hora2%2!=0:
                        if disponible[profe1][dia2][hora2] and disponible[profe1_2][dia2][hora2-1] and disponible[profe2][dia1][hora1] and disponible[profe2_2][dia1][hora1+1] and profe1 not in prof_dh(carga[profe1], dia2, hora2,horarios) and profe1_2 not in prof_dh(carga[profe1_2], dia2, hora2-1,horarios) and profe2 not in prof_dh(carga[profe2], dia1, hora1,horarios) and profe2_2 not in prof_dh(carga[profe2_2],dia1,hora1+1,horarios):
                                horarios[curso][dia1][hora1] = profe2
                                horarios[curso][dia1][hora1+1] = profe2_2
                                horarios[curso][dia2][hora2] = profe1
                                horarios[curso][dia2][hora2-1]=profe1_2
                                desorden += 1
                elif hora1%2!=0 and hora2%2==0:
                        if disponible[profe1][dia2][hora2] and disponible[profe1_2][dia2][hora2+1] and disponible[profe2][dia1][hora1] and disponible[profe2_2][dia1][hora1-1] and profe1 not in prof_dh(carga[profe1], dia2, hora2,horarios) and profe1_2 not in prof_dh(carga[profe1_2], dia2, hora2+1,horarios) and profe2 not in prof_dh(carga[profe2], dia1, hora1,horarios) and profe2_2 not in prof_dh(carga[profe2_2],dia1,hora1-1,horarios):
                                horarios[curso][dia1][hora1] = profe2
                                horarios[curso][dia1][hora1-1] = profe2_2
                                horarios[curso][dia2][hora2] = profe1
                                horarios[curso][dia2][hora2+1]=profe1_2
                                desorden += 1
                else:#if hora1%2!=0 and hora2%2!=0:
                        if disponible[profe1][dia2][hora2] and disponible[profe1_2][dia2][hora2-1] and disponible[profe2][dia1][hora1] and disponible[profe2_2][dia1][hora1-1] and profe1 not in prof_dh(carga[profe1], dia2, hora2,horarios) and profe1_2 not in prof_dh(carga[profe1_2], dia2, hora2-1,horarios) and profe2 not in prof_dh(carga[profe2], dia1, hora1,horarios) and profe2_2 not in prof_dh(carga[profe2_2],dia1,hora1-1, horarios):
                                horarios[curso][dia1][hora1] = profe2
                                horarios[curso][dia1][hora1-1] = profe2_2
                                horarios[curso][dia2][hora2] = profe1
                                horarios[curso][dia2][hora2-1]=profe1_2
                                desorden += 1



#carga, cursos, fijos = leer_carga_y_cursos()
#disponible = leer_disponibilidad_bool()
#profdecurso = profesores_de_curso()
carga_inicial = deepcopy(carga)



def shuffle_vacios(horarios, n):
   j=0
   cont0 = 0
   curso = choice(cursos)
   if True:
   #for curso in horarios:
        for dia in horarios[curso]:
                for hora in range(8):
                        if horarios[curso][dia][hora] == "0":
                           while j<n:
                                dia_r = choice(semana)
                                hora_r = randint(0,7)
                                profe_r = horarios[curso][dia_r][hora_r]
                                if profe_r == "0" or profe_r in fijos:
                                        cont0 += 1

                                elif disponible[profe_r][dia_r][hora_r] and profe_r not in prof_dh(carga[profe_r], dia, hora,horarios):
                                                horarios[curso][dia][hora] = profe_r
                                                horarios[curso][dia_r][hora_r] = "0"
                                                #print "Moviendo 0 desde : ", curso, dia, hora
                                                j+=1
                                                cont0 = 0
                                else:
                                        cont0 += 1
                                #if cont0 == 500:

def llenarvacio(horarios, n):
        j = 0
        for curso in horarios:
                for dia in horarios[curso]:
                        for hora in range(8):
                                if horarios[curso][dia][hora]== "0":
                                      for profe in carga:
                                         if curso in carga[profe] and j<n:
                                            if carga[profe][curso] > 0 and disponible[profe][dia][hora] and profe not in prof_dh(carga[profe], dia, hora,horarios):
                                                horarios[curso][dia][hora] = profe
                                                carga[profe][curso] -= 1
                                                #print "Agregando: ", profe, " en ", curso, dia, hora
                                                j += 1

def horas_total(carga):
        cont1 = 0
        for profe in carga:
                for curso in carga[profe]:
                        horas = carga[profe][curso]
                        if horas == 0:  pass
                        else:   cont1 += horas
        return cont1

def prueba_de_consistencia(carga, horarios, nbloques):
        cont1, cont2 = 0, 0
        #profes_restantes = {}
        for profe in carga:
                for curso in carga[profe]:
                        horas = carga[profe][curso]
                        #if curso not in profes_restantes:       profes_restantes[curso] = []
                        if horas == 0:  pass
                        else:
                               # if profe not in profes_restantes[curso]:
                                #        profes_restantes[curso].append(profe)
                                cont1 += horas
        for curso in horarios:
                for dia in horarios[curso]:
                        for hora in range(nbloques):
                                if horarios[curso][dia][hora]=="0":
                                        cont2 += 1
        print "\nHoras para asignar:  ", cont1, "\nBloques disponibles para asignar:  ", cont2
        if cont1 == cont2:      print "\nCorrecto!"
        else:   print "\nError!"



def asignar_fijos(fijos, carga, horarios):
	for fijo in fijos:
		for curso in horarios:
			for dia in semana:
				for hora in range(nbloques):
					if fijo in profdecurso[curso] and disponible[fijo][dia][hora] and carga[fijo][curso] > 0 and horarios[curso][dia][hora]=="0":
						horarios[curso][dia][hora] = fijo
						carga[fijo][curso] -= 1
					else:
						pass

def minimizar(horarios, energia, minimo):
        while energia(horarios)> minimo:
                horarios_ant = deepcopy(horarios)
                E0 = energia(horarios_ant)
                ran = randint(0,1)
                if ran == 0:    cambio(horarios, 5)
                elif ran == 1:  cambio_2(horarios, 1)
                E1 = energia(horarios)
                DeltaE = E1 - E0
                if DeltaE < 0:  pass
                else:
                        rand = randint(0,1000)
                        if rand>850 and ran==0: pass
                        else:   horarios = deepcopy(horarios_ant)


def llenar_profes_con_prioridad(carga,horarios):
        prioridad = []
        for profe in horas_disp:        prioridad.append((profe, horas_disp[profe]))
        prioridad = sorted(prioridad, key=lambda horas_d: horas_d[1])

        for profe in prioridad:
                for dia in semana:
                        for hora in range(nbloques):
                                for curso in cursos:
                                        if profe[0] in profdecurso[curso] and carga[profe[0]][curso] > 0 and horarios[curso][dia][hora] == "0" and disponible[profe[0]][dia][hora] and profe[0] not in prof_dh(carga[profe[0]], dia, hora, horarios):
                                                horarios[curso][dia][hora] = profe[0]
                                                carga[profe[0]][curso] -= 1
                                        else:   pass


def llenar(carga, horarios):
        conttest=0
        horarios_copy = deepcopy(horarios)
        while horas_total(carga) > 0:
                shuffle_vacios(horarios, 1)
                llenarvacio(horarios, 1)
                conttest += 1
                if conttest == 1000:
                        for profe in carga:
                                for curso in carga[profe]:
                                        if carga[profe][curso] > 0:
                                                cambio(horarios, 20)
                                                conttest = 0
