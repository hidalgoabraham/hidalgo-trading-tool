# -*- coding: utf-8 -*-
"""
Created on Mon Dec 20 15:04:00 2021

@author: Abraham Hidalgo
         ahidalgo3@uc.edu.ve
         aj.hidalgo2310@gmail.com

Telecommunications Engineer

Matthew 7:7-8 "... for everyone who seeks finds..."

"""
import datetime




""""
IMPORTANT!

Insert here the GMT (in minutes) according to your location.

This script is intended to run on Windows OS.
In order to allow sync up the system clock to the Binance's Server, 
you need to run this script as Administrator.

"""
# IMPORTANT!
# Insert here the GMT (in minutes) according to your location
shift = datetime.timedelta(minutes = 4*60) # (e.g. GMT Venezuela: +4h = 4*60 minutes)


import win32api


from time import sleep
from time import time
#from PyQt5.QtCore import QObject,pyqtSignal
import traceback
import threading
# import decimal

import numpy as np
import math

from binance.client import Client
# from binance import ThreadedWebsocketManager
from binance import *
# from unicorn_binance_websocket_api.unicorn_binance_websocket_api_manager import BinanceWebSocketApiManager
from unicorn_binance_websocket_api.manager import BinanceWebSocketApiManager
from unicorn_fy.unicorn_fy import UnicornFy

import websocket
import json
import requests
from urllib.parse import urljoin

import talib
import math

import sys, os

import PyQt5

from copy import deepcopy










from ventana_principal_ui import Ui_MainWindow as Ui_VentanaPrincipal
from ventana1_ui import Ui_MainWindow as Ui_Ventana1
from ventana2_ui import Ui_MainWindow as Ui_Ventana2
from ventana3_ui import Ui_MainWindow as Ui_Ventana3
from ventana_rankings_ui import Ui_MainWindow as Ui_VentanaRankings
from ventana_historial_ui import Ui_MainWindow as Ui_VentanaHistorial
from ventana_anuncio_ui import Ui_Dialog as Ui_VentanaAnuncio

class VentanaPrincipal(PyQt5.QtWidgets.QMainWindow, Ui_VentanaPrincipal, PyQt5.QtCore.QObject):
    
    def __init__(self):
        PyQt5.QtWidgets.QMainWindow.__init__(self)
        PyQt5.QtCore.QObject.__init__(self)
        self.setupUi(self)
        
        self.setEnabled(False)
        self.setWindowOpacity(0.0)
        
        self.futuresbot = FuturesBot(self)
        
        sincronizacion_correcta = False
        
        try:
            self.futuresbot.sincronizar()
            sincronizacion_correcta = True
        except:
            traceback.print_exc()
            anuncio = VentanaAnuncio('Error de sincronización con el servidor')
            anuncio.exec()
            self.hide()
        
        # sincronizacion_correcta = True
                          
            
        if sincronizacion_correcta:
                    
            self.ventana1 = Ventana1(self)
            self.ventana1.Accepted.connect(self.ventana1_accepted)
            self.ventana1.show()
            # self.ventana1.pbtn_aceptar_clicked()
            
        else:
            self.setWindowOpacity(1)
            self.salir()
            return
            
            
        
    def closeEvent(self, event):
        self.salir()
        event.accept()
        
    def salir(self): 
        try: self.scanner.detener = True
        except: pass
        
        try: self.scalper.detener = True
        except: pass
    
        try: self.posiciones.detener = True
        except: pass
    
        try: self.ventana_historial.salir()    
        except: pass
    
        try: self.ventana_rankings.salir()    
        except: pass
    
        self.hide()
        
    def pbtn_rankings_clicked(self): self.ventana_rankings.show()
        
    def pbtn_historial_clicked(self): self.ventana_historial.show()
            
    def ventana1_accepted(self): 
        respuesta_api = self.futuresbot.verificar_api()
        
        if respuesta_api == 'correcto': 
           
            try: 
                self.futuresbot.quote = 'USDT'
                self.futuresbot.lista_de_simbolos = self.futuresbot.obtener_lista_de_simbolos(self.futuresbot.quote)
                self.futuresbot.disponible = self.futuresbot.disponible_asset(self.futuresbot.quote)   
                self.futuresbot.disponible_inicio_sesion = self.futuresbot.disponible              
            except:
                pass
                traceback.print_exc()
                anuncio = VentanaAnuncio('No se pudo conectar con la API\no no tiene los permisos necesarios.')
                anuncio.exec()
                self.salir()
                return
                                    
            self.ventana1.salir()
            
            self.ventana2 = Ventana2(self)
            self.ventana2.Accepted.connect(self.ventana2_accepted)
            #self.ventana2.show()
            self.ventana2.pbtn_aceptar_clicked()
            
        else:
            
            if respuesta_api == 'incorrecto': mensaje = 'API Key o API Secret incorrectas'
            elif respuesta_api == 'sin_permiso_trading': mensaje = 'La cuenta no tiene permisos para hacer trading'
            elif respuesta_api == 'trading_bloqueado': mensaje = 'Opción de trading bloqueada'
            elif respuesta_api == 'no_spot_trading': mensaje = 'La cuenta no tiene permisos para operar en Spot'
            elif respuesta_api == 'no_futures_trading': mensaje = 'La cuenta no tiene permisos para operar en Futures'
            elif respuesta_api == 'no_status': mensaje = 'El estado de la cuenta es incorrecto'
            elif respuesta_api == 'Problema de conexión a internet': mensaje = 'Problema de conexión a internet'
            
            anuncio = VentanaAnuncio(mensaje)
            anuncio.exec()
            
            
    def ventana2_accepted(self):
        self.ventana2.salir()           
        self.ventana3 = Ventana3(self)
        self.ventana3.Accepted.connect(self.ventana3_accepted) 
              
        self.ventana3.spnbx_N_monedas.setMaximum(len(self.futuresbot.lista_de_simbolos))
        self.ventana3.spnbx_N_monedas.setValue(len(self.futuresbot.lista_de_simbolos))
        self.ventana3.show()
        #self.ventana3.pbtn_aceptar_clicked()
        
                    
    def ventana3_accepted(self):
        
        self.ventana3.salir() 
        
        self.lbl_disponible.setText('Disponible: ' + str(round(self.futuresbot.disponible,3)) + ' ' + self.futuresbot.quote)
        self.lbl_vela.setText('Vela: ' + self.futuresbot.vela)
        self.lbl_npt.setText('Periodos tendencia: ' + str(self.futuresbot.npt))
        self.lbl_nprsi.setText('Periodos RSI: ' + str(self.futuresbot.nprsi))
        self.lbl_N_monedas.setText('Número de monedas: ' + str(self.futuresbot.numero_de_monedas))
        
        completer = PyQt5.QtWidgets.QCompleter(self.futuresbot.lista_de_simbolos)
        completer.setCaseSensitivity(PyQt5.QtCore.Qt.CaseInsensitive)              
        regex = PyQt5.QtCore.QRegExp("[a-z-A-Z_]+")
        validator = PyQt5.QtGui.QRegExpValidator(regex)
        
        self.linedit_par.setCompleter(completer)
        self.linedit_par.setValidator(validator)
        self.linedit_par.textEdited.connect(self.linedit_par_text_edited)
        self.pbtn_seleccionar_par.clicked.connect(self.pbtn_seleccionar_par_clicked)
        self.pbtn_cambiar_par.clicked.connect(self.pbtn_cambiar_par_clicked)
        self.pbtn_cambiar_par.hide()
        
        self.gpbx_posicion.setEnabled(False)
        self.pbtn_entrar_posicion.hide()
        self.lbl_movimiento_favor.setText('')
        
        self.hsldr_apalancamiento.valueChanged.connect(self.hsldr_apalancamiento_value_changed)
        self.hsldr_apalancamiento.sliderReleased.connect(self.hsldr_apalancamiento_slider_released)
        
        self.spnbx_inversion.valueChanged.connect(self.spnbx_inversion_value_changed)
        
        self.linedit_precio.setValidator(PyQt5.QtGui.QDoubleValidator())
        
        self.pbtn_entrar_posicion.clicked.connect(self.pbtn_entrar_posicion_clicked)
        self.pbtn_salir_posicion.clicked.connect(self.pbtn_salir_posicion_clicked)
        self.pbtn_salir_posicion.hide()
               
        self.scanner = None
        self.scalper = None
        self.posiciones = None
        
        # self.scalper = Scalper(self.futuresbot)
        # self.scalper.newMessageUpdated.connect(self.scalper_new_message_updated)
        # self.scalper.GananciaEnOperacionUpdated.connect(self.scalper_ganancia_en_operacion_updated)
        # self.scalper.JustSell.connect(self.scalper_just_sell)   
        # self.scalper.newMessageToPrompt.connect(self.scalper_new_message_to_prompt)
        # self.scalper.start()
        
        self.pbtn_iniciar_escaneo.show()
        self.pbtn_detener_escaneo.hide()
        self.pbtn_iniciar_escaneo.clicked.connect(self.pbtn_iniciar_escaneo_clicked)
                              
        self.ventana_rankings = VentanaRankings(self)
        self.ventana_rankings.asignar_nombres_rankings()
        self.pbtn_rankings.clicked.connect(self.pbtn_rankings_clicked)
        self.pbtn_rankings.hide()
        
        self.ventana_historial = VentanaHistorial(self)
        self.pbtn_historial.clicked.connect(self.pbtn_historial_clicked)
        self.pbtn_historial.hide()

        self.pbar.hide()
   
        self.setEnabled(True)        
        self.setWindowOpacity(1)
        
    def linedit_par_text_edited(self):
        letter = self.linedit_par.text()
        self.linedit_par.setText(letter.upper())
        
    def spnbx_inversion_value_changed(self):
        inv =  self.futuresbot.disponible * (self.spnbx_inversion.value()/100)
        self.lbl_inversion_en_quote.setText('= ' + str(round(inv,3)) + ' USDT')
        
    def pbtn_seleccionar_par_clicked(self):
        self.linedit_par.setCursorPosition(0)
        
        if not (self.linedit_par.text() in self.futuresbot.lista_de_simbolos): 
            self.linedit_par.setText('')
            self.futuresbot.simbolo = self.linedit_par.text()
            return
        else:
            self.pbtn_seleccionar_par.hide()            
            self.linedit_par.setEnabled(False)
            self.pbtn_cambiar_par.show()
            self.futuresbot.simbolo = self.linedit_par.text()
            
            self.gpbx_posicion.setEnabled(True)
            self.pbtn_entrar_posicion.show()
            self.lbl_movimiento_favor.setText('')
            
            self.spnbx_inversion_value_changed()
            
            exchange_info = self.futuresbot.cliente.futures_exchange_info()
            for symbol_info in exchange_info['symbols']:
                if symbol_info['symbol'] == self.futuresbot.simbolo:
                    self.futuresbot.symbol_info = symbol_info
                    break
 
            self.futuresbot.leverage_brackets = self.futuresbot.cliente.futures_leverage_bracket(symbol = self.futuresbot.simbolo)
            max_leverage = int(self.futuresbot.leverage_brackets[0]['brackets'][0]['initialLeverage'])
            
            self.hsldr_apalancamiento.setMaximum(max_leverage)
            self.hsldr_apalancamiento.setSliderPosition(max_leverage)
            self.futuresbot.cliente.futures_change_leverage(symbol = self.futuresbot.simbolo, leverage = max_leverage)
            
            try: self.futuresbot.cliente.futures_change_margin_type(symbol=self.futuresbot.simbolo, marginType='ISOLATED')
            except: pass
                        
            self.posiciones = Posicion(self)
            
            self.posiciones.Entered.connect(self.posiciones_entered)
            self.posiciones.CameOut.connect(self.posiciones_came_out)
            self.posiciones.CrecimimientoActualizado.connect(self.posiciones_crecimimiento_actualizado)
            
            self.posiciones.start()
            
            
    def pbtn_cambiar_par_clicked(self):
        
        self.posiciones.detener = True
        
        self.pbtn_seleccionar_par.show()
        self.linedit_par.setText('')
        self.futuresbot.simbolo = self.linedit_par.text()
        self.linedit_par.setEnabled(True)
        self.pbtn_cambiar_par.hide()
        
        self.linedit_precio.setText('')
        
        self.cbx_direccion.setEnabled(True)
        self.hsldr_apalancamiento.setEnabled(True)
        self.spnbx_inversion.setEnabled(True)
        self.linedit_precio.setEnabled(True)
        self.spnbx_retroceso.setEnabled(True)
        self.spnbx_activacion.setEnabled(True)
        self.spnbx_stop_loss.setEnabled(True)
        
        self.gpbx_posicion.setEnabled(False)
        self.pbtn_entrar_posicion.show()
        
    def posiciones_entered(self, precio_entrada):
        self.pbtn_cambiar_par.hide()
        self.pbtn_salir_posicion.show()

        self.futuresbot.disponible = self.futuresbot.disponible_asset(self.futuresbot.quote) 
        self.lbl_disponible.setText('Disponible: ' + str(round(self.futuresbot.disponible,3)) + ' ' + self.futuresbot.quote)
    
    def posiciones_came_out(self, precio_salida):
        self.pbtn_entrar_posicion.show()
        self.pbtn_cambiar_par.show()
        self.lbl_movimiento_favor.setText('')
        self.pbtn_salir_posicion.hide()
        self.linedit_precio.setText('')
        
        self.cbx_direccion.setEnabled(True)
        self.hsldr_apalancamiento.setEnabled(True)
        self.spnbx_inversion.setEnabled(True)
        self.linedit_precio.setEnabled(True)
        self.spnbx_retroceso.setEnabled(True)
        self.spnbx_activacion.setEnabled(True)
        self.spnbx_stop_loss.setEnabled(True)
        
        self.futuresbot.disponible = self.futuresbot.disponible_asset(self.futuresbot.quote) 
        self.lbl_disponible.setText('Disponible: ' + str(round(self.futuresbot.disponible,3)) + ' ' + self.futuresbot.quote)
        
        self.futuresbot.ganancia_sesion = 100*(self.futuresbot.disponible - self.futuresbot.disponible_inicio_sesion)/self.futuresbot.disponible_inicio_sesion
        
        self.lbl_ganancia_sesion.setText('Ganancia en esta sesión: ' + str(round(self.futuresbot.ganancia_sesion,2)) + ' %')
        
        self.spnbx_inversion_value_changed()
    
    def posiciones_crecimimiento_actualizado(self, crecimiento):       
        self.lbl_movimiento_favor.setText('Movimiento a favor: ' + str(round(crecimiento,2)) + ' %')
        
    def pbtn_entrar_posicion_clicked(self):
               
        self.cbx_direccion.setEnabled(False)
        self.hsldr_apalancamiento.setEnabled(False)
        self.spnbx_inversion.setEnabled(False)
        self.linedit_precio.setEnabled(False)
        self.spnbx_retroceso.setEnabled(False)
        self.spnbx_activacion.setEnabled(False)
        self.spnbx_stop_loss.setEnabled(False)
        
        self.pbtn_entrar_posicion.hide()
        self.posiciones.entrar = True
                             
    def pbtn_salir_posicion_clicked(self):
        self.posiciones.salir = True
        self.pbtn_salir_posicion.hide()
        
    def hsldr_apalancamiento_value_changed(self, nuevo_valor):
         self.lbl_apalancamiento_2.setText('x' +str(nuevo_valor))
        
    def hsldr_apalancamiento_slider_released(self):
        nuevo_valor = self.hsldr_apalancamiento.sliderPosition()      
        self.futuresbot.cliente.futures_change_leverage(symbol = self.futuresbot.simbolo, leverage = nuevo_valor)
                                       
    def pbtn_iniciar_escaneo_clicked(self):
        self.pbtn_iniciar_escaneo.hide()
        self.pbtn_detener_escaneo.show()
        self.pbtn_rankings.hide()
                
        self.scanner = Scanner(self.futuresbot)
        self.scanner.ProgressUpdate.connect(self.scanner_progress_update)
        self.scanner.ScanningEnded.connect(self.scanner_scanning_ended)
        self.scanner.CriptosTopUpdated.connect(self.ventana_rankings.scanner_criptos_top_actualizadas)
        self.scanner.ConnectionLost.connect(self.scanner_connection_lost)
        self.scanner.start()
        
        self.pbar.show()
        self.lbl_prompt.setText('Descargando datos, por favor espere...')
    
    def pbtn_detener_escaneo_clicked(self):
        self.scanner.detener = True
        self.pbtn_detener_escaneo.hide()
        self.pbtn_iniciar_escaneo.show()
        self.lbl_prompt.setText('')
        
    # def pbtn_comprar_clicked(self):
    #     if self.scalper.simbolo == '': return
        
    #     self.futuresbot.disponible = self.futuresbot.disponible_asset(self.futuresbot.quote)
    #     self.futuresbot.capital_a_invertir = self.futuresbot.disponible
    #     self.futuresbot.saldo_bnb = self.futuresbot.disponible_asset('BNB')
    #     self.futuresbot.precio_bnb = float(self.futuresbot.cliente.get_klines(symbol = 'BNB' + self.futuresbot.quote, interval = self.futuresbot.vela)[-1][4])
        
    #     cap_bnb = self.futuresbot.saldo_bnb*self.futuresbot.precio_bnb
        
    #     if cap_bnb < (0.2/100)*self.futuresbot.capital_a_invertir: 
    #         anuncio = VentanaAnuncio('Saldo BNB insuficiente para operar\nDebe tener al menos 0.2% de la inversión\nOperación de compra rechazada')
    #         anuncio.exec()
    #         return
        
    #     self.scalper.lets_buy = True        
    #     self.scalper.lets_sell = False 
    #     self.pbtn_comprar.hide()
    #     self.pbtn_vender.show()
    #     self.lbl_ganancia_operacion.show()
    #     self.chkbx_venta_automatica.show()
        
    #     self.linedit_comprar.setEnabled(False)
    
    # def pbtn_vender_clicked(self):
    #     self.chkbx_venta_automatica.setChecked(False)
    #     self.scalper.venta_automatica = False
    #     self.chkbx_venta_automatica.hide()
        
    #     self.scalper.lets_buy = False        
    #     self.scalper.lets_sell = True 
    #     self.pbtn_comprar.show()
    #     self.pbtn_vender.hide()
        
    #     self.linedit_comprar.setEnabled(True)
        
    #     self.lbl_ganancia_operacion.setText('Ganancia en esta operación (estimado): 0 %')
    #     self.lbl_ganancia_operacion.hide()
        
    # def pbtn_vender_emergencia_clicked(self):
    #     pass
        
        
    ### From Signals
           
    def scanner_progress_update(self):
        self.pbar.setValue(self.scanner.progreso)
    
    def scanner_scanning_ended(self):
        self.pbar.hide()
        self.pbar.setValue(0)
        self.lbl_prompt.setText('')
        self.pbtn_rankings.show()  
        
        # completer = PyQt5.QtWidgets.QCompleter(self.futuresbot.lista_de_simbolos)
        # completer.setCaseSensitivity(PyQt5.QtCore.Qt.CaseInsensitive)
        # self.linedit_comprar.setCompleter(completer)
        
        # self.pbtn_comprar.show()
        # self.linedit_comprar.show()
        # self.lbl_ganancia_sesion.show()
        
        # self.scalper.scanner = self.scanner
        
        self.pbtn_iniciar_escaneo.hide()
        self.pbtn_detener_escaneo.hide()
    
    def scanner_connection_lost(self):
        pass
        print('\nConnection Lost\n')
        
    # def scalper_new_message_updated(self):
    #     self.ventana_historial.new_message(self.scalper.message_lstw)
        
    # def scalper_ganancia_en_operacion_updated(self):
    #     self.lbl_ganancia_operacion.setText('Crecimiento en esta operación (estimado): ' + str(round(self.scalper.g_op_calc,3)) + ' %')
    
    # def scalper_just_sell(self):
    #     self.lbl_disponible.setText('Disponible: ' + str(round(self.futuresbot.disponible,8)) + ' ' + self.futuresbot.quote)
        
    #     self.futuresbot.saldo_bnb = self.futuresbot.disponible_asset('BNB')
    #     self.futuresbot.precio_bnb = float(self.futuresbot.cliente.get_klines(symbol = 'BNB' + self.futuresbot.quote, interval = self.futuresbot.vela)[-1][4])
    #     self.lbl_saldo_bnb.setText('Saldo BNB: ' + str(round(self.futuresbot.saldo_bnb,8))+'  ->  '+str(round(self.futuresbot.saldo_bnb*self.futuresbot.precio_bnb,3))+' '+self.futuresbot.quote)
        
    #     if self.futuresbot.modo == 'Simulación':
    #         self.lbl_inversion.setText('Inversion: X')
    #     else:
    #         self.lbl_inversion.setText('Inversion: ' + str(round(self.futuresbot.capital_a_invertir,8)) + ' ' + self.futuresbot.quote)
            
    #     self.lbl_ganancia_sesion.setText('Ganancia en esta sesión: ' + str(round(self.futuresbot.ganancia_sesion,3)) + ' %')
                
    #     self.pbtn_vender_clicked()
        
    # def scalper_new_message_to_prompt(self):
    #     self.lbl_prompt.setText(self.scalper.message_to_prompt)
    

