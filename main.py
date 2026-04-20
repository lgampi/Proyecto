# ================================================================
# SISTEMA DE SEGURIDAD Y ACCESO PARA CASA INTELIGENTE
# ================================================================
# Proyecto que simula un sistema de seguridad completo para una
# casa inteligente, con diferentes dispositivos, escenas y eventos.
# ================================================================

import json
import os
from datetime import datetime
from random import randint, choice
from typing import List, Dict, Any, Optional

# ================================================================
# CONSTANTES DEL SISTEMA
# ================================================================

# Archivo para persistencia de datos
ARCHIVO_CONFIG = "config_sistema.json"
ARCHIVO_EVENTOS = "eventos_sistema.json"

# Tipos de dispositivos
TIPO_CERRADURA = "Cerradura Inteligente"
TIPO_CAMARA = "Cámara IP"
TIPO_SENSOR_PUERTA = "Sensor Puerta/Ventana"
TIPO_DETECTOR_HUMO = "Detector de Humo"
TIPO_DETECTOR_CO = "Detector de Monóxido de Carbono"
TIPO_ALARMA = "Alarma Inteligente"

# Estados de dispositivos
ESTADO_ACTIVO = "Activo"
ESTADO_INACTIVO = "Inactivo"
ESTADO_ABIERTO = "Abierto"
ESTADO_CERRADO = "Cerrado"
ESTADO_BLOQUEADO = "Bloqueado"
ESTADO_DESBLOQUEADO = "Desbloqueado"
ESTADO_ALERTA = "Alerta"

# Mensajes de sistema
SEPARADOR = "=" * 60


# ================================================================
# CLASES PARA MODELAR LOS DISPOSITIVOS
# ================================================================

class DispositivoSeguridad:
    """Clase base para todos los dispositivos de seguridad."""
    
    def __init__(self, nombre: str, tipo: str, habitacion: str):
        """
        Inicializa un dispositivo de seguridad.
        
        Args:
            nombre: Nombre identificador del dispositivo
            tipo: Tipo de dispositivo
            habitacion: Habitación donde está ubicado
        """
        self.nombre = nombre
        self.tipo = tipo
        self.habitacion = habitacion
        self.estado = ESTADO_INACTIVO
        self.bateria = 100  # Nivel de batería en porcentaje
        self.ultima_actividad = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def cambiar_estado(self, nuevo_estado: str) -> bool:
        """Cambia el estado del dispositivo."""
        self.estado = nuevo_estado
        self.ultima_actividad = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return True
    
    def obtener_informacion(self) -> Dict[str, Any]:
        """Retorna la información del dispositivo."""
        return {
            "nombre": self.nombre,
            "tipo": self.tipo,
            "habitacion": self.habitacion,
            "estado": self.estado,
            "bateria": self.bateria,
            "ultima_actividad": self.ultima_actividad
        }


class CerraduraInteligente(DispositivoSeguridad):
    """Modelar una cerradura inteligente."""
    
    def __init__(self, nombre: str, habitacion: str):
        super().__init__(nombre, TIPO_CERRADURA, habitacion)
        self.estado = ESTADO_BLOQUEADO
        self.intentos_fallidos = 0
    
    def bloquear(self) -> str:
        """Bloquea la cerradura."""
        self.cambiar_estado(ESTADO_BLOQUEADO)
        return f"[OK] {self.nombre} ha sido bloqueada."
    
    def desbloquear(self) -> str:
        """Desbloquea la cerradura."""
        self.cambiar_estado(ESTADO_DESBLOQUEADO)
        self.intentos_fallidos = 0
        return f"[OK] {self.nombre} ha sido desbloqueada."


