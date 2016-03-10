from leer_carga import *
import leer_carga

n_desorden_inicial = 10
minima_energia = -100

####################################################################################
#   INICIAMOS EL HORARIO LLENO DE ESPACIOS VACIOS "0"                              #
####################################################################################

horarios = {}
for curso in cursos:
        if curso not in horarios:	horarios[curso]={}
        for dia in semana:
		if dia not in horarios[curso]:	horarios[curso][dia]=[]
                for i in range(nbloques):	horarios[curso][dia].append("0")

####################################################################################
# Definimos una energia de acuerdo a las preferencias de orden.			####
####################################################################################

def energia(horarios):
	cont = 0
	for curso in horarios:
		for dia in horarios[curso]:
			for hora in range(nbloques):
				if hora%2==0:
					profe = horarios[curso][dia][hora]
					if profe == horarios[curso][dia][hora+1]:	cont -= 1
	return cont

######################################################################################

print "\n- Agregando condiciones fijas."
asignar_fijos(fijos, carga, horarios)

print "\n- Priorisando de acuerdo a disponibilidad."
llenar_profes_con_prioridad(carga,horarios)

print "\n- Evaluando condiciones luego de un llenado inicial incompleto."
prueba_de_consistencia(carga,horarios,nbloques)

print "\n- Buscando Horario Semilla."
llenar(carga, horarios)

print "\n- Verificando asignacion de carga horaria."
prueba_de_consistencia(carga,horarios,nbloques)

print "\n- Minimizando Horario."
print "- Desordenando horarios antes de iniciar."
print "Energia antes de realizar", n_desorden_inicial, " cambios:",	energia(horarios)
cambio(horarios, n_desorden_inicial)

print "Energia inicial:   ",   energia(horarios)
print "- Verificando Carga Horaria restante"
print "- Buscando Minimo."
minimizar(horarios, energia, minima_energia)

print "Energia Final:	", energia(horarios)
prueba_de_consistencia(carga,horarios,nbloques)

#mostrar_horario(horarios)