class Ventana1(PyQt5.QtWidgets.QMainWindow, Ui_Ventana1, PyQt5.QtCore.QObject):
    
    Accepted = PyQt5.QtCore.pyqtSignal()
    
    def __init__(self, ventana_principal):
        PyQt5.QtWidgets.QMainWindow.__init__(self)
        PyQt5.QtCore.QObject.__init__(self)
        self.setupUi(self)
        
        self.cvp = ventana_principal
        
        
        
        
        #Conexiones
        self.linedit_api_key.editingFinished.connect(self.linedit_api_key_editing_finished)
        self.linedit_api_secret.editingFinished.connect(self.linedit_api_secret_editing_finished)
        self.pbtn_aceptar.clicked.connect(self.pbtn_aceptar_clicked)
        
    
    def closeEvent(self, event):
        self.cvp.salir()
        event.accept()
        
    def salir(self):
        self.hide()
        
    def linedit_api_key_editing_finished(self):
        self.linedit_api_key.setCursorPosition(0)
    
    def linedit_api_secret_editing_finished(self):
        self.linedit_api_secret.setCursorPosition(0)
    
    def pbtn_aceptar_clicked(self):
        self.cvp.futuresbot.api_key = self.linedit_api_key.text()
        self.cvp.futuresbot.api_secret = self.linedit_api_secret.text()
        
        self.Accepted.emit()
        
        
class Ventana2(PyQt5.QtWidgets.QMainWindow, Ui_Ventana2, PyQt5.QtCore.QObject):
    
    Accepted = PyQt5.QtCore.pyqtSignal()
    
    def __init__(self, ventana_principal):
        PyQt5.QtWidgets.QMainWindow.__init__(self)
        PyQt5.QtCore.QObject.__init__(self)
        self.setupUi(self)
        
        self.cvp = ventana_principal
                
        #Conexiones
        self.pbtn_aceptar.clicked.connect(self.pbtn_aceptar_clicked)
        
        self.cbx_modo.setCurrentText('Real')
        
    
    def closeEvent(self, event):
        self.cvp.salir()
        event.accept()
        
    def salir(self):
        self.hide()
            
    def pbtn_aceptar_clicked(self):
        self.cvp.futuresbot.modo = self.cbx_modo.currentText()       
        self.Accepted.emit()
        
        
# class Ventana3(PyQt5.QtWidgets.QMainWindow, Ui_Ventana3, PyQt5.QtCore.QObject):
    
#     Accepted = PyQt5.QtCore.pyqtSignal()
    
#     def __init__(self, ventana_principal):
#         PyQt5.QtWidgets.QMainWindow.__init__(self)
#         PyQt5.QtCore.QObject.__init__(self)
#         self.setupUi(self)
        
#         self.cvp = ventana_principal
        
#         # self.cvp.futuresbot.disponible = self.cvp.futuresbot.disponible_asset(self.cvp.futuresbot.quote)
        
#         # self.lbl_disponible.setText('Disponible: '+str(round(self.cvp.futuresbot.disponible,8))+' ' +self.cvp.futuresbot.quote)
#         self.lbl_disponible.hide()
        
#         # self.cvp.futuresbot.saldo_bnb = self.cvp.futuresbot.disponible_asset('BNB')
#         # self.cvp.futuresbot.precio_bnb = float(self.cvp.futuresbot.cliente.get_klines(symbol = 'BNB' + self.cvp.futuresbot.quote, interval = self.cvp.futuresbot.vela)[-1][4])
        
#         # if self.cvp.futuresbot.modo == 'Simulación': 
#         #     self.spnbx_inversion.hide()
#         #     self.pbtn_max_inversion.hide()  
#         #     self.lbl_inversion.setText('Inversión: X')
            
            
#         # elif self.cvp.futuresbot.modo == 'Real':
#         #     self.spnbx_inversion.setMaximum(self.cvp.futuresbot.disponible)
        
#         self.spnbx_inversion.hide()
#         self.pbtn_max_inversion.hide()  
#         self.lbl_inversion.hide()
            
#         # self.lbl_saldo_bnb.setText('Saldo BNB: ' + str(round(self.cvp.futuresbot.saldo_bnb,8))+'  ->  '+str(round(self.cvp.futuresbot.saldo_bnb*self.cvp.futuresbot.precio_bnb,3))+' '+self.cvp.futuresbot.quote)
#         self.lbl_saldo_bnb.hide()
                        
#         # self.lbl_unidad_inversion.setText(self.cvp.futuresbot.quote)
#         self.lbl_unidad_inversion.hide()
        
#         #Conexiones
#         self.pbtn_aceptar.clicked.connect(self.pbtn_aceptar_clicked)
#         self.pbtn_max_inversion.clicked.connect(self.pbtn_max_inversion_clicked)
        
#         self.pbtn_max_inversion.hide()
#         # self.pbtn_max_inversion_clicked()
#         # self.spnbx_inversion.setEnabled(False)
        
        
#     def closeEvent(self, event):
#         self.cvp.salir()
#         event.accept()
        
#     def salir(self):
#         self.hide()
        
#     def pbtn_max_inversion_clicked(self):
#         self.spnbx_inversion.setValue(self.cvp.futuresbot.disponible)
    
#     def pbtn_aceptar_clicked(self):
        
#         # if self.cvp.futuresbot.modo == 'Simulación':
#         #     if self.cvp.futuresbot.disponible > 0:
#         #         self.cvp.futuresbot.capital_a_invertir = self.cvp.futuresbot.disponible*4
#         #     else:
#         #         self.cvp.futuresbot.capital_a_invertir = 100
            
#         # elif self.cvp.futuresbot.modo == 'Real':
#         #     self.cvp.futuresbot.capital_a_invertir = self.spnbx_inversion.value()
        
#         # self.cvp.futuresbot.capital_a_invertir_inicio_sesion = self.cvp.futuresbot.capital_a_invertir + self.cvp.futuresbot.capital_en_bnb
                
        
#         self.Accepted.emit()
        
        
class Ventana3(PyQt5.QtWidgets.QMainWindow, Ui_Ventana3, PyQt5.QtCore.QObject):
    
    Accepted = PyQt5.QtCore.pyqtSignal()
    
    def __init__(self, ventana_principal):
        PyQt5.QtWidgets.QMainWindow.__init__(self)
        PyQt5.QtCore.QObject.__init__(self)
        self.setupUi(self)
        
        self.cvp = ventana_principal
        
        #Conexiones
        self.pbtn_aceptar.clicked.connect(self.pbtn_aceptar_clicked)
    
    def closeEvent(self, event):
        self.cvp.salir()
        event.accept()
        
    def salir(self):
        self.hide()
            
    def pbtn_aceptar_clicked(self):
        
        self.cvp.futuresbot.vela = self.cbx_vela.currentText()
        
        #Mapeo
        if self.cvp.futuresbot.vela == '1m':
            self.cvp.futuresbot.muestreo = 1
            
        elif self.cvp.futuresbot.vela == '3m':
            self.cvp.futuresbot.muestreo = 3
            
        elif self.cvp.futuresbot.vela == '5m':
            self.cvp.futuresbot.muestreo = 5
            
        elif self.cvp.futuresbot.vela == '15m':
            self.cvp.futuresbot.muestreo = 15
            
        elif self.cvp.futuresbot.vela == '30m':
            self.cvp.futuresbot.muestreo = 30
            
        elif self.cvp.futuresbot.vela == '1h':
            self.cvp.futuresbot.muestreo = 60
            
        elif self.cvp.futuresbot.vela == '2h':
            self.cvp.futuresbot.muestreo = 2*60
            
        elif self.cvp.futuresbot.vela == '4h':
            self.cvp.futuresbot.muestreo = 4*60
            
        elif self.cvp.futuresbot.vela == '6h':
            self.cvp.futuresbot.muestreo = 6*60
            
        elif self.cvp.futuresbot.vela == '8h':
            self.cvp.futuresbot.muestreo = 8*60
            
        elif self.cvp.futuresbot.vela == '12h':
            self.cvp.futuresbot.muestreo = 12*60
            
        elif self.cvp.futuresbot.vela == '1d':
            self.cvp.futuresbot.muestreo = 24*60
            
        elif self.cvp.futuresbot.vela == '3d':
            self.cvp.futuresbot.muestreo = 3*24*60
            
        elif self.cvp.futuresbot.vela == '1w':
            self.cvp.futuresbot.muestreo = 7*24*60
            
        elif self.cvp.futuresbot.vela == '1M':
            self.cvp.futuresbot.muestreo = 30*24*60
               
        self.cvp.futuresbot.nprsi = self.spnbx_nprsi.value()
        self.cvp.futuresbot.npt = self.spnbx_npt.value()
                
        maximo = max(self.cvp.futuresbot.npt, self.cvp.futuresbot.nprsi)
        self.cvp.futuresbot.T = (2*maximo)*self.cvp.futuresbot.muestreo
                
        self.cvp.futuresbot.numero_de_monedas = self.spnbx_N_monedas.value()
                       
        self.Accepted.emit()
        
        

class VentanaRankings(PyQt5.QtWidgets.QMainWindow, Ui_VentanaRankings, PyQt5.QtCore.QObject):
    
    PbtnActualizarClicked = PyQt5.QtCore.pyqtSignal()
    
    def __init__(self, ventana_principal):
        PyQt5.QtWidgets.QMainWindow.__init__(self)
        PyQt5.QtCore.QObject.__init__(self)
        self.setupUi(self)
        
        self.cvp = ventana_principal
        
        self.pbtn_actualizar.clicked.connect(self.pbtn_actualizar_clicked)
           
    def closeEvent(self, event):
        event.accept()
        
    def salir(self):
        self.hide()
        
    def pbtn_actualizar_clicked(self): 
        self.pbtn_actualizar.hide()
        self.PbtnActualizarClicked.emit()
        
    def asignar_nombres_rankings(self):
        self.lbl_criterio1.setText(self.cvp.futuresbot.criterios_rankings[0])
        self.lbl_criterio2.setText(self.cvp.futuresbot.criterios_rankings[1])
        self.lbl_criterio3.setText(self.cvp.futuresbot.criterios_rankings[2])
        self.lbl_criterio4.setText(self.cvp.futuresbot.criterios_rankings[3])
        self.lbl_criterio5.setText(self.cvp.futuresbot.criterios_rankings[4])
        self.lbl_criterio6.setText(self.cvp.futuresbot.criterios_rankings[5])
        
    def reiniciar_rankings(self):
        self.tbw_criterio1.clear()
        self.tbw_criterio1.setHorizontalHeaderLabels(['Simbolo','Puntaje'])
        self.tbw_criterio1.verticalHeader().hide()
        
        self.tbw_criterio2.clear()
        self.tbw_criterio2.setHorizontalHeaderLabels(['Simbolo','Puntaje'])
        self.tbw_criterio2.verticalHeader().hide()
        
        self.tbw_criterio3.clear()
        self.tbw_criterio3.setHorizontalHeaderLabels(['Simbolo','Puntaje'])
        self.tbw_criterio3.verticalHeader().hide()
        
        self.tbw_criterio4.clear()
        self.tbw_criterio4.setHorizontalHeaderLabels(['Simbolo','Puntaje'])
        self.tbw_criterio4.verticalHeader().hide()
        
        self.tbw_criterio5.clear()
        self.tbw_criterio5.setHorizontalHeaderLabels(['Simbolo','Puntaje'])
        self.tbw_criterio5.verticalHeader().hide()
        
        self.tbw_criterio6.clear()
        self.tbw_criterio6.setHorizontalHeaderLabels(['Simbolo','Puntaje'])
        self.tbw_criterio6.verticalHeader().hide()
        
    def scanner_criptos_top_actualizadas(self):
        
        self.reiniciar_rankings()
                
        Ranking = self.cvp.scanner.Rankings[self.cvp.futuresbot.criterios_rankings[0]]
        self.tbw_criterio1.setRowCount(len(Ranking))
        for i in range(len(Ranking)):
            self.tbw_criterio1.setItem(i,0,PyQt5.QtWidgets.QTableWidgetItem(Ranking[i]['simbolo']))
            self.tbw_criterio1.setItem(i,1,PyQt5.QtWidgets.QTableWidgetItem(str(round(Ranking[i]['puntaje'],3))))
        
        Ranking = self.cvp.scanner.Rankings[self.cvp.futuresbot.criterios_rankings[1]]
        self.tbw_criterio2.setRowCount(len(Ranking))
        for i in range(len(Ranking)):
            self.tbw_criterio2.setItem(i,0,PyQt5.QtWidgets.QTableWidgetItem(Ranking[i]['simbolo']))
            self.tbw_criterio2.setItem(i,1,PyQt5.QtWidgets.QTableWidgetItem(str(round(Ranking[i]['puntaje'],3))))
            
        Ranking = self.cvp.scanner.Rankings[self.cvp.futuresbot.criterios_rankings[2]]
        self.tbw_criterio3.setRowCount(len(Ranking))
        for i in range(len(Ranking)):
            self.tbw_criterio3.setItem(i,0,PyQt5.QtWidgets.QTableWidgetItem(Ranking[i]['simbolo']))
            self.tbw_criterio3.setItem(i,1,PyQt5.QtWidgets.QTableWidgetItem(str(round(Ranking[i]['puntaje'],3))))
            
        Ranking = self.cvp.scanner.Rankings[self.cvp.futuresbot.criterios_rankings[3]]
        self.tbw_criterio4.setRowCount(len(Ranking))
        for i in range(len(Ranking)):
            self.tbw_criterio4.setItem(i,0,PyQt5.QtWidgets.QTableWidgetItem(Ranking[i]['simbolo']))
            self.tbw_criterio4.setItem(i,1,PyQt5.QtWidgets.QTableWidgetItem(str(round(Ranking[i]['puntaje'],3))))
            
        Ranking = self.cvp.scanner.Rankings[self.cvp.futuresbot.criterios_rankings[4]]
        self.tbw_criterio5.setRowCount(len(Ranking))
        for i in range(len(Ranking)):
            self.tbw_criterio5.setItem(i,0,PyQt5.QtWidgets.QTableWidgetItem(Ranking[i]['simbolo']))
            self.tbw_criterio5.setItem(i,1,PyQt5.QtWidgets.QTableWidgetItem(str(round(Ranking[i]['puntaje'],3))))
            
        Ranking = self.cvp.scanner.Rankings[self.cvp.futuresbot.criterios_rankings[5]]
        self.tbw_criterio6.setRowCount(len(Ranking))
        for i in range(len(Ranking)):
            self.tbw_criterio6.setItem(i,0,PyQt5.QtWidgets.QTableWidgetItem(Ranking[i]['simbolo']))
            self.tbw_criterio6.setItem(i,1,PyQt5.QtWidgets.QTableWidgetItem(str(round(Ranking[i]['puntaje'],3))))
            
        self.pbtn_actualizar.show()
    
        
class VentanaHistorial(PyQt5.QtWidgets.QMainWindow, Ui_VentanaHistorial):
    
    def __init__(self, ventana_principal):
        PyQt5.QtWidgets.QMainWindow.__init__(self)
        self.setupUi(self)
        
        self.cvp = ventana_principal
        
        self.pbtn_guardar_historial.clicked.connect(self.guardar)
    
    def closeEvent(self, event):
        event.accept()
        
    def salir(self):
        self.hide()
        
    def new_message(self, message):
        self.lstw_historial.addItem(message)
        
    def clear(self):
        self.lstw_historial.clear()
        
    def guardar(self):
        carpeta='.'
        extension = 'txt'
        ruta = PyQt5.QtWidgets.QFileDialog.getSaveFileName(self,'Guardar archivo',carpeta,'*.'+extension)[0]
        if ruta!='':
            if ruta[-(len(extension) +1):] != '.'+extension: ruta=ruta+'.'+extension
                                            
            with open(ruta, "w") as escritor:
                for linea in self.cvp.futuresbot.historial:
                    escritor.write(linea + "\n")
                    
                escritor.write('Ganancia total: '+str(round(self.cvp.futuresbot.ganancia_sesion,3)) + " % \n")


class VentanaAnuncio(PyQt5.QtWidgets.QDialog, Ui_VentanaAnuncio):
    def __init__(self, mensaje):
        PyQt5.QtWidgets.QDialog.__init__(self)
        self.setupUi(self)

        self.setWindowFlags(PyQt5.QtCore.Qt.WindowCloseButtonHint)
        
        self.lbl.setText(mensaje)
        
        #Conexiones
        self.pbtn.clicked.connect(self.pbtn_clicked)
        
    def closeEvent(self, event):
        event.accept()
        
    def salir(self): self.close()
    
    def pbtn_clicked(self): self.close()
    