class CamaraIP(DispositivoSeguridad):
    """Modelar una cámara IP con detección de movimiento."""
    
    def __init__(self, nombre: str, habitacion: str):
        super().__init__(nombre, TIPO_CAMARA, habitacion)
        self.estado = ESTADO_INACTIVO
        self.movimiento_detectado = False
        self.resolucion = "1080p"
    
    def activar(self) -> str:
        """Activa la cámara."""
        self.cambiar_estado(ESTADO_ACTIVO)
        return f"[OK] {self.nombre} ha sido activada."
    
    def desactivar(self) -> str:
        """Desactiva la cámara."""
        self.cambiar_estado(ESTADO_INACTIVO)
        self.movimiento_detectado = False
        return f"[OK] {self.nombre} ha sido desactivada."
    
    def simular_deteccion_movimiento(self) -> Optional[str]:
        """Simula detección de movimiento de forma aleatoria."""
        if self.estado == ESTADO_ACTIVO:
            probabilidad = randint(1, 100)
            if probabilidad > 70:  # 30% de probabilidad
                self.movimiento_detectado = True
                return f"[WARNING] MOVIMIENTO DETECTADO en {self.nombre}"
        return None


class SensorPuertaVentana(DispositivoSeguridad):
    """Modelar sensores de puertas y ventanas."""
    
    def __init__(self, nombre: str, habitacion: str):
        super().__init__(nombre, TIPO_SENSOR_PUERTA, habitacion)
        self.estado = ESTADO_CERRADO
    
    def abrir(self) -> str:
        """Simula apertura de puerta/ventana."""
        self.cambiar_estado(ESTADO_ABIERTO)
        return f"[WARNING] {self.nombre} está ABIERTA."
    
    def cerrar(self) -> str:
        """Simula cierre de puerta/ventana."""
        self.cambiar_estado(ESTADO_CERRADO)
        return f"[OK] {self.nombre} está CERRADA."


class DetectorHumo(DispositivoSeguridad):
    """Modelar detector de humo."""
    
    def __init__(self, nombre: str, habitacion: str):
        super().__init__(nombre, TIPO_DETECTOR_HUMO, habitacion)
        self.estado = ESTADO_INACTIVO
    
    def simular_deteccion_humo(self) -> Optional[str]:
        """Simula detección de humo de forma aleatoria."""
        probabilidad = randint(1, 100)
        if probabilidad > 97:  # 3% de probabilidad
            self.cambiar_estado(ESTADO_ALERTA)
            return f"[ALERT] ALERTA: Humo detectado en {self.nombre}"
        return None
    
    def resetear(self) -> str:
        """Resetea el detector después de una alerta."""
        self.cambiar_estado(ESTADO_INACTIVO)
        return f"[OK] {self.nombre} ha sido reseteado."


class DetectorMonoxidoCarbono(DispositivoSeguridad):
    """Modelar detector de monóxido de carbono."""
    
    def __init__(self, nombre: str, habitacion: str):
        super().__init__(nombre, TIPO_DETECTOR_CO, habitacion)
        self.estado = ESTADO_INACTIVO
    
    def simular_deteccion_co(self) -> Optional[str]:
        """Simula detección de CO de forma aleatoria."""
        probabilidad = randint(1, 100)
        if probabilidad > 98:  # 2% de probabilidad
            self.cambiar_estado(ESTADO_ALERTA)
            return f"[ALERT] ALERTA: Monóxido de Carbono detectado en {self.nombre}"
        return None
    
    def resetear(self) -> str:
        """Resetea el detector después de una alerta."""
        self.cambiar_estado(ESTADO_INACTIVO)
        return f"[OK] {self.nombre} ha sido reseteado."


class AlarmaInteligente(DispositivoSeguridad):
    """Modelar alarma y sirena inteligente."""
    
    def __init__(self, nombre: str, habitacion: str):
        super().__init__(nombre, TIPO_ALARMA, habitacion)
        self.estado = ESTADO_INACTIVO
        self.volumen = 50
    
    def activar(self) -> str:
        """Activa la alarma."""
        self.cambiar_estado(ESTADO_ACTIVO)
        return f"[ALARM] ¡¡ {self.nombre} ACTIVADA !! - Volumen: {self.volumen}%"
    
    def desactivar(self) -> str:
        """Desactiva la alarma."""
        self.cambiar_estado(ESTADO_INACTIVO)
        return f"[OK] {self.nombre} ha sido desactivada."
    
    def establecer_volumen(self, volumen: int) -> str:
        """Establece el nivel de volumen."""
        if 0 <= volumen <= 100:
            self.volumen = volumen
            return f"[OK] Volumen ajustado a {volumen}%"
        return "[ERROR] Volumen inválido. Debe estar entre 0 y 100."


