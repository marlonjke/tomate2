#!/usr/bin/env python
#-*- coding:utf-8 -*-
"""
Tomate2 !!!
Versão 'melhorada' do tomate original...
A versão original pode ser encontrada aqui:
https://gitorious.org/tomate
"""

import os
import gtk
import pygtk
pygtk.require('2.0')
import pickle
import gobject
import appindicator
from datetime import timedelta
from time import time
from math import floor
gtk.gdk.threads_init()


class Pomodoro:
    """ Classe principal que instancia o indicador do ubuntu...
    """
    def __init__(self):
        self.directory = os.path.dirname(os.path.realpath(__file__)) + os.path.sep
        self.ind = appindicator.Indicator('tomate', 'tomate', appindicator.CATEGORY_APPLICATION_STATUS)
        self.ind.set_status(appindicator.STATUS_ACTIVE)
        self.ind.set_icon(self.directory + "idle.png")
        self.tempo = self.get_tempo_min()
        self.state = "idle"
        self.tick_interval = 10
        self.start_working_time = 10
        self.menu = gtk.Menu()

        self.inicio = gtk.MenuItem('Iniciar')
        self.inicio.connect('activate', self.on_inicio_clicked, None)
        self.inicio.show()
        self.menu.append(self.inicio)

        self.separator = gtk.SeparatorMenuItem()
        self.separator.show()
        self.menu.append(self.separator)

        self.conf = gtk.MenuItem('Configurações')
        self.conf.connect('activate', self.on_config_clicked, None)
        self.conf.show()
        self.menu.append(self.conf)

        self.separator = gtk.SeparatorMenuItem()
        self.separator.show()
        self.menu.append(self.separator)

        self.sair = gtk.MenuItem('Sair')
        self.sair.connect('activate', gtk.main_quit, None)
        self.menu.append(self.sair)
        self.menu.show_all()
        self.ind.set_menu(self.menu)

    def on_inicio_clicked(self, *args):
        delta = time() - self.start_working_time
        if self.state == 'idle':
            self.set_state('working')
        else:
            self.set_state('idle')

    def on_config_clicked(self, *args):
        conf = Configuracoes()

    def format_time(self, segundos):
        if segundos < 3600:
            minutos = floor(segundos/60)
            if minutos > 1:
                return '%d minutos' % minutos
            else:
                return '%d minuto' % minutos
        else:
            td = timedelta(seconds=segundos)
            return ':'.join(str(td).split(':')[:2])

    def set_state(self, state):
        old_state = self.state
        self.ind.set_icon(self.directory+state+".png")
        if state == "idle":
            delta = time() - self.start_working_time
            if old_state == "ok":
                self.inicio.get_child().set_text("Bom! Você trabalhou durante %s." % self.format_time(delta))
            elif old_state == "working":
                self.inicio.get_child().set_text("Ruim! Você trabalhou por apenas %s." % self.format_time(delta))
        else:
            if state == "working":
                self.start_working_time = time()
            delta = time() - self.start_working_time
            self.inicio.get_child().set_text("Trabalhando por %s..." % self.format_time(delta))
        self.state = state

    def update(self):
        delta = time() - self.start_working_time
        if self.state == "idle":
            pass
        else:
            self.inicio.get_child().set_text("Trabalhando por %s..." % self.format_time(delta))
            if self.state == "working":
                if delta > self.tempo * 60:
                    self.set_state("ok")
        source_id = gobject.timeout_add(self.tick_interval*1000, self.update)

    def main(self):
        source_id = gobject.timeout_add(self.tick_interval, self.update)
        gtk.main()

    def get_tempo_min(self):
        path = self.directory + "tempo.mj"
        tempo = 25
        try:
            arquivo = open(path, 'rb')
            tempo = pickle.load(arquivo)
            arquivo.close()
        except IOError as ioer:
            print "Criando arquivo com configurações de tempo necessárias"
            self.set_tempo_min(tempo)
        except pickle.PickleError as perr:
            print "Não foi possivel coletar dados do arquivo"
        finally:
            return tempo

    def set_tempo_min(self, tempo_min):
        path = self.directory + "tempo.mj"
        self.tempo = tempo_min
        try:
            arquivo = open(path, 'wb')
            pickle.dump(tempo_min, arquivo)
            arquivo.close()
        except:
            print "Não foi possível inserir dados no arquivo."


class Configuracoes:
    """Janela de configurações de tempo mínimo de trabalho (por enquanto)"""
    def __init__(self):
        self.janela = gtk.Window()
        self.janela.set_title("Configurações")
        self.janela.set_position(gtk.WIN_POS_CENTER)
        self.janela.set_border_width(15)
        self.janela.connect('destroy', self.fechar, self.janela)

        self.conteudo = gtk.VBox(False, 1)

        self.boxConf = gtk.HBox(False, 1)
        self.label = gtk.Label("Tempo mínimo (minutos): ")
        self.tempo = gtk.Entry()
        self.tempo.set_text(str(app.tempo))

        self.boxConf.pack_start(self.label, False, False, 0)
        self.boxConf.pack_end(self.tempo, False, False, 0)
        self.conteudo.pack_start(self.boxConf, False, False, 0)

        self.boxButton = gtk.HBox(False, 1)
        self.btnOk = gtk.Button("OK")
        self.btnOk.connect('clicked', self.on_ok_clicked)

        self.btnCancelar = gtk.Button("Cancelar")
        self.btnCancelar.connect('clicked', self.on_cancelar_clicked)

        self.boxButton.pack_end(self.btnOk, False, False, 0)
        self.boxButton.pack_end(self.btnCancelar, False, False, 0)

        self.conteudo.pack_start(self.boxButton, False, False, 0)

        self.janela.add(self.conteudo)
        self.janela.show_all()

    def on_ok_clicked(self, *args):
        app.set_tempo_min(int(self.tempo.get_text()))
        self.janela.hide()

    def on_cancelar_clicked(self, *args):
        self.fechar()

    def fechar(self, *args):
        self.janela.hide()

if __name__ == '__main__':
    app = Pomodoro()
    app.main()