class Posicion(PyQt5.QtCore.QThread):
    Entered = PyQt5.QtCore.pyqtSignal(float)
    # FailedToEnter
    CameOut = PyQt5.QtCore.pyqtSignal(float)
    CrecimimientoActualizado = PyQt5.QtCore.pyqtSignal(float)
    
    def __init__(self, ventana_principal):
        PyQt5.QtCore.QThread.__init__(self)
        
        self.name = 'Hilo Posicion' # Thread.name
        
        self.cvp = ventana_principal
        
        self.detener = False
        self.entrar = False
        self.salir = False
        
        self.hilo_stream_klines = None
        self.configurar_stream_klines([self.cvp.futuresbot.simbolo], '1m')
        self.precio_actual = None
        
    def configurar_stream_klines(self, list_of_symbols, vela):
        
        if self.hilo_stream_klines is None: pass
        else: self.hilo_stream_klines.detener = True
                
        simbolos = []
        
        for symbol in list_of_symbols: simbolos.append(symbol.lower())
        
        direccion = 'binance.com-futures'
        
        streams = ['kline_'+vela]
                
        self.hilo_stream_klines = HiloStream(direccion, streams, simbolos, 'Hilo Stream Klines Posicion')
        
        #Conexion
        self.hilo_stream_klines.StreamReceived.connect(self.receptor_de_stream_klines)
        
        self.hilo_stream_klines.start()
        
   
    def receptor_de_stream_klines(self):
        
        if hasattr(self, 'hilo_stream_klines'): pass
        else: return
        
        message = self.hilo_stream_klines.last_message
        
        if message is not None: pass
        else: return
        
        if 'stream_type' in message: pass
        else: return
        
        vela = message['kline']
        
        self.precio_actual = float(vela['close_price'])
        
        if not self.precio_entrada is None:
            if self.direccion == 'Long':
                c = 100*(self.precio_actual - self.precio_entrada)/self.precio_entrada                       
                self.CrecimimientoActualizado.emit(c)
                
            elif self.direccion == 'Short':
                c = -100*(self.precio_actual - self.precio_entrada)/self.precio_entrada                       
                self.CrecimimientoActualizado.emit(c)
        
    def tomar_parametros(self):
        self.direccion = self.cvp.cbx_direccion.currentText()
        self.apalancamiento = self.cvp.hsldr_apalancamiento.sliderPosition()
        self.inversion = self.cvp.futuresbot.disponible * (self.cvp.spnbx_inversion.value()/100)
        if self.cvp.linedit_precio.text() == '': self.precio_para_entrar = None
        else: self.precio_para_entrar = float(self.cvp.linedit_precio.text())
        
        self.retroceso = self.cvp.spnbx_retroceso.value()
        self.activacion = self.cvp.spnbx_activacion.value()
        self.stop_loss = self.cvp.spnbx_stop_loss.value()
                
    def place_market_order(self, direction, investment, leverage, in_out, cantidad = None):
        
        if direction == 'Long': lado = 'BUY'       
        elif direction == 'Short': lado = 'SELL'
        
        m = 0.95
        n = 0.90 #para evitar excepciones por costo
        
        
        listo = False
        
        if in_out == 'in':
            while not listo:               
                MaxPos = investment * leverage * m
                Pos = MaxPos*n
                qty = Pos/self.precio_actual
                cantidad = qty_filter(qty, self.cvp.futuresbot.symbol_info)
                
                try:
                    order = self.cvp.futuresbot.cliente.futures_create_order(symbol = self.cvp.futuresbot.simbolo,
                                                                             side = lado,
                                                                             type = 'MARKET',
                                                                             quantity = cantidad)
                    listo = True
                    
                except BinanceAPIException as excptn:
                    if excptn.message == 'Margin is insufficient.': n -= 0.05
                
                
                
        elif in_out == 'out':
            if lado == 'BUY': lado_salida = 'SELL'
            elif lado == 'SELL': lado_salida = 'BUY'
            
            order = self.cvp.futuresbot.cliente.futures_create_order(symbol = self.cvp.futuresbot.simbolo,
                                                                     side = lado_salida,
                                                                     type = 'MARKET',
                                                                     quantity = cantidad,
                                                                     reduceOnly = 'true')
            
        return order, cantidad
            
    
    def run(self):
        
        self.precio_entrada = None
        
        try:
        
            while not self.detener:
                
                while not self.entrar:
                    if self.detener: break
                self.entrar = False
                
                if self.detener: break
            
                self.tomar_parametros()
                
                ### Entrada
            
                if self.precio_para_entrar is None: 
                    
                    orden_entrada, q = self.place_market_order(direction = self.direccion,
                                                               investment = self.inversion,
                                                               leverage = self.apalancamiento,
                                                               in_out = 'in')
                    
                    self.precio_entrada = self.precio_actual
                    self.Entered.emit(self.precio_entrada)
     
                else:
                    
                    if self.direccion == 'Long':
                        while self.precio_actual < self.precio_para_entrar: 
                            if self.detener: break
                    
                    elif self.direccion == 'Short':
                        while self.precio_actual > self.precio_para_entrar:
                            if self.detener: break
                    
                    if self.detener: break
                    
                    orden_entrada, q = self.place_market_order(direction = self.direccion,
                                                               investment = self.inversion,
                                                               leverage = self.apalancamiento,
                                                               in_out = 'in')
                    
                    self.precio_entrada = self.precio_actual
                    self.Entered.emit(self.precio_entrada)
                    
                    
                ### Salida
                                                                
                if self.direccion == 'Long':
                    precio_activacion = self.precio_entrada*(1 + self.activacion/100)
                    precio_stop_loss = self.precio_entrada*(1 - self.stop_loss/100)
                    max_p = -np.Infinity
                    
                    while True:
                        
                        if self.salir: break
                    
                        if self.detener: break
                        
                        if self.precio_actual <= precio_stop_loss: break
                        
                        if self.precio_actual > max_p: max_p = self.precio_actual
                                                                       
                        if max_p >= precio_activacion:

                            avance = max_p - self.precio_entrada
                            retro = max_p - self.precio_actual
                            
                            proporcion = 100*(retro/avance)
                            
                            if proporcion >= self.retroceso: 
                                if self.precio_actual > self.precio_entrada*(1+0.08/100): break #Para no salir en negativo
                            
                
                elif self.direccion == 'Short':
                    precio_activacion = self.precio_entrada*(1 - self.activacion/100)
                    precio_stop_loss = self.precio_entrada*(1 + self.stop_loss/100)
                    min_p = np.Infinity
                    
                    while True:
                        
                        if self.salir: break
                        
                        if self.detener: break
                        
                        if self.precio_actual >= precio_stop_loss: break
                        
                        if self.precio_actual < min_p: min_p = self.precio_actual
                                                
                        if min_p <= precio_activacion:

                            avance = self.precio_entrada - min_p
                            retro =  self.precio_actual - min_p
                            
                            proporcion = 100*(retro/avance)
                            
                            if proporcion >= self.retroceso:
                                if self.precio_actual < self.precio_entrada*(1-0.08/100): break #Para no salir en negativo
                        
                if self.detener: break
                
                orden_salida = self.place_market_order(direction = self.direccion,
                                                       investment = self.inversion,
                                                       leverage = self.apalancamiento,
                                                       in_out = 'out',
                                                       cantidad = q)
                
                precio_salida = self.precio_actual
                self.CameOut.emit(precio_salida)
                
                self.salir = False
                self.precio_entrada = None
                    
        except:
            traceback.print_exc()
            try: self.hilo_stream_klines.detener = True
            except: pass
        
        try: self.hilo_stream_klines.detener = True
        except: pass
    
        
    

class FuturesBot():
    def __init__(self, ventana_principal):
        self.cvp = ventana_principal
        
        self.url_base = 'https://api.binance.com'
        self.api_key = ''
        self.api_secret = ''
        self.cliente = None
        
        self.modo = ''
        self.quote = ''
        self.disponible = None
        
        self.lista_de_simbolos = []
        self.exclude = ['BTCSTUSDT'] #['TUSD', 'BUSD', 'USDC', 'USDT', 'GBP', 'AUD', 'SUSD', 'EUR', 'UST', 'BTCST']
        self.numero_de_monedas = None
        
        self.vela = '1m'
        self.muestreo = 1 #minutos
        self.npt = 30
        self.nprsi = 8
        
        maximo = max(self.npt, self.nprsi)
        self.T = (2*maximo )*self.muestreo
        
        self.callback = 0.1 #%
        self.activation = 0.3 #%
        self.stop_loss = 0.1 #%
        
        self.historial = []
        
        self.comision = 0.04 #% a pagar en comisiones por entrar a una posicion (Taker)
        
        self.disponible_inicio_sesion = None

        self.perdida_max = 7 #% del capital a invertir que estamos dispuestos a perder antes de detener al bot.
        self.ganancia_sesion = 0 #% Porcentaje de ganancia acumulada hasta ahora en esta sesion. 
                
        self.criterios_rankings = ['Crecimiento', 
                                   'Caida',
                                   'Amplitud',
                                   'RSI alto',
                                   'RSI bajo',
                                   'Criterio Bot'] # 'Tendencia y RSI'
        
        self.simbolo = ''
        self.leverage_brackets = None
        self.symbol_info = None
        

    def verificar_api(self):
        
        if (self.api_key == '') or (self.api_secret == ''): return 'incorrecto'
        
        try:
            self.cliente = Client(self.api_key, self.api_secret)
        except:
            traceback.print_exc()
            return 'incorrecto'
        
        try:
            respuesta = self.cliente.get_account_status()
            # print(respuesta)
            # print('')
            if respuesta['data'] == 'Normal': pass
            else: return 'incorrecto'
        except:
            traceback.print_exc()
            return 'incorrecto'
        
        try:
            respuesta = self.cliente.get_account()
            # print(respuesta)
            # print('')
            if respuesta['canTrade'] == True: pass
            else: return 'sin_permiso_trading' 
        except:
            traceback.print_exc()
            return 'incorrecto'
        
        try:
            respuesta = self.cliente.get_account_api_trading_status()
            # print(respuesta)
            # print('')
            if respuesta['data']['isLocked'] == False: pass
            else: return 'trading_bloqueado'
        except:
            traceback.print_exc()
            return 'incorrecto'
        
        try:
            respuesta = self.cliente.get_account_api_permissions()
            # print(respuesta)
            # print('')
            # if respuesta['enableSpotAndMarginTrading'] == True: pass
            # else: return 'no_spot_trading'
            
            if respuesta['enableFutures'] == True: pass
            else: return 'no_futures_trading'
            
        except:
            traceback.print_exc()
            return 'incorrecto'
        
        return 'correcto'
        
            
    def sincronizar(self):
        server_date_time = obtain_server_time_now(self.url_base, 'datetime', system_time_updated = False)
        global shift
        # adelanto = datetime.timedelta(minutes=4*60) # GMT Venezuela: +4h
        server_date_time = server_date_time + shift
                
        server_date = datetime_to_str(server_date_time)
        dayOfWeek = int(server_date_time.weekday())     
        
        year = int(server_date[0:4])
        month = int(server_date[5:7])
        day = int(server_date[8:10])
        hour = int(server_date[11:13])
        minute = int(server_date[14:16])
        second = int(server_date[17:19])
        millseconds = int(server_date[20:23])
        
        win32api.SetSystemTime(year, month, dayOfWeek, day, hour, minute, second, millseconds)
        
                
    def obtener_lista_de_simbolos(self, quote, max_num_criptos = None):
        # print(self.cliente.futures_leverage_bracket(symbol = 'BTCUSDT'))
        exchange_info = self.cliente.futures_exchange_info()
        lista=[]
        c=1
        d = len(quote)
        for elemento in exchange_info['symbols']:
            if elemento['symbol'][-d:] == quote: 
                if not (elemento['symbol'] in self.exclude):
                    lista.append(elemento['symbol'])
                    c+=1

            if max_num_criptos is not None:
                if c > max_num_criptos : break
                      
        return lista
   
    def symbol_info(self, simbolo):
        exchange_info= self.cliente.get_exchange_info()
        for elemento in exchange_info['symbols']:
            if elemento['symbol']==simbolo:
                return elemento
                        
    def disponible_asset(self, asset):  
        balance = self.cliente.futures_account_balance()
        #print(balance)
        disp = None
        
        for item in balance:
            if (item['asset'] == asset): 
                disp = float(item['balance'])
                break
            
        return disp


class Crypto():
    
    def __init__(self, simbolo,  klines = [], order_book = {}, precio = -1, precio_max = -2):
                
        self.simbolo = simbolo
        self.klines = klines
        self.precio = precio
        self.last_update_time_klines = np.Infinity
        self.last_candle_open_time = None
                       
        
class HiloStream(PyQt5.QtCore.QThread):
    
    StreamReceived = PyQt5.QtCore.pyqtSignal()
    
    def __init__(self, direccion, streams, simbolos, nombre_hilo):
        """
        'binance.com'
        ['kline_1m', 'depth']
        ['btcusdt', 'ethusdt']
        
        """
        PyQt5.QtCore.QThread.__init__(self)
        self.name = nombre_hilo
        self.streams = streams
        self.simbolos = simbolos
        self.manager = BinanceWebSocketApiManager(exchange = direccion, warn_on_update = False)
        self.last_message = None
        self.detener = False
        
    def run(self):
        stream_id = self.manager.create_stream(self.streams, self.simbolos)
        while not self.detener: 
            oldest_data_from_stream_buffer = self.manager.pop_stream_data_from_stream_buffer()
            if oldest_data_from_stream_buffer: 
                self.last_message = UnicornFy.binance_com_websocket(oldest_data_from_stream_buffer)
                
                self.StreamReceived.emit()
            
        self.manager.stop_stream(stream_id) 
        
        try:            
            self.manager.stop_manager_with_all_streams()
        except:
            traceback.print_exc()
            pass
  
    