# ================================================================
# CLASE PARA GESTIONAR HABITACIONES
# ================================================================

class Habitacion:
    """Gestiona una habitación y sus dispositivos."""
    
    def __init__(self, nombre: str, piso: int = 1):
        """
        Inicializa una habitación.
        
        Args:
            nombre: Nombre de la habitación
            piso: Número de piso
        """
        self.nombre = nombre
        self.piso = piso
        self.dispositivos: List[DispositivoSeguridad] = []
    
    def agregar_dispositivo(self, dispositivo: DispositivoSeguridad) -> bool:
        """Agrega un dispositivo a la habitación."""
        if dispositivo not in self.dispositivos:
            self.dispositivos.append(dispositivo)
            return True
        return False
    
    def eliminar_dispositivo(self, nombre_dispositivo: str) -> bool:
        """Elimina un dispositivo por su nombre."""
        for i, dispositivo in enumerate(self.dispositivos):
            if dispositivo.nombre == nombre_dispositivo:
                self.dispositivos.pop(i)
                return True
        return False
    
    def obtener_dispositivo(self, nombre: str) -> Optional[DispositivoSeguridad]:
        """Obtiene un dispositivo por su nombre."""
        for dispositivo in self.dispositivos:
            if dispositivo.nombre == nombre:
                return dispositivo
        return None
    
    def listar_dispositivos(self) -> str:
        """Retorna un string con los dispositivos de la habitación."""
        if not self.dispositivos:
            return f"  No hay dispositivos en {self.nombre}."
        
        info = f"\n  [ROOM] Habitación: {self.nombre} (Piso {self.piso})\n"
        for dispositivo in self.dispositivos:
            info_disp = dispositivo.obtener_informacion()
            info += f"    • {info_disp['nombre']} ({info_disp['tipo']})\n"
            info += f"      Estado: {info_disp['estado']} | Batería: {info_disp['bateria']}%\n"
        return info


# ================================================================
# CLASE PRINCIPAL DEL SISTEMA DE SEGURIDAD
# ================================================================