class Scanner(PyQt5.QtCore.QThread): 
    
    ProgressUpdate = PyQt5.QtCore.pyqtSignal()
    ScanningEnded = PyQt5.QtCore.pyqtSignal()
    ConnectionLost = PyQt5.QtCore.pyqtSignal()
    CriptosTopUpdated = PyQt5.QtCore.pyqtSignal()
        
    """
    Scanner y Monitor de streams de precios
    
    """
    
    def __init__(self, futuresbot):
        PyQt5.QtCore.QThread.__init__(self)
        self.name='Hilo Scanner Monitor'
        
        self.futuresbot = futuresbot
        self.detener = False
        self.progreso = 0
        
        self.monitor_timming = 0.75*60*self.futuresbot.muestreo
        
        self.CRYPTOS = {} # Datos de cada simbolo {'BTCUSDT': [...], 'ETHUSDT': [...]}
        self.last_candle_was_closed = {} # {'BTCUSDT': False, 'ETHUSDT': True}
        # self.criterios = ['Crecimiento', 'Caida', 'Amplitud', 'RSI alto',
        #                   'RSI bajo', 'Tendencia y RSI']
        self.Rankings = {} # un ranking por cada criterio
        # {'Gravedad': [{'simbolo':'BTCUSDT', 'puntaje':231.5}, {'simbolo':'ETHUSDT', 'puntaje':643.8}, ...], 'ssl': [...], ...}
        
        self.hilo_stream_klines = None
        # self.receptor_de_stream_klines_is_bussy = False
        self.list_of_simbols_verified = []
        
        self.STREAM_MESSAGES_BUFFER = {}
        
        self.futuresbot.cvp.ventana_rankings.PbtnActualizarClicked.connect(self.ventana_rankings_pbtn_actualizar_clicked)
        
        self.lets_obtain_ranking = False
        
                
    def escanear(self):
        self.escanear_criptos()
    
    def escanear_criptos(self):
        
        e = 0
        c = 0
        
        for simb in self.futuresbot.lista_de_simbolos:
                
            if self.detener: break
                  
            try: 
                
                time_actual = obtain_server_time_now(self.futuresbot.url_base,'time')
                time_actual = time_actual * 1000 # en milisegundos
                lapso_estudio = self.futuresbot.T*60*1000 #en milisegundos
                time_inicio = int(time_actual-lapso_estudio)
                time_final = int(time_actual)
                
                data_klines = self.futuresbot.cliente.futures_historical_klines(symbol = simb,
                                                                                interval = self.futuresbot.vela,
                                                                                start_str = time_inicio,
                                                                                end_str  = time_final,
                                                                                limit = 1000)
            except: 
                traceback.print_exc()
                data_klines = None
                
            tamanho = int(self.futuresbot.T / self.futuresbot.muestreo)
            
            if data_klines_correcto(data_klines, tamanho):
                
                data_klines_formateada = formatear_klines(data_klines)
                
                # if pasa_prueba_volumen(data_klines_formateada, vol_min = self.futuresbot.vol_min, inversion = self.futuresbot.capital_a_invertir): 
                if True:                   
                    self.CRYPTOS[simb] = Crypto(simb, klines = data_klines_formateada,
                                                order_book = {}, precio = data_klines_formateada[-1][4])
                    
                    self.CRYPTOS[simb].last_candle_open_time = self.CRYPTOS[simb].klines[-1][0]
                    
                    for fila in self.CRYPTOS[simb].klines : fila.append(InfoVela())
                    
                    self.list_of_simbols_verified.append(simb)
                    self.STREAM_MESSAGES_BUFFER[simb] = deepcopy([None]*1)
                    self.configurar_stream_klines(self.list_of_simbols_verified, self.futuresbot.vela)
                    
                    c += 1
                    # print(c)
                    self.progreso = 100*c/self.futuresbot.numero_de_monedas
                    self.ProgressUpdate.emit()
                    
                    if c >= self.futuresbot.numero_de_monedas : break
                    # sleep(1)
                    
                else:
                    pass
                    # e += 1
                    # print(e)
            else:
                # e += 1
                # print(e)
                pass
                                          
   
    def lista_ordenada_mayor_a_menor(self, lista_de_criptos, clave):
           
        def obtener(cripto):
            return cripto.get(clave)
        
        lista_de_criptos.sort(key=obtener, reverse=True)
        
        return lista_de_criptos
    
    
    def configurar_stream_klines(self, list_of_symbols, vela):
        
        if self.hilo_stream_klines is None: pass
        else: self.hilo_stream_klines.detener = True
                
        simbolos = []
        
        for symbol in list_of_symbols: simbolos.append(symbol.lower())
        
        direccion = 'binance.com-futures'
        
        streams = ['kline_'+vela]
                
        self.hilo_stream_klines = HiloStream(direccion, streams, simbolos, 'Hilo Stream Klines')
        
        #Conexion
        self.hilo_stream_klines.StreamReceived.connect(self.receptor_de_stream_klines)
        
        self.hilo_stream_klines.start()
        
   
    def receptor_de_stream_klines(self):
        
        if hasattr(self, 'hilo_stream_klines'): pass
        else: return
        
        message = self.hilo_stream_klines.last_message
        
        if message is not None: pass
        else: return
        
        if 'stream_type' in message: pass
        else: return
        
        simbolo = message['symbol']
                                    
        insertar_elemento_final(self.STREAM_MESSAGES_BUFFER[simbolo], message)

    
    def process_last_message_from_buffer(self, simbolo):
                
        message = self.STREAM_MESSAGES_BUFFER[simbolo][-1]
        
        if message is not None: pass
        else: return
        
        
        """
        Formato data_klines:
            [
                [
                  open time (mili seconds),  # int
                  open price,                # str
                  high price,                # str
                  low price,                 # str
                  close price,               # str
                  volume in base,            # str
                  close time (mili seconds), # int
                  volume in quote,           # str
                  number of trades,          # int
                  taker buy base volume,     # str
                  taker buy quote volume,    # str
                  can be ignored,            # str
                  información de la vela     # InfoVela
                ]
            ]
            
        
        """
        
        
        """
        Formato stream: (Unicorn)
            {
                'stream_type': 'btcusdt@kline_1m',
                'event_type': 'kline'               # event type
                'event_time': int                   # event time (miliseconds)
                'symbol': 'BTCUSDT'                 # symbol
                'kline': {
                            'kline_start_time': int         # kline start time (miliseconds)
                            'kline_close_time': int         # kline close time (miliseconds)
                            'symbol': 'BTCUSDT'             # symbol
                            'interval': '1m'                # interval
                            'first_trade_id': str           # first trade ID
                            'last_trade_id': str            # last trade ID
                            'open_price': str               # open price
                            'close_price': str              # close price
                            'high_price': str               # high price
                            'low_price': str                # low price
                            'base_volume': str              # volume in base
                            'number_of_trades': int         # number of trades
                            'is_closed': False              # is this kline closed?
                            'quote': str                    # volume in quote
                            'taker_by_base_asset_volume': str                   
                            'taker_by_quote_asset_volume': str         
                            'ignore': str         
                        }
            }
        
        """
        
        # self.receptor_de_stream_klines_is_bussy = True
        
        simbolo = message['symbol']
        
        vela = message['kline']
        
        self.CRYPTOS[simbolo].time_last_kline_update = obtain_server_time_now(self.futuresbot.url_base, 
                                                                              tipo = 'time', unit = 'seconds')
        
        fila = [vela['kline_start_time'], # open time [mili seconds]
                vela['open_price'], # open price
                vela['high_price'], # high price
                vela['low_price'], # low price
                vela['close_price'], # close price
                vela['base_volume'], # volume in base
                vela['kline_close_time'], # close time [mili seconds]
                vela['quote'], # volume in quote
                vela['number_of_trades'], # number of trades
                vela['taker_by_base_asset_volume'], # taker buy base volume
                vela['taker_by_quote_asset_volume'], # taker buy quote volume
                vela['ignore'], # can be ignored
                InfoVela()] # info de la vela
        
        fila[0] = int(fila[0])
        fila[1] = float(fila[1])
        fila[2] = float(fila[2])
        fila[3] = float(fila[3])
        fila[4] = float(fila[4])
        fila[5] = float(fila[5])
        fila[6] = int(fila[6])
        fila[7] = float(fila[7])
        fila[8] = int(fila[8])
        fila[9] = float(fila[9])
        fila[10] = float(fila[10])
        fila[11] = float(fila[11])
        
        if fila[0] > self.CRYPTOS[simbolo].last_candle_open_time: # la vela anterior ya cerró
        
            insertar_elemento_final(self.CRYPTOS[simbolo].klines, fila)
            self.CRYPTOS[simbolo].last_candle_open_time = fila[0]
            
        else: # la vela no ha cerrado
        
            self.CRYPTOS[simbolo].klines[-1] = fila
        
            
        self.CRYPTOS[simbolo].precio = self.CRYPTOS[simbolo].klines[-1][4]              
        self.CRYPTOS[simbolo].last_update_time_klines = obtain_server_time_now(self.futuresbot.url_base, tipo = 'time', unit = 'seconds')
     
    def actualizar_klines(self):
        for simbolo in self.CRYPTOS: self.process_last_message_from_buffer(simbolo)
    
    def ventana_rankings_pbtn_actualizar_clicked(self):        
        self.lets_obtain_ranking = True
                 
        
    def obtener_rankings(self, criterios):
        for criterio in criterios:
            self.Rankings[criterio] = []
            lista_criptos_puntajes = [] # [{'simbolo':'BTCUSDT','puntaje':341.2}, {'simbolo':'ETHUSDT','puntaje':560.5}, ...]

            for simbolo in self.CRYPTOS:
                
                if simbolo in self.futuresbot.exclude:
                    puntaje = -20
                    elemento = {'simbolo':simbolo, 'puntaje': puntaje}
                    lista_criptos_puntajes.append(elemento)
                    continue
                
                # 'Crecimiento', 
                #                    'Caida',
                #                    'Amplitud',
                #                    'RSI alto',
                #                    'RSI bajo',
                #                    'Tendencia y RSI'
                

                if criterio == 'Crecimiento':
                    try:
                        puntaje = IndicadorCrecimiento(self.CRYPTOS[simbolo].klines, self.futuresbot.npt)  
                    except:
                        traceback.print_exc()
                        puntaje = -10
                        
                elif criterio == 'Caida':
                    try:
                        puntaje = IndicadorCaida(self.CRYPTOS[simbolo].klines, self.futuresbot.npt) 
                    except:
                        traceback.print_exc()
                        puntaje = -10
                        
                elif criterio == 'Amplitud':
                    try:
                        
                        puntaje = IndicadorAmplitud(self.CRYPTOS[simbolo].klines, self.futuresbot.npt)  
                    except:
                        traceback.print_exc()
                        puntaje = -10
                        
                elif criterio == 'RSI alto':
                    try:
                        puntaje = IndicadorRSIalto(self.CRYPTOS[simbolo].klines, self.futuresbot.nprsi)  
                    except:
                        traceback.print_exc()
                        puntaje = -10
                                                                                                        
                elif criterio == 'RSI bajo':
                    try:
                        puntaje = IndicadorRSIbajo(self.CRYPTOS[simbolo].klines, self.futuresbot.nprsi)   
                    except:
                        traceback.print_exc()
                        puntaje = -10
                        
                elif criterio == 'Tendencia y RSI':
                    try:
                        puntaje = IndicadorEMARSI(self.CRYPTOS[simbolo].klines, self.futuresbot.npt, self.futuresbot.nprsi) 
                    except:
                        traceback.print_exc()
                        puntaje = -10
                        
                elif criterio == 'Criterio Bot':
                    try:
                        puntaje = IndicadorCriterioBot(self.CRYPTOS[simbolo].klines, self.futuresbot.npt) 
                    except:
                        traceback.print_exc()
                        puntaje = -10

                elif criterio == '':
                    pass
                
                elemento = {'simbolo':simbolo, 'puntaje': puntaje}
                lista_criptos_puntajes.append(elemento)
            
            self.Rankings[criterio] = self.lista_ordenada_mayor_a_menor(lista_criptos_puntajes, 'puntaje')
        
        self.CriptosTopUpdated.emit()
                  
    def run(self):
         
        try:
            
            self.escanear()
            self.ScanningEnded.emit()
            
            inicio = time()
            
            while not self.detener:
                
                final = time()
                
                if (final - inicio > self.monitor_timming) or self.lets_obtain_ranking:
                    self.actualizar_klines()
                    
                    if self.lets_obtain_ranking:
                        self.obtener_rankings(self.futuresbot.criterios_rankings)
                        self.lets_obtain_ranking = False
                
                    inicio = time()
                   
        except:
            traceback.print_exc()
            try: 
                self.hilo_stream_klines.detener = True
            except: 
                pass
        
        try: 
            self.hilo_stream_klines.detener = True
        except: 
            pass
        


class Scalper(PyQt5.QtCore.QThread):
    
    newMessageUpdated = PyQt5.QtCore.pyqtSignal()
    JustSell = PyQt5.QtCore.pyqtSignal()
    GananciaEnOperacionUpdated = PyQt5.QtCore.pyqtSignal()
    newMessageToPrompt = PyQt5.QtCore.pyqtSignal()
    
    def __init__(self, futuresbot):
        PyQt5.QtCore.QThread.__init__(self)
        self.name='Hilo Scalper'
        
        self.futuresbot = futuresbot
        
        self.detener = False
 
        self.anterior_capital_a_invertir = self.futuresbot.capital_a_invertir
        self.cantidad_asset_comprado = 0
                                                        
        self.ganancia_sesion = 0
        
        self.stop_loss = None
        
        self.max_g_op = -np.Infinity
        
        self.lets_buy = False
        self.lets_sell = False
        
        self.venta_automatica = self.futuresbot.cvp.chkbx_venta_automatica.isChecked()
        
        self.simbolo = None
        
        self.g_op_calc = None
        
        self.hilo_stream_klines = None
                
        self.scanner = None
        
        self.motivo_de_venta = None
        
        self.message_to_prompt = ''
        
        self.klines = None
        
             
    def anunciar_ganancia(self, ganancia):
        
        self.message_lstw = 'Ganancia en operación: ' +str(round(ganancia,3)) +' %\n'
        self.futuresbot.historial.append(self.message_lstw)
        self.newMessageUpdated.emit()
        sleep(1)
        
    def anunciar_motivo_de_venta(self, motivo):
        self.message_lstw = motivo
        self.futuresbot.historial.append(self.message_lstw)
        self.newMessageUpdated.emit()
        sleep(1)

    def anunciar_venta(self, simbolo, precio, cantidad = None):
        now = obtain_server_time_now(self.futuresbot.url_base, tipo='date')[:-5] #precision 0.1 segundo
        
        if cantidad is None:
            self.message_lstw = '--- Vende ' +simbolo + ' @' +str(round(precio,8)) + ' ' + self.futuresbot.quote +' || ' + now
        else:
            self.message_lstw = '--- Vende ' +str(cantidad)+ ' ' +simbolo + ' @' +str(round(precio,8)) + ' '+self.futuresbot.quote +' || ' + now
        
        self.futuresbot.historial.append(self.message_lstw)
        self.newMessageUpdated.emit()
        sleep(1)
        
    def anunciar_compra(self, simbolo, precio, cantidad = None):
        now = obtain_server_time_now(self.futuresbot.url_base, tipo='date')[:-5] #precision 0.1 segundo
        
        if cantidad is None:
            self.message_lstw = '--- Compra ' +simbolo + ' @' +str(round(precio,8)) + ' ' + self.futuresbot.quote +' || ' + now
        else:
            self.message_lstw = '--- Compra ' +str(cantidad)+ ' ' +simbolo + ' @' +str(round(precio,8)) + ' '+self.futuresbot.quote +' || ' + now
        
        self.futuresbot.historial.append(self.message_lstw)
        self.newMessageUpdated.emit()
        sleep(1)

                  
    def activa_criterio_venta(self, simbolo, precio_compra):
                
        self.klines = formatear_klines(obtener_klines(simbolo, 3*self.futuresbot.muestreo, self.futuresbot.vela, self.futuresbot.url_base))
        
        precio_actual = self.klines[-1][4]
        
        precio_venta = self.price_filter(precio_actual*(self.futuresbot.pvr/100), simbolo)
                
        if precio_actual <= self.stop_loss: 
            self.motivo_de_venta = 'Venta por Stop Loss'
            return True
            
        # # si hay fondos en bnb para pagar los fees, aquí comision es 0
        # comision = 0 #self.futuresbot.comision
        
        # #capital_pre_compra = self.anterior_capital_a_invertir
        # capital_post_compra = precio_compra*self.cantidad_asset_comprado       
        # # capital_pre_venta = self.cantidad_asset_comprado*precio_actual
        
        # precio_venta = self.price_filter(precio_actual*(self.futuresbot.pvr/100), simbolo)
        # cantidad_post_venta = self.cantidad_asset_comprado #self.qty_filter(self.cantidad_asset_comprado*(1-comision/100), simbolo)        
        # capital_post_venta = cantidad_post_venta*precio_venta
        
        # asset = simbolo[:-len(self.futuresbot.quote)]
        # resto_qty = self.futuresbot.disponible_asset(asset) - cantidad_post_venta
        
        # g = 100*(capital_post_venta - capital_post_compra)/(capital_post_compra)
        
        Ci = self.precio_compra*self.cantidad_asset_comprado
        Cf = precio_venta*self.cantidad_asset_comprado
        
        # g = 100*(precio_actual - precio_compra)/precio_compra # en realidad, este es el crecimiento
        
        g = 100*(Cf - Ci)/Ci # las comisiones se cobran de BNB
        
        self.g_op_calc = g
        self.GananciaEnOperacionUpdated.emit()
        
        if (self.max_g_op is None) and (g > self.futuresbot.gmin): 
            self.max_g_op = g
            return False
        
        if not self.max_g_op is None:
            
            if g > self.futuresbot.gmin:            
                # if g < self.futuresbot.gmin:
                #     self.motivo_de_venta = 'Venta por caída debajo de gmin'
                #     return True
                                
                if g <= self.max_g_op*(1 - self.futuresbot.max_fall/100):
                    self.motivo_de_venta = 'Venta por Fall Umbral'
                    return True
                else:
                    if g > self.max_g_op: self.max_g_op = g                    
                    return False
            else:
                return False
            

        return False
     
        
    def precio_compra_venta(self, respuesta):
        if float(respuesta['price']) == 0:
            acum = 0
            
            for fill in  respuesta['fills']: acum += float(fill['price'])*float(fill['qty'])
            
            return round(acum/float(respuesta['executedQty']), 8)
                
        else:
            return round(float(respuesta['price']), 8)
        
    def price_filter(self, precio, simbolo):
        symbol_info = self.futuresbot.symbol_info(simbolo)
        
        decimales = int(symbol_info['quotePrecision'])
        
        for elemento in symbol_info['filters']:
            if elemento['filterType']=='PRICE_FILTER':
                tick = round(float(elemento['tickSize']),decimales)
                break
            
        # precio = precio - (precio % tick)/tick
        
        # t = decimal.Decimal(str(tick))
        # d = t.as_tuple().exponent
        # d=abs(d)
        
        # precio=round(precio,d)
        
        # return precio
        
        acum = 0
        
        while acum <= precio: acum += tick
        
        acum -= tick
        
        acum = round(acum,decimales)
        
        return acum
    
    def qty_filter(self, cantidad, symbol_info):
        
        decimales = int(symbol_info['baseAssetPrecision'])
        
        for filtro in symbol_info['filters']:
            if filtro['filterType']=='MARKET_LOT_SIZE':
                step = round(float(filtro['stepSize']),decimales)
                break
                        
        acum = 0
        
        while acum <= cantidad: acum += step
        
        acum -= step
        
        acum = round(acum,decimales)
        
        return acum
    
    def comprar(self, simbolo):
        if self.futuresbot.modo == 'Simulación':
                       
            self.anterior_capital_a_invertir = self.futuresbot.capital_a_invertir
            self.futuresbot.capital_a_invertir = self.futuresbot.capital_a_invertir*(1 - self.futuresbot.comision/100)
            precio_compra = self.scanner.CRYPTOS[simbolo].precio
            self.cantidad_asset_comprado = self.futuresbot.capital_a_invertir/precio_compra
            self.anunciar_compra(simbolo, precio_compra)
            return precio_compra
        else:
            # Emitir una orden de compra tipo limit
            self.futuresbot.salvo = self.futuresbot.disponible - self.futuresbot.capital_a_invertir
            self.anterior_capital_a_invertir = self.futuresbot.capital_a_invertir
            asset = simbolo[:-len(self.futuresbot.quote)]
            cantidad_previa_asset = self.futuresbot.disponible_asset(asset)
            
            self.klines = formatear_klines(obtener_klines(simbolo, 3*self.futuresbot.muestreo, self.futuresbot.vela, self.futuresbot.url_base))
            
            price = self.klines[-1][4]
            precio = self.price_filter(price*(self.futuresbot.pcr/100), simbolo)
            cantidad = self.qty_filter(self.futuresbot.capital_a_invertir/precio, simbolo)
            respuesta = self.futuresbot.cliente.create_order(symbol = simbolo,
                                                          side = 'BUY',
                                                          type = 'LIMIT',
                                                          timeInForce = 'GTC',
                                                          quantity = cantidad,
                                                          price = precio)
            order_id = respuesta['orderId']
            
            sleep(1)
            
            respuesta = self.futuresbot.cliente.get_order(symbol = simbolo, orderId = order_id)
                       
            while respuesta['status'] != 'FILLED': 
                
                if respuesta['status'] == 'PARTIALLY_FILLED': 
                    pass
                    # Resolver esto
                    print('\nCompra PARTIALLY_FILLED\n')
                else:
                    
                    cancel = self.futuresbot.cliente.cancel_order(symbol = simbolo, orderId = order_id)
                    
                    self.klines = formatear_klines(obtener_klines(simbolo, 3*self.futuresbot.muestreo, self.futuresbot.vela, self.futuresbot.url_base))
                    
                    price = self.klines[-1][4]
                    precio = self.price_filter(price*(self.futuresbot.pcr/100), simbolo)
                    cantidad = self.qty_filter(self.futuresbot.capital_a_invertir/precio, simbolo)
                    respuesta = self.futuresbot.cliente.create_order(symbol = simbolo,
                                                                  side = 'BUY',
                                                                  type = 'LIMIT',
                                                                  timeInForce = 'GTC',
                                                                  quantity = cantidad,
                                                                  price = precio)
                    order_id = respuesta['orderId']
                    
                    self.message_to_prompt = 'Intentando comprar al precio: ' + str(precio)
                    self.newMessageToPrompt.emit()
                    sleep(1)
                    
                    respuesta = self.futuresbot.cliente.get_order(symbol = simbolo, orderId = order_id)
                
                            
            self.message_to_prompt = ''
            self.newMessageToPrompt.emit()
            precio_compra = self.precio_compra_venta(respuesta)
            self.precio_compra = precio_compra
            self.cantidad_asset_comprado = float(respuesta['executedQty']) #self.qty_filter(self.futuresbot.disponible_asset(asset) - cantidad_previa_asset, simbolo)
            #self.cantidad_asset_comprado = self.futuresbot.disponible_asset(asset) - cantidad_previa_asset
            #float(respuesta['origQty'])
            self.anunciar_compra(simbolo, precio_compra, self.cantidad_asset_comprado)
            
            #Emitir una orden oco de emergencia
            # precio_profit = self.price_filter(round(precio_compra*(1 + self.futuresbot.oco_p_profit), 8), simbolo) 
            # precio_stop = self.price_filter(round(precio_compra*(1 - self.futuresbot.oco_p_stop), 8), simbolo) 
            # precio_limit = self.price_filter(round(precio_compra*(1 - self.futuresbot.oco_p_limit), 8), simbolo) 
            
            
            
            # respuesta_oco = send_oco_sell_order(self.futuresbot.cliente, simbolo,
            #                                     self.cantidad_asset_comprado, 
            #                                     precio_profit, 
            #                                     precio_stop, 
            #                                     precio_limit)
            
            respuesta_oco = None
            
            
            if not (respuesta_oco is None): self.futuresbot.id_oco = respuesta_oco['orderListId']
            else: self.futuresbot.id_oco = None
            
            return precio_compra
    
    def vender(self, simbolo):
        if self.futuresbot.modo == 'Simulación':
            
            precio_venta = self.scanner.CRYPTOS[simbolo].precio
            self.futuresbot.capital_a_invertir = self.cantidad_asset_comprado*precio_venta
            self.futuresbot.capital_a_invertir = self.futuresbot.capital_a_invertir*(1 - self.futuresbot.comision/100)
            ganancia = 100*(self.futuresbot.capital_a_invertir - self.anterior_capital_a_invertir)/self.anterior_capital_a_invertir
            self.anunciar_venta(simbolo, precio_venta)
            return ganancia
        else:
            # Emitir una orden de compra tipo limit
            
            self.klines = formatear_klines(obtener_klines(simbolo, 3*self.futuresbot.muestreo, self.futuresbot.vela, self.futuresbot.url_base))
            
            price = self.klines[-1][4]
            precio = self.price_filter(price*(self.futuresbot.pvr/100), simbolo)
            cantidad = self.cantidad_asset_comprado 
            respuesta = self.futuresbot.cliente.create_order(symbol = simbolo,
                                                          side = 'SELL',
                                                          type = 'LIMIT',
                                                          timeInForce = 'GTC',
                                                          quantity = cantidad,
                                                          price = precio)
            order_id = respuesta['orderId']
            
            sleep(1)
            
            respuesta = self.futuresbot.cliente.get_order(symbol = simbolo, orderId = order_id)
                       
            while respuesta['status'] != 'FILLED': 
                
                if respuesta['status'] == 'PARTIALLY_FILLED': 
                    pass
                    # Resolver esto
                    print('\nVenta PARTIALLY_FILLED\n')
                else:
                    
                    respuesta = self.futuresbot.cliente.cancel_order(symbol = simbolo, orderId = order_id)
                    
                    self.klines = formatear_klines(obtener_klines(simbolo, 3*self.futuresbot.muestreo, self.futuresbot.vela, self.futuresbot.url_base))
                    
                    price = self.klines[-1][4]
                    precio = self.price_filter(price*(self.futuresbot.pvr/100), simbolo)
                    cantidad = self.cantidad_asset_comprado 
                    respuesta = self.futuresbot.cliente.create_order(symbol = simbolo,
                                                                  side = 'SELL',
                                                                  type = 'LIMIT',
                                                                  timeInForce = 'GTC',
                                                                  quantity = cantidad,
                                                                  price = precio)
                    order_id = respuesta['orderId']
                    
                    self.message_to_prompt = 'Intentando vender al precio: ' + str(precio)
                    self.newMessageToPrompt.emit()
                    sleep(1)
                    
                    respuesta = self.futuresbot.cliente.get_order(symbol = simbolo, orderId = order_id)
 
            
            self.message_to_prompt = ''
            self.newMessageToPrompt.emit()
            
            precio_venta = self.precio_compra_venta(respuesta)
            cantidad_venta = float(respuesta['executedQty'])
            #self.futuresbot.capital_a_invertir = cantidad*precio_venta
            self.futuresbot.disponible = self.futuresbot.disponible_asset(self.futuresbot.quote)
            self.futuresbot.capital_a_invertir = self.futuresbot.disponible - self.futuresbot.salvo
            
            #ganancia = 100*(self.futuresbot.capital_a_invertir - self.anterior_capital_a_invertir)/self.anterior_capital_a_invertir
            Ci = self.precio_compra*self.cantidad_asset_comprado
            Cf = precio_venta*cantidad_venta
            
            ganancia = 100*(Cf - Ci)/Ci
            
            self.anunciar_venta(simbolo, precio_venta, self.cantidad_asset_comprado)

            
            #Cancelar la orden oco de emergencia
            if not(self.futuresbot.id_oco is None):
                result = self.futuresbot.cliente.cancel_order(symbol = simbolo, orderId = self.futuresbot.id_oco)
                self.futuresbot.id_oco = None
            
            return ganancia
    
        
    def run(self):
        
        try:
            
            while not self.detener: 
                
                if self.lets_buy:
                                        
                    precio_compra = self.comprar(self.simbolo)
                    
                    if self.klines[-2][3] < self.klines[-1][3]: low = self.klines[-2][3]
                    else: low = self.klines[-1][3]
                    
                    self.stop_loss = low*(1-self.futuresbot.stop_loss/100)
                    
                    while not self.lets_sell:
                        sleep(1) # descanso al procesador
                        if self.detener: break
                        
                        can_sell = self.activa_criterio_venta(self.simbolo, precio_compra)
                        
                        if self.venta_automatica: self.lets_sell = can_sell
                        else: pass
                    
                                                               
                    self.g_op_calc = 0
                    ganancia = self.vender(self.simbolo)
                    if ganancia is None: return
                    if self.venta_automatica: self.anunciar_motivo_de_venta(self.motivo_de_venta)
                    self.anunciar_ganancia(ganancia)
                    capital_en_bnb = self.futuresbot.disponible_asset('BNB')*float(self.futuresbot.cliente.get_klines(symbol = 'BNB'+self.futuresbot.quote, interval = self.futuresbot.vela)[-1][4])        
                    self.futuresbot.ganancia_sesion = 100*( self.futuresbot.capital_a_invertir + capital_en_bnb - self.futuresbot.capital_a_invertir_inicio_sesion)/self.futuresbot.capital_a_invertir_inicio_sesion
                    self.JustSell.emit()
                    
                    self.lets_buy = False
        
        except:
            traceback.print_exc()
            pass
        