class SistemaSeguridad:
    """Gestiona todo el sistema de seguridad de la casa inteligente."""
    
    def __init__(self):
        """Inicializa el sistema de seguridad."""
        self.habitaciones: List[Habitacion] = []
        self.eventos: List[Dict[str, Any]] = []
        self.escenas_predefinidas = self._crear_escenas()
    
    def _crear_escenas(self) -> Dict[str, List[tuple]]:
        """Define las escenas predefinidas del sistema."""
        return {
            "seguridad_noche": [
                ("cerraduras", "bloquear"),
                ("camaras", "activar"),
                ("alarma", "activar")
            ],
            "seguridad_dia": [
                ("cerraduras", "desbloquear"),
                ("camaras", "desactivar"),
                ("alarma", "desactivar")
            ],
            "ausencia_prolongada": [
                ("cerraduras", "bloquear"),
                ("camaras", "activar"),
                ("alarma", "activar"),
                ("luces", "desactivar")
            ]
        }
    
    def crear_habitacion(self, nombre: str, piso: int = 1) -> str:
        """Crea una nueva habitación."""
        # Validar que no exista una habitación con el mismo nombre
        if any(h.nombre.lower() == nombre.lower() for h in self.habitaciones):
            return "[ERROR] La habitación ya existe."
        
        habitacion = Habitacion(nombre, piso)
        self.habitaciones.append(habitacion)
        self._registrar_evento(f"Habitación '{nombre}' creada")
        return f"[OK] Habitación '{nombre}' creada exitosamente."
    
    def eliminar_habitacion(self, nombre: str) -> str:
        """Elimina una habitación y todos sus dispositivos."""
        for i, habitacion in enumerate(self.habitaciones):
            if habitacion.nombre.lower() == nombre.lower():
                self.habitaciones.pop(i)
                self._registrar_evento(f"Habitación '{nombre}' eliminada")
                return f"[OK] Habitación '{nombre}' eliminada."
        return "[ERROR] Habitación no encontrada."
    
    def obtener_habitacion(self, nombre: str) -> Optional[Habitacion]:
        """Obtiene una habitación por su nombre."""
        for habitacion in self.habitaciones:
            if habitacion.nombre.lower() == nombre.lower():
                return habitacion
        return None
    
    def listar_habitaciones(self) -> str:
        """Retorna un string con todas las habitaciones."""
        if not self.habitaciones:
            return "No hay habitaciones creadas aún."
        
        info = f"\n{SEPARADOR}\n[LIST] HABITACIONES DEL SISTEMA:\n{SEPARADOR}\n"
        for habitacion in self.habitaciones:
            info += f"• {habitacion.nombre} (Piso {habitacion.piso}) - {len(habitacion.dispositivos)} dispositivo(s)\n"
        return info
    
    def agregar_dispositivo(self, habitacion_nombre: str, dispositivo: DispositivoSeguridad) -> str:
        """Agrega un dispositivo a una habitación."""
        habitacion = self.obtener_habitacion(habitacion_nombre)
        if not habitacion:
            return "[ERROR] Habitación no encontrada."
        
        if habitacion.agregar_dispositivo(dispositivo):
            self._registrar_evento(f"Dispositivo '{dispositivo.nombre}' agregado a '{habitacion_nombre}'")
            return f"[OK] Dispositivo '{dispositivo.nombre}' agregado a '{habitacion_nombre}'."
        return "[ERROR] El dispositivo ya existe en esta habitación."
    
    def eliminar_dispositivo(self, habitacion_nombre: str, dispositivo_nombre: str) -> str:
        """Elimina un dispositivo de una habitación."""
        habitacion = self.obtener_habitacion(habitacion_nombre)
        if not habitacion:
            return "[ERROR] Habitación no encontrada."
        
        if habitacion.eliminar_dispositivo(dispositivo_nombre):
            self._registrar_evento(f"Dispositivo '{dispositivo_nombre}' eliminado de '{habitacion_nombre}'")
            return f"[OK] Dispositivo '{dispositivo_nombre}' eliminado."
        return "[ERROR] Dispositivo no encontrado."
    
    def cambiar_estado_dispositivo(self, habitacion_nombre: str, 
                                   dispositivo_nombre: str, accion: str) -> str:
        """Cambia el estado de un dispositivo específico."""
        habitacion = self.obtener_habitacion(habitacion_nombre)
        if not habitacion:
            return "[ERROR] Habitación no encontrada."
        
        dispositivo = habitacion.obtener_dispositivo(dispositivo_nombre)
        if not dispositivo:
            return "[ERROR] Dispositivo no encontrado."
        
        # Ejecutar la acción según el tipo de dispositivo
        resultado = ""
        
        if isinstance(dispositivo, CerraduraInteligente):
            if accion.lower() == "bloquear":
                resultado = dispositivo.bloquear()
            elif accion.lower() == "desbloquear":
                resultado = dispositivo.desbloquear()
            else:
                return "[ERROR] Acción no válida para cerradura. Use 'bloquear' o 'desbloquear'."
        
        elif isinstance(dispositivo, CamaraIP):
            if accion.lower() == "activar":
                resultado = dispositivo.activar()
            elif accion.lower() == "desactivar":
                resultado = dispositivo.desactivar()
            else:
                return "[ERROR] Acción no válida para cámara. Use 'activar' o 'desactivar'."
        
        elif isinstance(dispositivo, SensorPuertaVentana):
            if accion.lower() == "abrir":
                resultado = dispositivo.abrir()
            elif accion.lower() == "cerrar":
                resultado = dispositivo.cerrar()
            else:
                return "[ERROR] Acción no válida para sensor. Use 'abrir' o 'cerrar'."
        
        elif isinstance(dispositivo, AlarmaInteligente):
            if accion.lower() == "activar":
                resultado = dispositivo.activar()
            elif accion.lower() == "desactivar":
                resultado = dispositivo.desactivar()
            else:
                return "[ERROR] Acción no válida para alarma. Use 'activar' o 'desactivar'."
        
        else:
            return "[ERROR] Operación no soportada para este dispositivo."
        
        self._registrar_evento(f"Acción '{accion}' en '{dispositivo_nombre}'")
        return resultado
    
    def ejecutar_escena(self, nombre_escena: str) -> str:
        """Ejecuta una escena predefinida."""
        if nombre_escena not in self.escenas_predefinidas:
            escenas_disponibles = ", ".join(self.escenas_predefinidas.keys())
            return f"[ERROR] Escena no encontrada. Escenas disponibles: {escenas_disponibles}"
        
        info = f"\n[SCENE] Ejecutando escena: {nombre_escena}\n"
        
        for tipo_dispositivo, accion in self.escenas_predefinidas[nombre_escena]:
            info += self._ejecutar_accion_en_tipo(tipo_dispositivo, accion)
        
        self._registrar_evento(f"Escena '{nombre_escena}' ejecutada")
        return info
    
    def _ejecutar_accion_en_tipo(self, tipo: str, accion: str) -> str:
        """Ejecuta una acción en todos los dispositivos de un tipo."""
        resultado = ""
        
        for habitacion in self.habitaciones:
            for dispositivo in habitacion.dispositivos:
                if tipo == "cerraduras" and isinstance(dispositivo, CerraduraInteligente):
                    if accion == "bloquear":
                        resultado += f"  • {dispositivo.bloquear()}\n"
                    elif accion == "desbloquear":
                        resultado += f"  • {dispositivo.desbloquear()}\n"
                
                elif tipo == "camaras" and isinstance(dispositivo, CamaraIP):
                    if accion == "activar":
                        resultado += f"  • {dispositivo.activar()}\n"
                    elif accion == "desactivar":
                        resultado += f"  • {dispositivo.desactivar()}\n"
                
                elif tipo == "alarma" and isinstance(dispositivo, AlarmaInteligente):
                    if accion == "activar":
                        resultado += f"  • {dispositivo.activar()}\n"
                    elif accion == "desactivar":
                        resultado += f"  • {dispositivo.desactivar()}\n"
        
        return resultado if resultado else f"  (No hay dispositivos del tipo '{tipo}')\n"
    
    def simular_eventos_sensores(self) -> List[str]:
        """Simula eventos de los sensores de forma aleatoria."""
        eventos_detectados = []
        
        for habitacion in self.habitaciones:
            for dispositivo in habitacion.dispositivos:
                evento = None
                
                if isinstance(dispositivo, CamaraIP):
                    evento = dispositivo.simular_deteccion_movimiento()
                elif isinstance(dispositivo, DetectorHumo):
                    evento = dispositivo.simular_deteccion_humo()
                elif isinstance(dispositivo, DetectorMonoxidoCarbono):
                    evento = dispositivo.simular_deteccion_co()
                
                if evento:
                    eventos_detectados.append(evento)
                    self._registrar_evento(evento)
        
        return eventos_detectados
    
    def _registrar_evento(self, descripcion: str) -> None:
        """Registra un evento en la bitácora del sistema."""
        evento = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "descripcion": descripcion
        }
        self.eventos.append(evento)
    
    def obtener_bitacora(self, cantidad: int = 20) -> str:
        """Retorna los últimos eventos registrados."""
        if not self.eventos:
            return "No hay eventos registrados aún."
        
        eventos_mostrados = self.eventos[-cantidad:]
        info = f"\n{SEPARADOR}\n[LOG] BITÁCORA DE EVENTOS (últimos {len(eventos_mostrados)}):\n{SEPARADOR}\n"
        
        for evento in eventos_mostrados:
            info += f"[{evento['timestamp']}] {evento['descripcion']}\n"
        
        return info
    
    def obtener_estado_general(self) -> str:
        """Obtiene el estado general del sistema."""
        info = f"\n{SEPARADOR}\n[HOME] ESTADO GENERAL DEL SISTEMA\n{SEPARADOR}\n"
        info += f"Habitaciones: {len(self.habitaciones)}\n"
        
        total_dispositivos = sum(len(h.dispositivos) for h in self.habitaciones)
        info += f"Dispositivos totales: {total_dispositivos}\n"
        
        # Contar dispositivos activos e inactivos
        activos = 0
        inactivos = 0
        alertas = 0
        
        for habitacion in self.habitaciones:
            for dispositivo in habitacion.dispositivos:
                if dispositivo.estado == ESTADO_ACTIVO:
                    activos += 1
                elif dispositivo.estado == ESTADO_ALERTA:
                    alertas += 1
                else:
                    inactivos += 1
        
        info += f"  [+] Activos: {activos}\n"
        info += f"  [-] Inactivos: {inactivos}\n"
        info += f"  [!] Alertas: {alertas}\n"
        info += f"Eventos registrados: {len(self.eventos)}\n"
        
        return info
    
    def guardar_estado(self) -> str:
        """Guarda el estado del sistema en un archivo JSON."""
        try:
            datos = {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "habitaciones": [],
                "eventos": self.eventos
            }
            
            # Guardar información de habitaciones y dispositivos
            for habitacion in self.habitaciones:
                hab_data = {
                    "nombre": habitacion.nombre,
                    "piso": habitacion.piso,
                    "dispositivos": []
                }
                
                for dispositivo in habitacion.dispositivos:
                    hab_data["dispositivos"].append(dispositivo.obtener_informacion())
                
                datos["habitaciones"].append(hab_data)
            
            with open(ARCHIVO_CONFIG, 'w', encoding='utf-8') as f:
                json.dump(datos, f, indent=4, ensure_ascii=False)
            
            return f"[OK] Estado guardado en '{ARCHIVO_CONFIG}'."
        except Exception as e:
            return f"[ERROR] Error al guardar: {str(e)}"
    
    def cargar_estado(self) -> str:
        """Carga el estado del sistema desde un archivo JSON."""
        if not os.path.exists(ARCHIVO_CONFIG):
            return "[ERROR] No se encontró archivo de configuración previo."
        
        try:
            with open(ARCHIVO_CONFIG, 'r', encoding='utf-8') as f:
                datos = json.load(f)
            
            # Limpiar estado actual
            self.habitaciones.clear()
            self.eventos = datos.get("eventos", [])
            
            # Reconstruir habitaciones y dispositivos
            for hab_data in datos.get("habitaciones", []):
                self.crear_habitacion(hab_data["nombre"], hab_data["piso"])
            
            return f"[OK] Estado cargado desde '{ARCHIVO_CONFIG}'."
        except Exception as e:
            return f"[ERROR] Error al cargar: {str(e)}"