### Funciones Generales
def VolumeWeightedAveragePrice(data_klines, last_n_intervals, value_of_candle):
    init = len(data_klines) - last_n_intervals
    final = len(data_klines) - 1
    
    acum_vp=0
    acum_v=0
    vwap = []

    for i in range(init,final+1):
        if value_of_candle == 'precio tipico': price = (float(data_klines[i][2])+float(data_klines[i][3])+float(data_klines[i][4]))/3
        volume = float(data_klines[i][5])
        pv = price * volume
        acum_vp += pv
        acum_v += volume
        
        if acum_v != 0: vwap.append(acum_vp/acum_v)
        else: vwap.append(0)
            
    return vwap[-1]



# def Weights_Moving_Averages(np,tipo_av,peso_minimo):
#     N = np - 1
#     pm = peso_minimo
#     weights=[]
    
#     if tipo_av == 'lineal':
#         for i in range(np): 
#             if np == 1 : weights.append(1)
#             elif np > 1 : weights.append(((1-pm)/N)*i + pm)
            
#     elif tipo_av == 'exponencial':
#         for i in range(np): 
#             if np == 1 : weights.append(1)
#             elif np > 1 : weights.append(math.e**((-1*(math.log(pm))/N)*(i-N)))
        
#     return weights

# def Moving_Averages(data,pesos,npc,npm,npl):  
    
#     npmax=max(npc,npm,npl) # máximo número de períodos
    
#     acum_corto=0
#     acum_medio=0
#     acum_largo=0

#     for i in range(1,npmax+1):

#         valor = pesos[-1*i]*data[-1*i]
        
#         if i <= npc: acum_corto+=valor
#         if i <= npm: acum_medio+=valor
#         if i <= npl: acum_largo+=valor
                       
#     if npc > 0 : av_corto = acum_corto / npc
#     else: av_corto = 0
    
#     if npm > 0 : av_medio = acum_medio / npm
#     else: av_medio = 0
    
#     if npl > 0 : av_largo = acum_largo / npl
#     else: av_largo = 0
        
#     return av_corto, av_medio, av_largo

# def SimpleAverage(data,init,final):
#     avgs = []
    
#     for i in range(init,final+1):
#         acum = 0
#         for j in range(init+1): acum+=data[i-j]
#         p = acum/(init+1)
        
#         avgs.append(p)
            
#     return avgs
    
def copia_de_lista(original):
    copia = []
    for elemento in original: copia.append(elemento)
    return copia
    
# def SimpleAverage(data_original,init,final):
#     data = copia_de_lista(data_original)
#     last_n = final - init + 1
#     avgs = []
    
#     for i in range(init,final+1):
#         suma = 0
#         for j in range(i - last_n + 1, i + 1): suma += data[j]
#         av = suma/last_n
#         avgs.append(av)
#         data[i] = av
            
#     return avgs

def SimpleAverage(data,init,final):
    last_n = final - init + 1
    
    r = talib.SMA(np.array(data), timeperiod=last_n)
    
    return r.tolist()

    
    # suma = 0
    # for j in range(init - last_n + 1, init + 1): suma += data[j]
    # av = suma/last_n
    # previo = av
    
    # suma_2 = previo
    
    # for i in range(init+1,final+1): suma_2+=data[i]
                    
    # return suma_2/last_n

def ExponentialAverage(data,init,final):
    
    last_n = final - init + 1
    
    r = talib.EMA(np.array(data), timeperiod=last_n)
    
    return r.tolist()
    
    
    
    # if not from_first:
    #     delta = final - init + 1
    #     i_sa = init - round(0.75*delta)
    #     f_sa = init - 1
    #     anterior = SimpleAverage(data,i_sa,f_sa)[-1]
    #     avgs = []
        
    #     last_periods = f_sa - i_sa + 1
        
    #     for i in range(delta):
    #         last_periods+=1
    #         c = 2/(last_periods+1)
    #         anterior = (data[init+i]-anterior)*c + anterior
    #         avgs.append(anterior)
        
    #     return avgs
    
    # else:
    #     delta = final - init + 1
    #     anterior = 0
    #     avgs = []
        
    #     last_periods=0
        
    #     for i in range(delta):
    #         last_periods+=1
    #         c = 2/(last_periods+1)
    #         anterior = (data[init+i]-anterior)*c + anterior
    #         avgs.append(anterior)
        
    #     return avgs
    

def VWAP(data_klines, last_n_intervals, value_of_candle='precio tipico'):
    Lista = []
    init = len(data_klines) - last_n_intervals
    final = len(data_klines) - 1
    
    for i in range(init,final+1):
        Lista.append(VolumeWeightedAveragePrice(data_klines[i-last_n_intervals+1:i+1], last_n_intervals, value_of_candle))

    return Lista

def SMA(data_klines,last_n_intervals):

    closes = data_klines_to_data(data_klines,'close')
    init_index = len(closes) - last_n_intervals
    final_index = len(closes) - 1
    
    return SimpleAverage(closes,init_index,final_index)[-1*last_n_intervals:]
    
def EMA(data_klines, last_n_intervals):
    closes = data_klines_to_data(data_klines,'close')
    init_index = len(closes) - last_n_intervals
    final_index = len(closes) - 1
    
    return ExponentialAverage(closes,init_index,final_index)[-1*last_n_intervals:]


# def EMA(data,last_n_intervals):
#     closes = data_klines_to_data(data_klines,'close')
#     return talib.EMA(np.array(closes), timeperiod=last_n_intervals)
    

import pandas as pd
import ta

def RSI(data_klines, last_n_intervals): 
    closess = data_klines_to_data(data_klines, 'close')
    
    closes = pd.Series(closess)
    
    RSI_Indicator = ta.momentum.RSIIndicator(close = closes, window = last_n_intervals, fillna = False)
    
    r = RSI_Indicator.rsi()
    
    res = r.tolist()
    return res
    # copia = []
    
    # for item in res: copia.append(item)

    # return copia

# def RSI(data_klines, last_n_intervals): 
#     closes = data_klines_to_data(data_klines, 'close')
    
#     return talib.RSI(np.array(closes), timeperiod=last_n_intervals).tolist()[-1*last_n_intervals:]
    
    # U = []
    # D = []
    
       
    # for i in range(1,len(data_klines)):
    #     if closes[i] > closes[i-1]: 
    #         U.append(closes[i] - closes[i-1])
    #         D.append(0)
    #     elif closes[i] < closes[i-1]: 
    #         D.append(closes[i-1] - closes[i])
    #         U.append(0)
    #     elif closes[i] == closes[i-1]: 
    #         U.append(0)
    #         D.append(0)
            
    # # peso_minimo = 0.850
    # # weights = Weights_Moving_Averages(last_n_intervals,'exponencial',peso_minimo)
    # # EMA_U = Moving_Averages(U,weights,npc=0,npm=0,npl=last_n_intervals)[2]
    # # EMA_D = Moving_Averages(D,weights,npc=0,npm=0,npl=last_n_intervals)[2]
            
    # init = len(U) - last_n_intervals
    # final = len(U) - 1
   
    # EMA_U = ExponentialAverage(U,init,final) 
    # EMA_D = ExponentialAverage(D,init,final) 
        
    # rsi = 100*(EMA_U)/(EMA_U + EMA_D)
    # return rsi

    # # return talib.RSI(np.array(closes), timeperiod=last_n_intervals)

# def MACD_hist(data_klines,fastperiod=12,slowperiod=26,signalperiod=9):
#     closes = data_klines_to_data(data_klines,'close')
#     closes = np.array(closes)
#     macd, macdsignal, macdhist = talib.MACD(closes, fastperiod, slowperiod, signalperiod)
#     # print(macd)
#     # print(macdsignal)
#     # print(macdhist)
#     macdhist = macdhist.tolist()
    
#     resp = []
#     for elemento in macdhist:
#         if not math.isnan(elemento): resp.append(elemento)
        
#     return resp
    

def data_klines_to_data(data_klines, valor_de_vela='close'):
    lista=[]
    for i in range(len(data_klines)):
        if valor_de_vela == 'open':
            dato = float(data_klines[i][1]) # el valor open
        elif valor_de_vela == 'close':
            dato = float(data_klines[i][4]) # el valor close
        elif valor_de_vela == 'promedio open close':
            dato = (float(data_klines[i][1])+float(data_klines[i][4]))/2 # el promedio de los valores open y close
        elif valor_de_vela == 'promedio low high':
            dato = (float(data_klines[i][3])+float(data_klines[i][2]))/2 # el promedio de los valores low y high
        elif valor_de_vela == 'precio tipico':
            dato = (float(data_klines[i][3])+float(data_klines[i][2])+float(data_klines[i][4]))/3 # el promedio de low, high y close
        elif valor_de_vela == 'promedio ohlc':
            dato = (float(data_klines[i][1])+float(data_klines[i][2])+float(data_klines[i][3])+float(data_klines[i][4]))/4 # el promedio ohlc
        elif valor_de_vela == 'quote volume':
            dato = float(data_klines[i][7]) # el volumen de la moneda quote
    
        lista.append(dato)
        
    return lista

def print_pretty_candle(vela):

    open_time = datetime.datetime.fromtimestamp(float(vela[0]/1000)).strftime('%Y-%m-%d %H:%M:%S.%f')
    open_price = float(vela[1])
    high_price = float(vela[2])
    low_price = float(vela[3])
    close_price = float(vela[4])
    close_time = datetime.datetime.fromtimestamp(float(vela[6]/1000)).strftime('%Y-%m-%d %H:%M:%S.%f')
    print(open_time)
    print(open_price)
    print(high_price)
    print(low_price)
    print(close_price)
    print(close_time)
    print(' ')
    
def print_pretty_klines(data_klines):
    for vela in data_klines: print_pretty_candle(vela)
    print('\n----------------------------\n\n')
    

def crecimientos(data):
    c = []
    for i in range(len(data)):
        if i == 0: c.append(0)
        elif i > 0: c.append(100*(data[i]-data[i-1])/data[i-1])
    return c

def derivada_proporcional(data,muestreo):
    inicio = 0
    final = len(data) - 1
    
    d = []
    
    for i in range(len(data)):
        if data[i] != 0:
            if i == inicio: d.append(((data[i+1]-data[i])/data[i])/(muestreo))
            elif i > inicio and i < final: d.append(((data[i+1]-data[i-1])/data[i])/(2*muestreo))
            elif i == final: d.append(((data[i]-data[i-1])/data[i])/(muestreo))
        else:
            d.append(-777.0)
    
    return d

def obtener_precio_actual(simbolo,url_base):
    # precio = cliente.get_symbol_ticker(symbol=simbolo)['price']
    # return float(precio)
    
    listo=False
    while not listo:
        try:
            path = '/api/v3/ticker/price'
            
            parametros = {
                'symbol': simbolo
            }
            
            url = urljoin(url_base, path)
            r = requests.get(url, params=parametros)
            if r.status_code == 200:
                respuesta = r.json()['price']
            else:
                raise BinanceException(status_code=r.status_code, data=r.json())

            listo=True
        except:
            listo=False
            traceback.print_exc()
            respuesta = None
            break
    
    return respuesta

def obtain_server_time_now(url_base, tipo, unit = 'seconds', system_time_updated = True):
    """
    tipo: 'time', 'datetime', 'datetime_str'
    unit: 'seconds', 'miliseconds'
    
    """
    if not system_time_updated:
        try:
            path = '/api/v3/time'
            
            parametros = {}
            
            url = urljoin(url_base, path)
            r = requests.get(url, params=parametros)
            if r.status_code == 200:
                respuesta = r.json()['serverTime'] # en milisegundos
            else:
                raise BinanceException(status_code=r.status_code, data=r.json())

        except:
            traceback.print_exc()
            respuesta = None
    else:
        
        respuesta = int(time()*1000) # en milisegundos
        
    if respuesta is None: return None
    
    if tipo == 'time': 
        if unit == 'seconds': return float(respuesta/1000) # en segundos
        elif unit == 'miliseconds': return int(respuesta) # en mili segundos
        
    elif tipo == 'datetime_str': 
        return datetime.datetime.fromtimestamp(float(respuesta/1000)).strftime('%Y-%m-%d %H:%M:%S.%f')
    
    elif tipo == 'datetime':
        return datetime.datetime.fromtimestamp(float(respuesta/1000))

def obtener_klines(simbolo, T, vela, url_base):
    
    time_actual = obtain_server_time_now(url_base,'time')
    time_actual = time_actual * 1000 # en milisegundos
    lapso_estudio = T*60*1000 #en milisegundos
    fecha_inicio = int(time_actual-lapso_estudio)
    fecha_final = int(time_actual)
            
    try:
        path = '/api/v3/klines'
        
        parametros = {
            'symbol': simbolo,
            'interval': vela,
            'startTime': fecha_inicio,
            'endTime': fecha_final,
            'limit': 1000
        }
        
        url = urljoin(url_base, path)
        r = requests.get(url, params=parametros)
        if r.status_code == 200:
            data_klines = r.json()
        else:
            raise BinanceException(status_code=r.status_code, data=r.json())

    except:
        traceback.print_exc()
        data_klines = None
                  
    return data_klines