# ================================================================
# FUNCIONES DEL MENÚ INTERACTIVO
# ================================================================

def mostrar_menu_principal() -> None:
    """Muestra el menú principal del sistema."""
    print(f"\n{SEPARADOR}")
    print("[SECURITY SYSTEM] SISTEMA DE SEGURIDAD - CASA INTELIGENTE")
    print(f"{SEPARADOR}")
    print("\n1. Gestionar habitaciones y dispositivos")
    print("2. Cambiar estado de dispositivos")
    print("3. Ejecutar escenas predefinidas")
    print("4. Simular eventos de sensores")
    print("5. Ver reportes y bitácora")
    print("6. Ver estado general del sistema")
    print("7. Guardar estado del sistema")
    print("8. Cargar estado del sistema")
    print("9. Salir")
    print(f"{SEPARADOR}\n")


def menu_gestionar_habitaciones(sistema: SistemaSeguridad) -> None:
    """Menú para gestionar habitaciones y dispositivos."""
    while True:
        print(f"\n{SEPARADOR}")
        print("[MANAGEMENT] GESTIÓN DE HABITACIONES Y DISPOSITIVOS")
        print(f"{SEPARADOR}")
        print("1. Crear habitación")
        print("2. Listar habitaciones")
        print("3. Eliminar habitación")
        print("4. Agregar dispositivo a habitación")
        print("5. Eliminar dispositivo de habitación")
        print("6. Ver dispositivos de una habitación")
        print("7. Volver al menú principal")
        print(f"{SEPARADOR}\n")
        
        opcion = input("Seleccione una opción (1-7): ").strip()
        
        if opcion == "1":
            nombre = input("Nombre de la habitación: ").strip()
            if nombre:
                piso = input("Número de piso (default=1): ").strip()
                piso = int(piso) if piso.isdigit() else 1
                print(sistema.crear_habitacion(nombre, piso))
            else:
                print("[ERROR] El nombre no puede estar vacío.")
        
        elif opcion == "2":
            print(sistema.listar_habitaciones())
        
        elif opcion == "3":
            nombre = input("Nombre de la habitación a eliminar: ").strip()
            if nombre:
                confirmacion = input("¿Está seguro? (s/n): ").strip().lower()
                if confirmacion == 's':
                    print(sistema.eliminar_habitacion(nombre))
                else:
                    print("[INFO] Operación cancelada.")
            
            if sistema.obtener_habitacion(habitacion):
                print("\nTipos de dispositivos disponibles:")
                print("1. Cerradura Inteligente")
                print("2. Cámara IP")
                print("3. Sensor Puerta/Ventana")
                print("4. Detector de Humo")
                print("5. Detector de Monóxido de Carbono")
                print("6. Alarma Inteligente")
                
                tipo = input("\nSeleccione tipo de dispositivo (1-6): ").strip()
                nombre_disp = input("Nombre del dispositivo: ").strip()
                
                if nombre_disp:
                    dispositivo = None
                    
                    if tipo == "1":
                        dispositivo = CerraduraInteligente(nombre_disp, habitacion)
                    elif tipo == "2":
                        dispositivo = CamaraIP(nombre_disp, habitacion)
                    elif tipo == "3":
                        dispositivo = SensorPuertaVentana(nombre_disp, habitacion)
                    elif tipo == "4":
                        dispositivo = DetectorHumo(nombre_disp, habitacion)
                    elif tipo == "5":
                        dispositivo = DetectorMonoxidoCarbono(nombre_disp, habitacion)
                    elif tipo == "6":
                        dispositivo = AlarmaInteligente(nombre_disp, habitacion)
                    else:
                        print("[ERROR] Tipo de dispositivo inválido.")
                    
                    if dispositivo:
                        print(sistema.agregar_dispositivo(habitacion, dispositivo))
                else:
                    print("[ERROR] El nombre no puede estar vacío.")
            else:
                print("[ERROR] Habitación no encontrada.")
        
        elif opcion == "5":
            habitacion = input("Nombre de la habitación: ").strip()
            if sistema.obtener_habitacion(habitacion):
                hab = sistema.obtener_habitacion(habitacion)
                print(hab.listar_dispositivos())
                nombre_disp = input("Nombre del dispositivo a eliminar: ").strip()
                if nombre_disp:
                    print(sistema.eliminar_dispositivo(habitacion, nombre_disp))
            else:
                print("[ERROR] Habitación no encontrada.")
        
        elif opcion == "6":
            habitacion = input("Nombre de la habitación: ").strip()
            hab = sistema.obtener_habitacion(habitacion)
            if hab:
                print(hab.listar_dispositivos())
            else:
                print("[ERROR] Habitación no encontrada.")
        
        elif opcion == "7":
            break
        
        else:
            print("[ERROR] Opción inválida.")