def obtener_order_book(simbolo, limite, url_base):
    
    try:
        path = '/api/v3/depth'
        
        parametros = {
            'symbol': simbolo,
            'limit': limite
        }
        
        url = urljoin(url_base, path)
        r = requests.get(url, params=parametros)
        if r.status_code == 200:
            respuesta = r.json()
        else:
            raise BinanceException(status_code=r.status_code, data=r.json())

    except:
        traceback.print_exc()
        respuesta = None

    return respuesta


# def send_market_buy_order(cliente, simbolo, quote_qty):
    
#     try:
        
#         respuesta = cliente.create_test_order(symbol =  simbolo, side = 'BUY', type =  'MARKET', quoteOrderQty =  quote_qty)
#         # print(respuesta)
        
#         if respuesta == {}: pass
#         else: return None
        
        

#         respuesta = cliente.create_order(symbol =  simbolo, side = 'BUY', type =  'MARKET', quoteOrderQty =  quote_qty)
#         # print(respuesta)
        
#         # if not 'status' in respuesta: return None
#         # if respuesta['status'] != 'FILLED': return None
        
#         return respuesta

#     except:
#         traceback.print_exc()
#         return None
 

    
# def send_market_sell_order(cliente, simbolo, base_qty):
    
#     try:
        
#         respuesta = cliente.create_test_order(symbol =  simbolo, side = 'SELL', type =  'MARKET', quantity =  base_qty)
        
#         if respuesta == {}: pass
#         else: return None
        
#         respuesta = cliente.create_order(symbol =  simbolo, side = 'SELL', type =  'MARKET', quantity =  base_qty)
        
#         return respuesta

#     except:
#         traceback.print_exc()
#         return None


# def send_market_buy_order(url_base, simbolo, quote_qty):
    
#     try:

#         parametros = {
#             'symbol': simbolo,
#             'side': 'BUY',
#             'type': 'MARKET',
#             'quoteOrderQty': quote_qty,
#             'timestamp': obtain_server_time_now(url_base, tipo = 'time', unit = 'miliseconds')
#         }
        
#         path = '/api/v3/order/test'
        
#         url = urljoin(url_base, path)
#         r = requests.post(url, params=parametros)
#         if r.status_code == 200: respuesta = r.json()
#         else: raise BinanceException(status_code=r.status_code, data=r.json())
#         # print(respuesta)
#         if respuesta == {}: pass
#         else: return None
        
        

#         path = '/api/v3/order'
        
#         url = urljoin(url_base, path)
#         r = requests.post(url, params=parametros)
#         if r.status_code == 200: respuesta = r.json()
#         else: raise BinanceException(status_code=r.status_code, data=r.json())
        
#         while not 'status' in respuesta: pass
#         while respuesta['status'] != 'FILLED': pass
        
#         return respuesta

#     except:
#         traceback.print_exc()
#         return None
    
# def send_market_sell_order(url_base, simbolo, base_qty):
    
#     try:

#         parametros = {
#             'symbol': simbolo,
#             'side': 'SELL',
#             'type': 'MARKET',
#             'quantity': base_qty,
#             'timestamp': obtain_server_time_now(url_base, tipo = 'time', unit = 'miliseconds')
#         }
        
#         path = '/api/v3/order/test'
        
#         url = urljoin(url_base, path)
#         r = requests.post(url, params=parametros)
#         if r.status_code == 200: respuesta = r.json()
#         else: raise BinanceException(status_code=r.status_code, data=r.json())
        
#         if respuesta == {}: pass
#         else: return None
        
        

#         path = '/api/v3/order'
        
#         url = urljoin(url_base, path)
#         r = requests.post(url, params=parametros)
#         if r.status_code == 200: respuesta = r.json()
#         else: raise BinanceException(status_code=r.status_code, data=r.json())
        
#         while not 'status' in respuesta: pass
#         while respuesta['status'] != 'FILLED': pass
        
#         return respuesta

#     except:
#         traceback.print_exc()
#         return None

# def obtener_klines(simbolo,T,vela,muestreo,url_base):
#     #time_actual = time() # en segundos
#     time_actual = obtain_server_time_now(url_base,'time')
#     #print(datetime.datetime.fromtimestamp(time_actual).strftime('%Y-%m-%d %H:%M:%S.%f'))
#     t_peticion = time_actual # en segundos
#     time_actual = time_actual * 1000 # en milisegundos
#     lapso_estudio = T*60*1000 #en milisegundos
#     fecha_inicio = int(time_actual-lapso_estudio)
#     fecha_final = int(time_actual)
    
#     # time_actual = datetime.datetime.now()
#     # datetime.timedelta(weeks = 1, days = 2, hours = 4, minutes = 10,
#     #                        seconds = 8, milliseconds = 25, microseconds = 8)
    
#     last_candle_complete = False
    
#     listo=False
#     while not listo:
#         try:
#             path = '/api/v3/klines'
            
#             parametros = {
#                 'symbol': simbolo,
#                 'interval': vela,
#                 'startTime': fecha_inicio,
#                 'endTime': fecha_final,
#                 'limit': 1000
#             }
            
#             url = urljoin(url_base, path)
#             r = requests.get(url, params=parametros)
#             if r.status_code == 200:
#                 data_klines = r.json()
#             else:
#                 raise BinanceException(status_code=r.status_code, data=r.json())

#             listo=True
#         except:
#             listo=False
#             traceback.print_exc()
#             data_klines = None
#             break
        
#     if data_klines is not None:
#         t_last = float(data_klines[-1][0]/1000) # en segundos
#         delta = (t_peticion - t_last)/60 # en minutos
#         # print(t_peticion)
#         # print(datetime.datetime.fromtimestamp(t_peticion).strftime('%Y-%m-%d %H:%M:%S.%f'))
#         # print(t_last)
#         # print(datetime.datetime.fromtimestamp(t_last).strftime('%Y-%m-%d %H:%M:%S.%f'))
#         # print(delta)
#         # print('')
#         if delta <= muestreo:
#             last_candle_complete = True
#         else:
#             fila_nueva = [-1, # open time
#                           -1, # open price
#                           -1, # high price
#                           -1, # low price
#                           obtener_precio_actual(simbolo,url_base), # close price
#                           -1, # base volume
#                           -1, # close time
#                           -1, # quote volume
#                           -1, # Number of trades
#                           -1, # taker buy base volume 
#                           -1, # taker buy quote volume 
#                           -1] # can be ignored
            
#             data_klines = insertar_elemento_final(data_klines,fila_nueva)
#             last_candle_complete = False
              
#     return data_klines, last_candle_complete

def data_klines_correcto(data_klines, tamanho):
    
    if data_klines is not None: pass
    else: return False
    
    if len(data_klines) == tamanho: pass
    else: return False
    
    # validar el tamaño de cada vela y el formato de cada elemento ?
    try:
        for vela in data_klines:
            
            if len(vela) == 12: pass
            else: return False
            
            if int(vela[0]) > 0 : pass #open time
            else: return False
            
            if float(vela[1]) > 0: pass #open price
            else: return False
            
            if float(vela[2]) > 0: pass #high price
            else: return False
            
            if float(vela[3]) > 0: pass #low price
            else: return False
            
            if float(vela[4]) > 0: pass #close price
            else: return False
            
            if int(vela[6]) > 0: pass #close time
            else: return False
            
            #...
            
          
    except:
        traceback.print_exc()
        return False
        

    return True


def order_book_correcto(order_book):
    
    try:
        if order_book is not None: pass
        else: return False
        
        if len(order_book) == 3: pass
        else: return False
        
        if len(order_book['bids']) > 0 : pass
        else: return False
        
        if len(order_book['asks']) > 0 : pass
        else: return False
        
    except:
        traceback.print_exc()
        return False
        

    return True



def formatear_klines(klines):
    for fila in klines:
        fila[0] = int(fila[0])
        fila[1] = float(fila[1])
        fila[2] = float(fila[2])
        fila[3] = float(fila[3])
        fila[4] = float(fila[4])
        fila[5] = float(fila[5])
        fila[6] = int(fila[6])
        fila[7] = float(fila[7])
        fila[8] = int(fila[8])
        fila[9] = float(fila[9])
        fila[10] = float(fila[10])
        fila[11] = float(fila[11])
        
    return klines

def formatear_order_book(order_book):
    bids = []
    asks = []
    
    for fila in order_book['bids']: bids.append([float(fila[0]),float(fila[1])])
        
    for fila in order_book['asks']: asks.append([float(fila[0]),float(fila[1])])
    
    order_book['bids'] = bids
    order_book['asks'] = asks
    
    return order_book

def ordenar_order_book(order_book):
    """
    Formato Order Book:
        
        {
        'lastUpdateId': int,
        'bids': [
                    [63600.09000000, 0.18030000], # price, quantity
                    [63520.00000000, 0.5030000], # price, quantity
                    ...
                ],
        'asks': [
                    [63552.54000000, 0.00079000], # price, quantity
                    [64000.11000000, 0.01000000], # price, quantity
                    ...
                ]
        }
    
    """
    b = []
    for par in order_book['bids']: b.append(par[0]) # price level
    
    a = []
    for par in order_book['asks']: a.append(par[0]) # price level
    
    b.sort(reverse=True) # de mayor a menor
    a.sort(reverse=False) # de menor a mayor
    
    bids = []
    for price in b:
        for par in order_book['bids']: 
            if par[0] == price: 
                bids.append(par)
                break
        
    asks = []
    for price in a:
        for par in order_book['asks']: 
            if par[0] == price: 
                asks.append(par)
                break
        
    order_book['bids'] = bids
    order_book['asks'] = asks
    
    return order_book



       
def time_to_datetime_str(time):
    """
    Insert time in seconds
    
    """
    r = datetime.datetime.fromtimestamp(time).strftime('%Y-%m-%d %H:%M:%S.%f')
    return r

def datetime_to_str(datetime, decimales=None):
    r = datetime.strftime('%Y-%m-%d %H:%M:%S.%f')
    
    
    if decimales is None: 
        return r
    else: 
        index = -1*(6-decimales)
        return r[:index]
    
def datetime_to_time(datetime):
    """
    Insert a datetime object
    Return time in seconds
    """
    r = datetime.timestamp()
    return r

def tendencia(data, muestreo, last_n=None, Nderivada='primera', average='exponencial'):
    
    if last_n is None:
        last_n = len(data)
    
    init = len(data) - last_n
    final = len(data) - 1

    data = copia_de_lista(data)[init:final+1]

    #c = crecimientos(data)
    d = derivada_proporcional(data,muestreo)

    if Nderivada == 'segunda': d = derivada_proporcional(d,muestreo)
    
    if average == 'lineal': avg = SimpleAverage(d,0,(len(d)-1))[-1]*100
    if average == 'exponencial': avg = ExponentialAverage(d,0,(len(d)-1))[-1]*100
    
    return avg

def separaciones(lista,lista_ref):
    """
    lista y lista_ref son del mismo tamaño
    contienen datos tipo float
    
    """
    
    r = []
    for i in range(len(lista_ref)): r.append( lista[i] - lista_ref[i] ) #r.append( (lista[i]-lista_ref[i])/lista_ref[i] )
    
    return r

def DeltaDataRef(data, Ref, muestreo, s_aceptable=4, last_n=None):
    """
    Indica la separación de los datos respecto de la referencia
    Mayor puntaje para separación positiva pequeña 
    y separación con tendencia creciente
    
    s_aceptable es un porcentaje. Si la separación actual es positiva y menor o igual que s_aceptable
    el puntaje aumenta en +50
    
    si la tendencia es a que la separación aumenta, el puntaje aumenta en +50
    
    """
    if last_n is None:
        last_n = len(Ref)
    
    data_2 = copia_de_lista(data)[-1*last_n:]
    Ref_2 = copia_de_lista(Ref)[-1*last_n:]
    
    sep = separaciones(data_2, Ref_2)
    
    tend = tendencia(sep, muestreo, last_n)
    
    s = 100*(data_2[-1] - Ref_2[-1])/Ref_2[-1]
    # print(s)
    # print(tend)
    r = 0
    
    if (s > 0) and (s <= s_aceptable): r+=50
    if (s > 0) and (tend > 0) : r+=50
                
    return r 

def high_of_candle(vela):
    
    maximo = -np.Infinity
    
    for i in range(1,5):
        if float(vela[i]) > maximo: maximo = float(vela[i])
        
    return maximo

def low_of_candle(vela):
    
    minimo = np.Infinity
    
    for i in range(1,5):
        if float(vela[i]) < minimo: minimo = float(vela[i])
        
    return minimo

def Piso(data_klines, last_n=None):
        
    if last_n is None:
        last_n = len(data_klines)

    klines = copia_de_lista(data_klines)[-1*last_n:-1]

    minimo = np.Infinity
    
    for fila in klines:
        valor = low_of_candle(fila)
        if (valor < minimo): minimo = valor
        
    return minimo    

def Techo(data_klines, last_n=None):
        
    if last_n is None:
        last_n = len(data_klines)

    klines = copia_de_lista(data_klines)[-1*last_n:-1]

    maximo = -np.Infinity
    
    for fila in klines:
        valor = high_of_candle(fila)
        if (valor > maximo): maximo = valor
        
    return maximo

def SuperaTecho(data_klines, precio, last_n):
    maximo = Techo(data_klines, last_n)
    delta = 100*(precio - maximo)/maximo

    return delta
    
    # if precio > maximo: return True
    # else: return False

def RecienSuperaTecho(data_klines, precio, por, last_n):
    maximo = Techo(data_klines, last_n)
    high_anterior = high_of_candle(data_klines[-2]) 
    
    if high_anterior < maximo:
        delta = 100*(precio - maximo)/maximo
        if delta > por: 
            #print(delta)
            return True
        else: return False
    else:
        return False
    
def TechoEnLastN(data_klines, techo, last_n, imprimir):
    
    for i in range(2, last_n + 2):
        if high_of_candle(data_klines[-i]) != techo: 
            pass
        else: 
            if imprimir: print(str(i-1))
            return True
    
    return False

def PisoEnLastN(data_klines, piso, last_n, imprimir):
    
    for i in range(2, last_n + 2):
        if low_of_candle(data_klines[-i]) != piso: 
            pass
        else: 
            if imprimir: print(str(i-1))
            return True
    
    return False
        

def Maxima_pendiente(data, muestreo, last_n = None):
    
    if last_n is None: last_n = len(data)
    
    datos = copia_de_lista(data)[-1*last_n:]
    
    m_max=-1*np.Infinity
    presente = datos[-1]
    
    init_index = len(datos) - last_n
    final_index = len(datos) - 1
    
    for i in range(init_index,final_index+1):
        pasado = datos[i]
        p = round(100*(presente-pasado)/pasado,2)
        delta_t = ((len(datos)-1-i)*muestreo) # en minutos
        if delta_t != 0:
            m = p/delta_t
            if m > m_max: m_max = m
            
    return m_max

def linea_de_tendencia(data, last_n = None):
    
    X = []
    
    if last_n is None: last_n = len(data)
    
    Y = data[-1*last_n:]
    
    for i in range(len(Y)): X.append(i)
    
    coefs = np.polyfit(X, Y, 1)
    
    resp = []
    
    for x in X: resp.append( coefs[0]*x + coefs[1] )
        
    return resp

def tendencia_porcentual(data, last_n = None):
    linea = linea_de_tendencia(data, last_n)
    p = 100*(linea[-1] - linea[0])/linea[0]
    
    return p

def MA_en_orden_alza(ma_corto,ma_medio,ma_largo,gap=1.002):
    """
    Indica si los Moving Averages están en orden de alza
    gap % >= 1
    
    """
           
    if (ma_corto[-1] > ma_medio[-1]*gap) and (ma_medio[-1] > ma_largo[-1]*gap): resp = True
    else: resp = False
            
    
    return resp
    

def IndicadorTendenciaPrecio(data, muestreo, last_n=None):
    """
    Indica si un activo está en comportamiento creciente (primera derivada)
    en una escala ponderada de 0 a 100
    Si el activo tiene un crecimiento promedio de 0.05% por minuto, I=100
    
    """
    if last_n is None:
        last_n = len(data)
    
    precios = copia_de_lista(data)[-1*last_n:]
    
    tend = tendencia(precios, muestreo, last_n, Nderivada='primera', average='exponencial')

    #Mapeo
    
    r = tend*2000
        
    return round(r,1)


def IndicadorMAenAlza(ma_corto,ma_medio,ma_largo,gap=1.002):
    """
    Indica si los Moving Averages están en orden de alza
    gap % >= 1
    En caso afirmativo I = 100
    """
    
    resp = 0
       
    if ma_corto[-1] > ma_medio[-1]*gap: resp+=50
    if ma_medio[-1] > ma_largo[-1]*gap: resp+=50
    
    return resp

def IndicadorDeltaPrecioVWAP(data, VWAP, muestreo, s_aceptable=4, last_n=None):
    """
    Indica la separación del precio respecto del VWAP
    Mayor puntaje para separación positiva pequeña 
    y separación con tendencia creciente
    
    s_aceptable es un porcentaje. Si la separación actual es positiva y menor o igual que s_aceptable
    el puntaje aumenta en +50
    
    si la tendencia es a que la separación aumenta, el puntaje aumenta en +50
    
    """
    if last_n is None:
        last_n = len(VWAP)
    
    data_2 = copia_de_lista(data)[-1*last_n:]
    VWAP_2 = copia_de_lista(VWAP)[-1*last_n:]
    
    sep = separaciones(data_2, VWAP_2)
    
    tend = tendencia(sep, muestreo, last_n)
    
    s = 100*(data_2[-1] - VWAP_2[-1])/VWAP_2[-1]
    # print(s)
    # print(tend)
    r = 0
    
    if (s > 0) and (s <= s_aceptable): r+=50
    if (s > 0) and (tend > 0) : r+=50
                
    return r   
    
    
    
    
    
    # vwap = VWAP(data_klines, len(data_klines))
    
    # deltas = []
    
    # for i in range(len(vwap)):
    #     deltas.append(float(data_klines[i][4])-vwap[i])
    
    # d = derivada_proporcional(deltas,muestreo)
    
    # init_index = len(d) - last_n
    # final_index = len(d) - 1
    
    # p = ExponentialAverage(d,init_index,final_index)[-1]
    
    # return p
    
def IndicadorTendenciaVWAP(VWAP, muestreo, last_n=None):
    """
    Indica si el VWAP está en comportamiento creciente (primera derivada)
    en una escala ponderada de 0 a 100
    Si tiene un crecimiento promedio de 0.1% por minuto, I=100
    
    """

    if last_n is None: last_n = len(VWAP)

    
    Avg = copia_de_lista(VWAP)[-1*last_n:]
    
    
    tend = tendencia(Avg, muestreo, last_n, Nderivada='primera', average='exponencial')
    #print(tend)
    #Mapeo
    
    r = tend*1000
        
    return round(r,1)

def IndicadoresTendenciasAverages(Avg_corto, Avg_medio, Avg_largo, muestreo, last_n=None):
    """
    Indica si los averages están en comportamiento creciente (primera derivada)
    en una escala ponderada de 0 a 100
    Si tienen un crecimiento promedio de 0.05% por minuto, I=100
    
    """
    
    if last_n is None:
        last_nc = len(Avg_corto)
        last_nm = len(Avg_medio)
        last_nl = len(Avg_largo)
    else:
        last_nc = last_n
        last_nm = last_n
        last_nl = last_n
        
    
    r_corto = tendencia(Avg_corto, muestreo, last_nc, Nderivada='primera', average='exponencial')*2000        
    
    r_medio = tendencia(Avg_medio, muestreo, last_nm, Nderivada='primera', average='exponencial')*2000
    
    r_largo = tendencia(Avg_largo, muestreo, last_nl, Nderivada='primera', average='exponencial')*2000
    
    return r_corto, r_medio, r_largo


def IndicadoresTendenciasTendenciasAverages(Avg_corto, Avg_medio, Avg_largo, muestreo, last_n=None):
    """
    Indica si los averages están en comportamiento cóncavo (segunda derivada)
    en una escala ponderada de 0 a 100
    
    """
    
    if last_n is None:
        last_nc = len(Avg_corto)
        last_nm = len(Avg_medio)
        last_nl = len(Avg_largo)
    else:
        last_nc = last_n
        last_nm = last_n
        last_nl = last_n
    
    r_corto = tendencia(Avg_corto, muestreo, last_nc, Nderivada='segunda', average='exponencial')*2        
    
    r_medio = tendencia(Avg_medio, muestreo, last_nm, Nderivada='segunda', average='exponencial')*2
    
    r_largo = tendencia(Avg_largo, muestreo, last_nl, Nderivada='segunda', average='exponencial')*2
    
    return r_corto, r_medio, r_largo


# def IndicadorMACD(data_klines,muestreo,last_n=None,fastperiod=12,slowperiod=26,signalperiod=9):
#     """
#     Indica si el MACD están en comportamiento creciente (primera derivada)
#     y si es positivo actuamente
#     en una escala ponderada de 0 a 100
    
#     """
    
#     MACD = MACD_hist(data_klines,fastperiod,slowperiod,signalperiod)
    
#     d = derivada_proporcional(MACD,muestreo)
#     d2 = derivada_proporcional(d,muestreo)
    
#     if last_n is not None:
#         init_index = len(d) - last_n
#         final_index = len(d) - 1 
#     else:
#         init_index = 0
#         final_index = len(d) - 1
    
#     p = ExponentialAverage(d,init_index,final_index)[-1]
#     p2 = ExponentialAverage(d2,init_index,final_index)[-1]
#     # previo = suma_previa(MACD,-2)
#     # actual = float(data_klines[-1][4])
#     # #float(data_klines[-1][4])
    
#     # if p > 0 :
#     #     if p > 0:
#     #         r = p + p2
#     #     else:
#     #         r = p
#     # else:
#     #     r = p
        
#     return 1000*d[-2]*MACD[-2]/float(data_klines[-1][4])
    
# def minimo_positivo(array):
#     minimo = -1
#     for elemento in array:
#         if elemento > 0 : 
#             if elemento < minimo : minimo = elemento
        
#     return minimo

# def suma_previa(array,index):
#     """
#     index es negativo
#     """
    
#     suma=0
#     final = len(array) + index
#     for i in range(0,final+1):
#         suma+=array[i]
        
#     return suma
    
def Indicador_Pendiente(datos, muestreo, last_n=None):
    """
    Indica cuál es la máxima pendiente de crecimiento alcanzada (%/min)
    en los últimos n periodos
    
    si la pendiente es de 0.067%/min retorna un puntaje de 100
    
    """
    
    pendiente = Maxima_pendiente(datos, muestreo, last_n)
    
    return 1493 * pendiente



def IndicadorTendenciaDeltas(datos, referencia, muestreo, last_n=None):
    """
    Indica la tendencia (primera derivada) de las diferencias 
    entre dos listas de datos.
    
    si la tendencia es a que la separación aumenta, 
    y el ratio es de 100%/min, se obtiene un puntaje de 100
    
    """
    if last_n is None:
        last_n = len(referencia)
    
    data = copia_de_lista(datos)[-1*last_n:]
    ref = copia_de_lista(referencia)[-1*last_n:]
    
    sep = separaciones(data, ref)
    
    tend = tendencia(sep, muestreo, last_n)
                    
    return tend


def IndicadorAvcortoAvmedio(ma_corto,ma_medio,gap=1.002):
    """
    Indica si los Moving Averages están en orden de alza
    gap % >= 1
    En caso afirmativo I = 100
    """
    
    resp = 0
       
    if ma_corto[-1] > ma_medio[-1]*gap: resp+=100
    
    return resp
    

def IndicadorAj(data_klines,muestreo,
                npc,npm,npl,npv,
                last_n_precio = None,
                last_n_vwap = None,
                last_n_avgs = None,
                last_n_pendiente = None,
                last_n_deltas = None,
                valor_de_vela = 'close',
                p_tendencia_precio = 1, #15
                p_ma_alza = 1, #10
                p_delta_precio_vwap = 1, #1
                p_tendencia_vwap = 1,
                p_tendencia_avg_corto = 1, #10
                p_tendencia_avg_medio = 1, #2
                p_tendencia_avg_largo = 1, #2
                p_tendencia_2_avg_corto = 1,
                p_tendencia_2_avg_medio = 1,
                p_tendencia_2_avg_largo = 1,
                p_pendiente = 1,
                p_deltas = 1,
                p_av_corto_av_medio = 1):
    """
    Indica qué tan conveniente es una moneda para hacerle scalping
    
    last_n es None o es un valor menor o igual al np más pequeño
    
    """
    
    data = data_klines_to_data(data_klines,valor_de_vela)
    
    MA_corto = EMA(data_klines,npc)
    MA_medio = EMA(data_klines,npm)
    MA_largo = EMA(data_klines,npl)
    
    vwap = VWAP(data_klines, npv)
    
    if last_n_precio is None: last_n_precio = len(data)
    if last_n_vwap is None: last_n_vwap = len(vwap)
    if last_n_pendiente is None: last_n_pendiente = len(data)
    if last_n_deltas is None: last_n_deltas = len(data)


    I_tendencia_precio = IndicadorTendenciaPrecio(data, muestreo, last_n_precio)
    I_ma_alza = IndicadorMAenAlza(MA_corto, MA_medio, MA_largo, gap=0)
    I_delta_precio_vwap = IndicadorDeltaPrecioVWAP(data, vwap, muestreo, s_aceptable=4, last_n = last_n_vwap)
    I_tendencia_vwap = IndicadorTendenciaVWAP(vwap, muestreo, last_n_vwap)
    I_tendencia_avg_corto, I_tendencia_avg_medio, I_tendencia_avg_largo = IndicadoresTendenciasAverages(MA_corto, 
                                                                                                        MA_medio, 
                                                                                                        MA_largo, 
                                                                                                        muestreo, 
                                                                                                        last_n_avgs)
    I_tendencia_2_avg_corto, I_tendencia_2_avg_medio, I_tendencia_2_avg_largo = IndicadoresTendenciasTendenciasAverages(MA_corto, 
                                                                                                                        MA_medio, 
                                                                                                                        MA_largo, 
                                                                                                                        muestreo, 
                                                                                                                        last_n_avgs)
    I_pendiente = Indicador_Pendiente(data, muestreo, last_n_pendiente)
    I_deltas = IndicadorTendenciaDeltas(data, MA_corto, muestreo, last_n_deltas)
    I_av_corto_av_medio = IndicadorAvcortoAvmedio(MA_corto, MA_medio, gap=1.001)
    
    I_Aj = 0
    I_Aj += I_tendencia_precio*p_tendencia_precio
    I_Aj += I_ma_alza*p_ma_alza
    I_Aj += I_delta_precio_vwap*p_delta_precio_vwap
    I_Aj += I_tendencia_vwap*p_tendencia_vwap
    I_Aj += I_tendencia_avg_corto*p_tendencia_avg_corto
    I_Aj += I_tendencia_avg_medio*p_tendencia_avg_medio
    I_Aj += I_tendencia_avg_largo*p_tendencia_avg_largo
    I_Aj += I_tendencia_2_avg_corto*p_tendencia_2_avg_corto
    I_Aj += I_tendencia_2_avg_medio*p_tendencia_2_avg_medio
    I_Aj += I_tendencia_2_avg_largo*p_tendencia_2_avg_largo
    I_Aj += I_pendiente*p_pendiente
    I_Aj += I_deltas*p_deltas
    I_Aj += I_av_corto_av_medio*p_av_corto_av_medio
    
    return I_Aj

def IndicadorTendenciaAVlargo(data, muestreo, last_n=None):
    """
    Indica si el average largo está en comportamiento creciente (primera derivada)
    en una escala ponderada
    Si el average tiene un crecimiento promedio de 0.001% por minuto, I=100
    
    """
    if last_n is None: last_n = len(data)
    
    avg = copia_de_lista(data)[-1*last_n:]
    
    tend = tendencia(avg, muestreo, last_n, Nderivada='primera', average='exponencial')

    #Mapeo
    
    r = tend*1e5
    
    # if tend >= 0 : r = 100
    # else: r = -100
    
    return round(r,1)

def IndicadorTendenciaAVmedio(data, muestreo, last_n=None):
    """
    Indica si el average medio está en comportamiento creciente (primera derivada)
    en una escala ponderada
    Si el average tiene un crecimiento promedio de 0.004% por minuto, I=100
    
    """
    if last_n is None: last_n = len(data)
    
    avg = copia_de_lista(data)[-1*last_n:]
    
    tend = tendencia(avg, muestreo, last_n, Nderivada='primera', average='exponencial')

    #Mapeo
    
    r = tend*2.5e4
    
    # if tend >= 0 : r = 100
    # else: r = -100
        
    return round(r,1)

def IndicadorTendenciaAVcorto(data, muestreo, last_n=None):
    """
    Indica si el average corto está en comportamiento creciente (primera derivada)
    en una escala ponderada
    Si el average tiene un crecimiento promedio de 0.01% por minuto, I=100
    
    """
    if last_n is None: last_n = len(data)
    
    avg = copia_de_lista(data)[-1*last_n:]
    
    tend = tendencia(avg, muestreo, last_n, Nderivada='primera', average='exponencial')

    #Mapeo
    
    r = tend*1e4
        
    return round(r,1)

def IndicadorTecho(data_klines, tipo_techo, last_n):
    """
    Indica si se superó el techo en las últimas n velas
    True 100 pts
    False -100 pts
    
    """
    
    
    techo = Techo(data_klines, tipo_techo, last_n=None)
    actual = float(data_klines[-1][4])
    
    if actual > techo : return 100
    else: return -100
    
def IndicadorDeltaPrecioAv(precio, av, limite):
    """
    Indica qué tanta separación tiene el precio
    respecto de un average.
    
    si delta < = 0 : puntaje = 0
    si delta = limite/2 : puntaje = puntaje_max
    si delta = limite : puntaje = 0
    si delta > limite : puntaje negativo
    
    """
    
    puntaje_max = 100
    
    delta = 100*(precio - av)/av
    
    if delta <= 0: 
        r = 0
    elif delta > 0:
        r = -(((2*math.sqrt(puntaje_max))/limite)**2)*(delta)*(delta - limite)
    
    return r

def IndicadorCruce(data, referencia, max_n_velas):
    """
    Indica qué tan reciente ocurrió el cruce de data a referencia,
    para estar ahora por encima de ésta. 
    Funciona sólo si actualmente data está por encima de la referencia
    
    si el cruce ocurrió en las últimas max_n_velas, puntaje = 100
    mientras más reciente, mayor puntaje.
    
    """
    c = -1
    
    if data[c] > referencia[c]:
        while (data[c] > referencia[c]) and (c < -len(referencia) ): c -= 1
        c+=1
        
        r = (-800/max_n_velas)*(abs(c))+900
    
    else:
        r = 0
        
    return r
    

def IndicadorLineaTendenciaVWAP(data, muestreo, last_n = None):
    
    if last_n is None: last_n = len(data)
    
    vwap = copia_de_lista(data)[-1*last_n:]
    
    linea_tendencia_vwap = linea_de_tendencia(vwap)
    delta = 100*(linea_tendencia_vwap[-1] - linea_tendencia_vwap[0])/linea_tendencia_vwap[0] # %/min
    pendiente_linea = delta/(len(linea_tendencia_vwap)*muestreo) # %/min
    
    return pendiente_linea*1e4

def DeltaUnder(vwap,precio):
    """
    5% por debajo es puntaje de 100
    """
    
    delta = 100*(vwap - precio)/precio
    
    return delta*20




def cruce_reciente(data_klines, ref):
    
    if data_klines[-1][4] > ref[-1]: pass
    else: return False
    
    if data_klines[-2][1] < ref[-2]: pass
    else: return False
    
    return True


# def Indicador_Aj(data_klines,muestreo,
#                 npc = 5,
#                 npm = 60,
#                 npl = 100,
#                 npv = 4,
#                 last_n_corto = None,
#                 last_n_medio = None,
#                 last_n_largo = None,
#                 last_n_techo = None,
#                 last_n_cruce = 8,
#                 p_tendencia_av_corto = 1, 
#                 p_tendencia_av_medio = 0, 
#                 p_tendencia_av_largo = 0,
#                 p_techo = 0,
#                 p_delta_precio = 0,
#                 p_cruce = 0,
#                 p_tendencia_vwap = 1,
#                 p_delta_under = 1):
#     """
#     Indica qué tan conveniente es una moneda para hacerle scalping
    
#     """
    
#     data = data_klines_to_data(data_klines)
    
#     MA_corto = SMA(data_klines,npc)
#     # MA_medio = SMA(data_klines,npm)
#     # MA_largo = SMA(data_klines,npl)
    
#     vwap = VWAP(data_klines, npv)
    
#     if last_n_corto is None: last_n_corto = npc
#     if last_n_medio is None: last_n_medio = npm
#     if last_n_largo is None: last_n_largo = npl
    
#     I_tendencia_av_corto = IndicadorTendenciaAVcorto(MA_corto, muestreo, last_n_corto)
#     # I_tendencia_av_medio = IndicadorTendenciaAVmedio(MA_medio, muestreo, last_n_medio)
#     # I_tendencia_av_largo = IndicadorTendenciaAVlargo(MA_largo, muestreo, last_n_largo)
#     # I_techo = IndicadorTecho(data_klines, 'close', last_n_techo)
#     # I_delta_precio = IndicadorDeltaPrecioAv(data[-1], MA_medio[-1], limite=1.5)
#     # I_cruce = IndicadorCruce(data, MA_medio, last_n_cruce)
#     I_tendencia_vwap = IndicadorLineaTendenciaVWAP(vwap, muestreo)
#     I_delta_under = DeltaUnder(vwap[-1], data[-1])
    
#     # I_Aj = 0
#     # I_Aj += I_tendencia_av_corto*p_tendencia_av_corto
#     # I_Aj += I_tendencia_av_medio*p_tendencia_av_medio
#     # I_Aj += I_tendencia_av_largo*p_tendencia_av_largo
#     # I_Aj += I_techo*p_techo
#     # I_Aj += I_delta_precio*p_delta_precio
#     # I_Aj += I_cruce*p_cruce
#     # I_Aj += I_tendencia_vwap*p_tendencia_vwap
#     # I_Aj += I_gravedad*p_gravedad
    
    
#     I_Aj = 0
#     if (I_tendencia_vwap > 0) and (I_delta_under > 0): 
#         I_Aj += I_tendencia_vwap*p_tendencia_vwap
#         I_Aj += I_delta_under*p_delta_under
#         I_Aj += I_tendencia_av_corto*p_tendencia_av_corto
           
#     return I_Aj
    


def IndicadorTendenciaDominante(data_klines, precio, muestreo,
                                npc = 5,
                                npm = 30,
                                npl = 100,
                                last_n_techo = 25,
                                p_tendencia_ma_corto = 1,
                                p_tendencia_ma_medio = 1,
                                p_tendencia_ma_largo = 1,
                                p_techo = 1):
     
    MA_largo = SMA(data_klines, npl)
    MA_medio = SMA(data_klines, npm)
    MA_corto = SMA(data_klines, npc)
        
    I_tendencia_ma_largo = IndicadorTendenciaAVlargo(MA_largo, muestreo, last_n = npl)
    I_tendencia_ma_medio = IndicadorTendenciaAVmedio(MA_medio, muestreo, last_n = npm)
    # I_tendencia_ma_corto = IndicadorTendenciaAVcorto(MA_corto, muestreo, last_n = 3)
    
    precio = float(data_klines[-1][4])
    
    I_techo = RecienSuperaTecho(data_klines, precio, por = 0.2, last_n = last_n_techo)
    
    
    I_Aj = 0
    
    
    if pasa_prueba_volumen(data_klines, vol_min = 25e3, last_n = None): pass
    else: return 0
    
    if (MA_corto[-1] > MA_medio[-1]) and (MA_medio[-1] > MA_largo[-1]): pass
    else: return 0
        
    if I_tendencia_ma_largo > 0: pass # 100
    else: return 0
    
    if I_tendencia_ma_medio > 0: pass # 100
    else: return 0
    
    if precio > MA_medio[-1]: pass
    else: return 0
    
    if I_techo : pass # 0.02
    else: return 0
    
    # if I_tendencia_ma_corto > 0: pass # 100
    # else: return 0
    
    I_Aj += I_tendencia_ma_largo*p_tendencia_ma_largo
    I_Aj += I_tendencia_ma_medio*p_tendencia_ma_medio
    # I_Aj += I_techo*p_techo
    # I_Aj += I_tendencia_ma_corto*p_tendencia_ma_corto
    
    return I_Aj


    

def BSS(order_book, precio_actual, filtro=0.2, modo='ambos sentidos'): # Buy Sell Spread
    """
    modo: por encima del precio actual, ambos sentidos
    filtro: % máximo aceptable de la desviación del precio de una orden
            respecto del precio actual
    
    """
    
    """
    Formato Order Book:
        
        {
        'lastUpdateId': int,
        'bids': [
                    [63600.09000000, 0.18030000], # price, quantity
                    [63520.00000000, 0.5030000], # price, quantity
                    ...
                ],
        'asks': [
                    [63552.54000000, 0.00079000], # price, quantity
                    [64000.11000000, 0.01000000], # price, quantity
                    ...
                ]
        }
    
    """
    
    compras = 0
    
    for fila in order_book['bids']: 
        precio = fila[0]
        cantidad = fila[1]
        delta = 100*(precio - precio_actual)/precio_actual
        
        if modo == 'por encima del precio actual':
            if (delta > 0) and (delta <= filtro): compras += precio*cantidad
                
        elif modo == 'ambos sentidos':
            if abs(delta) <= filtro: compras += precio*cantidad
            
            
    ventas = 0
    
    for fila in order_book['asks']: 
        precio = fila[0]
        cantidad = fila[1]
        delta = 100*(precio - precio_actual)/precio_actual
        
        if modo == 'por encima del precio actual':
            if (delta > 0) and (delta <= filtro): ventas += precio*cantidad
                
        elif modo == 'ambos sentidos':
            if abs(delta) <= filtro: ventas += precio*cantidad
            
    if ventas != 0:
        pass
    else:
        precio_venta_bajo = order_book['asks'][0][0]
        cantidad = order_book['asks'][0][1]
        ventas = precio_venta_bajo*cantidad
        
    return 100*(compras - ventas)/ventas
    