def menu_cambiar_estado(sistema: SistemaSeguridad) -> None:
    """Menú para cambiar el estado de dispositivos."""
    print(sistema.listar_habitaciones())
    habitacion = input("Nombre de la habitación: ").strip()
    
    hab = sistema.obtener_habitacion(habitacion)
    if not hab:
        print("[ERROR] Habitación no encontrada.")
        return
    
    print(hab.listar_dispositivos())
    dispositivo = input("Nombre del dispositivo: ").strip()
    
    disp = hab.obtener_dispositivo(dispositivo)
    if not disp:
        print("[ERROR] Dispositivo no encontrado.")
        return
    
    print(f"\nDispositivo: {dispositivo} ({disp.tipo})")
    print("Estado actual: " + disp.estado)
    
    # Sugerir acciones según el tipo de dispositivo
    if isinstance(disp, CerraduraInteligente):
        print("\nAcciones disponibles: bloquear, desbloquear")
    elif isinstance(disp, CamaraIP):
        print("\nAcciones disponibles: activar, desactivar")
    elif isinstance(disp, SensorPuertaVentana):
        print("\nAcciones disponibles: abrir, cerrar")
    elif isinstance(disp, AlarmaInteligente):
        print("\nAcciones disponibles: activar, desactivar")
    
    accion = input("Ingrese la acción a ejecutar: ").strip()
    
    if accion:
        print(sistema.cambiar_estado_dispositivo(habitacion, dispositivo, accion))


def menu_escenas(sistema: SistemaSeguridad) -> None:
    """Menú para ejecutar escenas predefinidas."""
    print(f"\n{SEPARADOR}")
    print("[SCENES] ESCENAS PREDEFINIDAS")
    print(f"{SEPARADOR}")
    
    escenas = sistema.escenas_predefinidas.keys()
    for i, escena in enumerate(escenas, 1):
        print(f"{i}. {escena}")
    print(f"{len(escenas)+1}. Volver")
    
    opcion = input("\nSeleccione una escena: ").strip()
    
    try:
        opcion = int(opcion)
        escenas_list = list(escenas)
        
        if 1 <= opcion <= len(escenas_list):
            escena_seleccionada = escenas_list[opcion - 1]
            print(sistema.ejecutar_escena(escena_seleccionada))
    except ValueError:
        print("[ERROR] Opción inválida.")


def menu_simular_eventos(sistema: SistemaSeguridad) -> None:
    """Menú para simular eventos de sensores."""
    print(f"\n{SEPARADOR}")
    print("[SIMULATION] SIMULACIÓN DE EVENTOS DE SENSORES")
    print(f"{SEPARADOR}\n")
    
    eventos = sistema.simular_eventos_sensores()
    
    if eventos:
        print("Eventos detectados:\n")
        for evento in eventos:
            print(f"  {evento}")
    else:
        print("No se detectaron eventos en esta simulación.")