def BAS(order_book, precio_actual, filtro): # Bid Ask Spread
    """
    Formato Order Book:
        
        {
        'lastUpdateId': int,
        'bids': [
                    [63600.09000000, 0.18030000], # price, quantity
                    [62520.00000000, 0.5030000], # price, quantity
                    ...
                ],
        'asks': [
                    [63552.54000000, 0.00079000], # price, quantity
                    [64000.11000000, 0.01000000], # price, quantity
                    ...
                ]
        }
    
    """
    
    filtro = filtro/100
    
    techo = precio_actual*(1 + filtro)
    piso = precio_actual*(1 - filtro)
    
    max_bid_price = order_book['bids'][-1][0]
    for fila in order_book['bids']:
        precio = fila[0]
        if (precio > max_bid_price) and (precio <= techo): max_bid_price = precio
        
    min_bid_price = order_book['asks'][-1][0]
    for fila in order_book['asks']:
        precio = fila[0]
        if (precio < min_bid_price) and (precio >= piso): min_bid_price = precio
        
    return 100*(max_bid_price - min_bid_price)/min_bid_price


def PCC(order_book, precio_actual, filtro, modo): # Potencial de Crecimiento debido a Compras
    """
    modo: por encima del precio actual, ambos sentidos
    filtro: % máximo aceptable de la desviación del precio de una orden
            respecto del precio actual
    
    """
    
    """
    Formato Order Book:
        
        {
        'lastUpdateId': int,
        'bids': [
                    [63600.09000000, 0.18030000], # price, quantity
                    [63520.00000000, 0.5030000], # price, quantity
                    ...
                ],
        'asks': [
                    [63552.54000000, 0.00079000], # price, quantity
                    [64000.11000000, 0.01000000], # price, quantity
                    ...
                ]
        }
    
    """
    
    compras = 0
    
    for fila in order_book['bids']: 
        precio = fila[0]
        cantidad = fila[1]
        delta = 100*(precio - precio_actual)/precio_actual
        
        if modo == 'por encima del precio actual':
            if (delta > 0) and (delta <= filtro): compras += precio*cantidad
                
        elif modo == 'ambos sentidos':
            if abs(delta) <= filtro: compras += precio*cantidad
            
            
    ventas = 0
    
    for fila in order_book['asks']: 
        precio = fila[0]
        cantidad = fila[1]
        delta = 100*(precio - precio_actual)/precio_actual
        
        if modo == 'por encima del precio actual':
            if (delta > 0) and (delta <= filtro): ventas += precio*cantidad
                
        elif modo == 'ambos sentidos':
            if abs(delta) <= filtro: ventas += precio*cantidad
            
    p = compras - ventas
            
    return 100*(p - precio_actual)/precio_actual



def IndicadorCombinado(data_klines, order_book, precio_actual,
                       muestreo,
                       npv,
                       p_tendencia_vwap = 1,
                       p_delta_under = 1,
                       p_last_trend_vwap = 1):

    
    data = data_klines_to_data(data_klines)
    
    vwap = VWAP(data_klines, npv)
        
    I_tendencia_vwap = IndicadorLineaTendenciaVWAP(vwap, muestreo)
    #I_delta_under = DeltaUnder(vwap[-1], data[-1])
    
    #I_last_trend_vwap = tendencia(vwap, muestreo, last_n = npv, Nderivada='primera', average='exponencial')*2.5e4
    
    bss = BSS(order_book, precio_actual, filtro = 5, modo = 'ambos sentidos') # por encima del precio actual, ambos sentidos # 0.2
    
    #bas = BAS(order_book, precio_actual, filtro = 1)
    
    # print(bss)
    # return bss
    
    I_Aj = 0
    
    if pasa_prueba_volumen(data_klines, vol_min = 25e3, last_n = None): pass
    else: return 0
    
    if I_tendencia_vwap > 0.05: I_Aj += I_tendencia_vwap*p_tendencia_vwap
    else: return 0
    
    # if I_delta_under > 0 : I_Aj += I_delta_under*p_delta_under
    # else: return 0
    
    # if I_last_trend_vwap > 0.07: I_Aj += I_last_trend_vwap*p_last_trend_vwap
    # else: return 0
    
    if bss > 200: I_Aj += bss*5
    else: return 0
        
    
    #if SuperaTecho(data_klines, last_n = 6): I_Aj += 200
    # else: return 0
    
    
    return I_Aj
    

### Funciones seleccionadas

def qty_filter(cantidad, symbol_info):
    
    decimales = int(symbol_info['baseAssetPrecision'])
    
    for filtro in symbol_info['filters']:
        if filtro['filterType']=='MARKET_LOT_SIZE':
            step = round(float(filtro['stepSize']),decimales)
            break
                    
    acum = 0
    
    while acum <= cantidad: acum += step
    
    acum -= step
    
    acum = round(acum,decimales)
    
    return acum

def pendiente(data):
    
    X = []
    
    Y = data
    
    for i in range(len(Y)): X.append(i)
    
    coefs = np.polyfit(X, Y, 1)
    
    return coefs[0]

def SimpleAverage(data,init,final):
    last_n = final - init + 1
    
    r = talib.SMA(np.array(data), timeperiod=last_n)
    
    return r.tolist()


def pasa_prueba_volumen(data_klines, vol_min, inversion, last_n = None):
        
    if (last_n is None) or (last_n > len(data_klines)): last_n = len(data_klines)

    data_klines = copia_de_lista(data_klines)[-1*last_n:]
    
    vols = data_klines_to_data(data_klines, valor_de_vela='quote volume')
    # vol_avg = SimpleAverage(vols,0,len(vols)-1)[-1]
    
    acum = 0
    
    for v in vols: acum += v
    
    vol_avg = acum/len(vols)
    
    if vol_avg <= 0: return False
    
    proporcion = 100*(inversion/vol_avg)
        
    if proporcion < 1: return True
    else: return False
    
    # if vol_avg >= vol_min: 
        
    #     return True
        
    #     proporcion = 100*(inversion/vol_avg)
        
    #     if proporcion < 1: return True
    #     else: return False
        
    # else: 
    #     return False
    
    
def insertar_elemento_final(lista, elemento_nuevo):
    
    for i in range(len(lista)-1): lista[i] = lista[i+1]
        
    lista[-1] = elemento_nuevo
    
    return lista

def mean_percent_candle(klines, last_n = None):
    
    if last_n is None: last_n = len(klines)
    
    data_klines = klines[-1*last_n:]
    
    c = 0
    
    acum = 0
    
    for fila in data_klines:
        delta = 100*(fila[2] - fila[3])/fila[3]
        acum += delta
        c += 1
        
    return acum/c

def abs_mean_percent_candle(klines, last_n = None):
    
    if last_n is None: last_n = len(klines)
    
    data_klines = klines[-1*last_n:]
    
    c = 0
    
    acum = 0
    
    for fila in data_klines:
        
        if fila[4] >= fila[1]: delta = 100*(fila[2] - fila[3])/fila[3] # vela verde
        if fila[4] < fila[1]: delta = 100*(fila[2] - fila[3])/fila[2] # vela roja
        
        acum += delta
        c += 1
        
    return acum/c


def percent_candle_positive(klines, last_n = None):
    
    if last_n is None: last_n = len(klines)
    
    data_klines = copia_de_lista(klines)[-1*last_n:]
    
    sum_rojas = 0
    sum_verdes = 0
        
    for fila in data_klines:
        if fila[4] >= fila[1]: sum_verdes += (fila[4] - fila[1])
        elif fila[4] < fila[1]: sum_rojas += (fila[1] - fila[4])

    if (sum_rojas + sum_verdes) == 0:
        return 0

    p = 100*(sum_verdes)/(sum_rojas + sum_verdes)
    
    return p


def send_market_buy_order(cliente, simbolo, quote_qty):
    
    try:
        
        respuesta = cliente.create_test_order(symbol =  simbolo, side = 'BUY', type =  'MARKET', quoteOrderQty =  quote_qty)
        # print(respuesta)
        
        if respuesta == {}: pass
        else: return None
        
        

        respuesta = cliente.create_order(symbol =  simbolo, side = 'BUY', type =  'MARKET', quoteOrderQty =  quote_qty)
        # print(respuesta)
        
        # if not 'status' in respuesta: return None
        # if respuesta['status'] != 'FILLED': return None
        
        return respuesta

    except:
        traceback.print_exc()
        return None
 

def send_market_sell_order(cliente, simbolo, base_qty):
    
    try:
                
        respuesta = None
        
        respuesta = cliente.order_market_sell(symbol =  simbolo, quantity =  base_qty)
        
        return respuesta

    except:
        traceback.print_exc()
        return None
    
       
def send_oco_sell_order(cliente, simbolo, base_qty, precio_profit, precio_stop, precio_limit):
    
    try:
        
        respuesta = cliente.create_test_order(symbol =  simbolo, side = 'SELL', type =  'MARKET', quantity =  base_qty)
        
        if respuesta == {}: pass
        else: return None
        
        respuesta = cliente.create_oco_order(symbol = simbolo, side = 'SELL', quantity = base_qty,
                                             price = precio_profit, stopPrice = precio_stop, stopLimitPrice = precio_limit,
                                             stopLimitTimeInForce = 'GTC')
        
        return respuesta

    except:
        traceback.print_exc()
        return None


def IndicadorGravedad(data_klines, inversion, vol_min, muestreo,
                      npv = 40,
                      p_tendencia_vwap = 1,
                      p_delta_under = 1):
       
    precio = data_klines[-1][4]
    
    data = data_klines_to_data(data_klines)
    
    vwap = VWAP(data_klines, npv)
        
    I_tendencia_vwap = IndicadorLineaTendenciaVWAP(vwap, muestreo, npv)
    I_delta_under = DeltaUnder(vwap[-1], data[-1])
    
    I_Aj = 1
        
    if pasa_prueba_volumen(data_klines, vol_min, inversion, last_n = None): pass
    else: return 0
    
    if I_tendencia_vwap > 0 : pass #100
    else: return 0

    if I_delta_under > 0 : pass
    else: return 0
                
    I_Aj += I_tendencia_vwap*p_tendencia_vwap
    I_Aj += I_delta_under*p_delta_under
    I_Aj *= mean_percent_candle(data_klines, last_n = None)
        
    return I_Aj


def IndicadorCercaDeSoporte(data_klines, inversion, vol_min,
                            last_n_piso = 12,
                            exclude_last_n_piso = 4):
    
    I_Aj = 1

    if pasa_prueba_volumen(data_klines, vol_min, inversion, last_n = None): pass
    else: return 0
    
    precio = data_klines[-1][4]
        
    piso = Piso(data_klines, last_n = last_n_piso)
    piso_en_last_N = PisoEnLastN(data_klines, piso, exclude_last_n_piso, False)
    
    if not piso_en_last_N: pass
    else: return 0
    
    distancia = 100*(precio - piso)/piso
    
    if distancia > 0: pass
    else: return 0
       
    I_Aj += 10/distancia
    
    return I_Aj


def IndicadorRupturaResistencia(data_klines, inversion, vol_min,
                                last_n_techo = 12,
                                exclude_last_n_techo = 4):
    
    I_Aj = 1

    if pasa_prueba_volumen(data_klines, vol_min, inversion, last_n = None): pass
    else: return 0
    
    precio = data_klines[-1][4]
    
    if SuperaTecho(data_klines, precio, last_n_techo) > 0: pass #0.07 #0.1 
    else: return 0
    
    techo = Techo(data_klines, last_n = last_n_techo)
    techo_en_last_N = TechoEnLastN(data_klines, techo, exclude_last_n_techo, False)
    
    if not techo_en_last_N: pass
    else: return 0
       
    I_Aj += mean_percent_candle(data_klines, last_n = None)
    
    return I_Aj


def IndicadorLowRSI(data_klines, inversion, vol_min, n):
        
    I_Aj = 1

    if pasa_prueba_volumen(data_klines, vol_min, inversion, last_n = None): pass
    else: return 0

    rsi = RSI(data_klines, last_n_intervals = n)
            
    I_Aj += 100 - rsi[-1]
       
    return I_Aj


def IndicadorVolatilidad(data_klines, inversion, vol_min, n):
    
    I_Aj = 1

    if pasa_prueba_volumen(data_klines, vol_min, inversion, last_n = None): pass
    else: return 0
    
    p = percent_candle_positive(data_klines, last_n = 20)
    
    if p > 50: pass
    else: return 0
    
    I_Aj += mean_percent_candle(data_klines, last_n = n)
       
    return I_Aj

def IndicadorReboteRSI(data_klines, inversion, vol_min, n):
    
    I_Aj = 1

    if pasa_prueba_volumen(data_klines, vol_min, inversion, last_n = None): pass
    else: return 0

    rsi = RSI(data_klines, last_n_intervals = n)[-n+2:]
            
    menor = np.Infinity
    
    for item in rsi:
        if item < menor: menor = item
    
    if (rsi[-2] == menor) and ((rsi[-1] - rsi[-2]) > 0) : pass # and (rsi[-1] < 50)
    else: return 0
        
    I_Aj += (rsi[-1] - rsi[-2])*10
       
    return I_Aj




def IndicadorAlfa(data_klines, inversion, vol_min, nprsi, npbb):
        
    I_Aj = 1

    if pasa_prueba_volumen(data_klines, vol_min, inversion, last_n = None): pass
    else: return 0

    rsi = RSI(data_klines, last_n_intervals = nprsi)[-nprsi+2:]
            
    if rsi[-1] < 30: pass 
    else: return 0
    
    closes = data_klines_to_data(data_klines, valor_de_vela = 'close')
    
    up, mid, low = talib.BBANDS(np.array(closes), timeperiod = npbb)
    
    if (up[-1] - low[-1]) != 0: pass
    else: return 0
    
    bbp = (closes[-1] - low[-1])/(up[-1] - low[-1])
    
    if bbp < 0: pass
    else: return 0
    
           
    I_Aj += mean_percent_candle(data_klines, last_n = None)
       
    return I_Aj

def IndicadorCrecimiento(data_klines, n):
    
    klines = data_klines[-1*n:]
    data = data_klines_to_data(klines, valor_de_vela = 'promedio low high')  
    p = tendencia_porcentual(data)    
    
    I_Aj = p
       
    return I_Aj

def IndicadorCaida(data_klines, n):
    
    klines = data_klines[-1*n:]
    data = data_klines_to_data(klines, valor_de_vela = 'promedio low high')  
    p = tendencia_porcentual(data)    
    
    I_Aj = -p
       
    return I_Aj


def IndicadorAmplitud(data_klines, n):
            
    I_Aj = abs_mean_percent_candle(data_klines, last_n = n)
       
    return I_Aj

def IndicadorRSIalto(data_klines, n):
        
    rsi = RSI(data_klines, last_n_intervals = n)
            
    I_Aj = rsi[-1]
       
    return I_Aj

def IndicadorRSIbajo(data_klines, n):
        
    rsi = RSI(data_klines, last_n_intervals = n)
            
    I_Aj = 100 - rsi[-1]
       
    return I_Aj

def IndicadorBollinger(data_klines, n):
        
    closes = data_klines_to_data(data_klines, valor_de_vela = 'close')
    
    up, mid, low = talib.BBANDS(np.array(closes), timeperiod = n)
    
    if (up[-1] - low[-1]) != 0: pass
    else: return 0
    
    bbp_d = abs(closes[-1] - low[-1])/(up[-1] - low[-1])
    bbp_u = abs(closes[-1] - up[-1])/(up[-1] - low[-1])

    I_Aj = 10 - min(bbp_d, bbp_u)
    
    return I_Aj 

def IndicadorEMARSI(data_klines, nt, nrsi):
    
    I_Aj = 0
    
    precio = data_klines[-1][4]
    avg = EMA(data_klines, nt)[-1]
    
    rsi = RSI(data_klines, last_n_intervals = nrsi)[-1]
    
    if precio >= avg: I_Aj = 100 - rsi
    else: I_Aj = rsi
    
    return I_Aj

def maximo_past_n(data_klines, n):
    klines = data_klines[-1*n:]
    maximo = -np.Infinity
    
    for i in range(len(klines)): #ohlc
        if klines[i][2] > maximo:
            maximo = klines[i][2]
            index = i
            
    posicion = len(klines) - index
    
    return maximo, posicion


def minimo_past_n(data_klines, n):
    klines = data_klines[-1*n:]
    minimo = np.Infinity
    
    for i in range(len(klines)): #ohlc
        if klines[i][3] < minimo:
            minimo = klines[i][3]
            index = i
            
    posicion = len(klines) - index
    
    return minimo, posicion

def IndicadorCriterioBot(data_klines, npt):
    
    min_ps = 0.05 #0.1
    max_ps = 0.3 #0.2
    past_n = 5
    exclude_pos = 2 #1 [5, 4, 3, 2, 1]
    
    klines = data_klines[-1*npt:]
    data = data_klines_to_data(klines, valor_de_vela = 'promedio low high')  
    p = tendencia_porcentual(data)
    
    if p > 0: #alcista
        maximo, posicion = maximo_past_n(data_klines, past_n)        
        superacion = 100*(data_klines[-1][4] - maximo)/maximo
        
        if (superacion >= min_ps) and (superacion <= max_ps): pass
        else: return 0
        
        if posicion > exclude_pos : pass
        else: return 0
        
        return p    
        
    elif p <= 0: #bajista
        minimo, posicion = minimo_past_n(data_klines, past_n)
        superacion = -100*(data_klines[-1][4] - minimo)/minimo
        
        if (superacion >= min_ps) and (superacion <= max_ps): pass
        else: return 0
        
        if posicion > exclude_pos : pass
        else: return 0
        
        return -p 
        
    
    
           
                
class BinanceException(Exception):
    def __init__(self, status_code, data):

        self.status_code = status_code
        if data:
            self.code = data['code']
            self.msg = data['msg']
        else:
            self.code = None
            self.msg = None
        message = f"{status_code} [{self.code}] {self.msg}"

        super().__init__(message)
        
       
class InfoVela():
    
    def __init__(self):
        self.esPiso = False
        self.esMinimo = False
        self.esMaximo = False
        self.esTecho = False
        

        
       

            
        
                
 

            
 

if __name__ == "__main__":
    
    app = PyQt5.QtWidgets.QApplication([])
    ventana_principal = VentanaPrincipal()
    ventana_principal.show()
        
    app.exec_()
    