def menu_reportes(sistema: SistemaSeguridad) -> None:
    """Menú para ver reportes y bitácora."""
    while True:
        print(f"\n{SEPARADOR}")
        print("[REPORTS] REPORTES Y BITÁCORA")
        print(f"{SEPARADOR}")
        print("1. Ver últimos 20 eventos")
        print("2. Ver últimos 50 eventos")
        print("3. Ver todos los eventos")
        print("4. Volver")
        print(f"{SEPARADOR}\n")
        
        opcion = input("Seleccione una opción: ").strip()
        
        if opcion == "1":
            print(sistema.obtener_bitacora(20))
        elif opcion == "2":
            print(sistema.obtener_bitacora(50))
        elif opcion == "3":
            print(sistema.obtener_bitacora(len(sistema.eventos)))
        elif opcion == "4":
            break
        else:
            print("[ERROR] Opción inválida.")


# ================================================================
# FUNCIÓN PRINCIPAL
# ================================================================

def main() -> None:
    """Función principal del programa."""
    
    # Inicializar el sistema
    sistema = SistemaSeguridad()
    
    # Intentar cargar estado previo
    print("\n" + SEPARADOR)
    print("[STARTUP] INICIANDO SISTEMA DE SEGURIDAD...")
    print(SEPARADOR)
    resultado_carga = sistema.cargar_estado()
    print(resultado_carga)
    
    # Menú principal
    while True:
        mostrar_menu_principal()
        opcion = input("Seleccione una opción (1-9): ").strip()
        
        if opcion == "1":
            menu_gestionar_habitaciones(sistema)
        
        elif opcion == "2":
            menu_cambiar_estado(sistema)
        
        elif opcion == "3":
            menu_escenas(sistema)
        
        elif opcion == "4":
            menu_simular_eventos(sistema)
        
        elif opcion == "5":
            menu_reportes(sistema)
        
        elif opcion == "6":
            print(sistema.obtener_estado_general())
        
        elif opcion == "7":
            print(sistema.guardar_estado())
        
        elif opcion == "8":
            print(sistema.cargar_estado())
        
        elif opcion == "9":
            confirmacion = input("\n¿Está seguro de que desea salir? (s/n): ").strip().lower()
            if confirmacion == 's':
                # Guardar antes de salir
                print(sistema.guardar_estado())
                print("\n[OK] ¡Hasta luego! El sistema ha sido guardado correctamente.")
                print(SEPARADOR + "\n")
                break
        
        else:
            print("[ERROR] Opción inválida. Intente de nuevo.")


if __name__ == "__main__":
    main()
