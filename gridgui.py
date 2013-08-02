#!/usr/bin/env python
#
#  Copyright (c) 2010 Corey Goldberg (corey@goldb.org)
#  License: GNU LGPLv3
#
#  This file is part of Multi-Mechanize | Performance Test Framework
#


"""
Multi-Mechanize Grid Controller
sample gui application for controlling multi-mechanize instances via the remote management api
"""


import socket
import ScrolledText
import Tkinter
import tkFileDialog
import xmlrpclib
import os
import time

# list of hosts:ports where multi-mechanize is listening
with open(os.path.expanduser('~/.multimech'), 'r') as f:
    text = f.read()
    NODES = text.split('\n')

#NODES = [
#    '127.0.0.1:1025',
#    '127.0.0.1:1026',
#]



class Application:
    def __init__(self, root, hosts):
        self.hosts = hosts
        self.root = root
        self.root.geometry('%dx%d%+d%+d' % (600, 400, 100, 100))
        self.root.title('Multi-Mechanize Grid Controller')

        Tkinter.Button(self.root, text='List Nodes', command=self.list_nodes, width=15,).place(x=5, y=5)
        Tkinter.Button(self.root, text='Check Tests', command=self.check_servers, width=15,).place(x=5, y=35)
        Tkinter.Button(self.root, text='Get Project Names', command=self.get_project_names, width=15).place(x=5, y=65)
        Tkinter.Button(self.root, text='Get Configs', command=self.get_configs, width=15).place(x=5, y=95)
        Tkinter.Button(self.root, text='Update Configs', command=self.update_configs, width=15).place(x=5, y=125)
        Tkinter.Button(self.root, text='Get Results', command=self.get_results, width=15).place(x=5, y=155)
        Tkinter.Button(self.root, text='Run Tests', command=self.run_tests, width=15).place(x=5, y=185)
	#Tkinter.Button(self.root, text='Stop Tests', command=self.stop_tests, width=15).place(x=5, y=215)
        self.text_box = ScrolledText.ScrolledText(self.root, width=59, height=24, font=('Helvetica', 9))
        self.text_box.place(x=162, y=5)


    def clear_window(self):
        self.text_box.delete(1.0, Tkinter.END)


    def list_nodes(self):
        self.clear_window()
        for host, port in self.hosts:
            self.text_box.insert(Tkinter.END, '%s:%s\n' % (host, port))


    def run_tests(self):
        self.clear_window()
        for host, port in self.hosts:
            server = xmlrpclib.ServerProxy('http://%s:%s' % (host, port))
            try:
                status = server.run_test()
                self.text_box.insert(Tkinter.END, '%s:%s:\n%s\n\n\n' % (host, port, status))
            except socket.error:
                self.text_box.insert(Tkinter.END, 'can not make connection to: %s:%s\n' % (host, port))

    def stop_tests(self):
	self.clear_window()
	for host, port in self.hosts:
	    server = xmlrpclib.ServerProxy('http://%s:%s' % (host, port))
            try:
                status = server.stop_test()
                self.text_box.insert(Tkinter.END, '%s:%s:\n%s\n\n\n' % (host, port, status))
            except socket.error:
                self.text_box.insert(Tkinter.END, 'can not make connection to: %s:%s\n' % (host, port))

    def get_configs(self):
        self.clear_window()
        for host, port in self.hosts:
            server = xmlrpclib.ServerProxy('http://%s:%s' % (host, port))
            try:
                config = server.get_config()
                self.text_box.insert(Tkinter.END, '%s:%s config:\n%s\n\n\n' % (host, port, config))
            except socket.error:
                self.text_box.insert(Tkinter.END, 'can not make connection to: %s:%s\n' % (host, port))


    def update_configs(self):
        self.clear_window()
        f = tkFileDialog.askopenfile(parent=self.root, initialdir='./', title='Select a Config File')
        newconfig = f.read()
        for host, port in self.hosts:
            server = xmlrpclib.ServerProxy('http://%s:%s' % (host, port))
            try:
                status = server.update_config(newconfig)
                self.text_box.insert(Tkinter.END, '%s:%s config updated:\n%s\n\n' % (host, port, status))
            except socket.error:
                self.text_box.insert(Tkinter.END, 'can not make connection to: %s:%s\n' % (host, port))


    def get_results(self):
        self.clear_window()
        save_dir = 'gridresults'
	project_dir = self.get_project_name()
        run_localtime = time.strftime('%Y.%m.%d_%H.%M.%S', time.localtime())
        results_dir = save_dir+'/'+project_dir+'/results/'+run_localtime
        self.text_box.insert(Tkinter.END, 'Writing swarm results to %s/results.csv\n' % results_dir)
        try:
            os.makedirs(results_dir)
        except OSError:
            self.text_box.insert(Tkinter.END, 'ERROR: Can not create results directory: %s\n' % results_dir)
            return

        with open(os.path.expanduser(results_dir+'/results.csv'), 'w') as f:
            for host, port in self.hosts:
                server = xmlrpclib.ServerProxy('http://%s:%s' % (host, port))
                try:
                    results = server.get_results()
                    if results.startswith("Results Not Available"):
                        self.text_box.insert(Tkinter.END, 'bee %s returned no results\n' % host)
                    else:
                        f.write(results)
                except socket.error:
                    self.text_box.insert(Tkinter.END, 'can not make connection to: %s:%s\n' % (host, port))
                    return
        self.text_box.insert(Tkinter.END, 'Writing swarm config to %s/config.cfg\n' % results_dir)
        with open(os.path.expanduser(results_dir+'/config.cfg'), 'w') as f:
	    config = server.get_config()
            f.write(config)
	try:
            os.makedirs(save_dir+'/'+project_dir+'/test_scripts')
        except OSError:
            pass

        self.text_box.insert(Tkinter.END, 'Generating graphs for swarm in %s\n' % results_dir)
        os.system('multimech-run %s -d %s -r %s' % (project_dir, save_dir, run_localtime))

    def get_project_name(self):
        for host, port in self.hosts:
            server = xmlrpclib.ServerProxy('http://%s:%s' % (host, port))
            try:
                name = server.get_project_name()
		return name
            except socket.error:
                self.text_box.insert(Tkinter.END, 'can not make connection to: %s:%s\n' % (host, port))

    def get_project_names(self):
        self.clear_window()
        for host, port in self.hosts:
            server = xmlrpclib.ServerProxy('http://%s:%s' % (host, port))
            try:
                name = server.get_project_name()
                self.text_box.insert(Tkinter.END, '%s:%s project name:\n%s\n\n' % (host, port, name))
            except socket.error:
                self.text_box.insert(Tkinter.END, 'can not make connection to: %s:%s\n' % (host, port))


    def check_servers(self):
        self.clear_window()
        for host, port in self.hosts:
            server = xmlrpclib.ServerProxy('http://%s:%s' % (host, port))
            try:
                is_running = server.check_test_running()
                self.text_box.insert(Tkinter.END, '%s:%s test running:\n%s\n\n' % (host, port, is_running))
            except socket.error:
                self.text_box.insert(Tkinter.END, 'can not make connection to: %s:%s\n' % (host, port))



def main():
    #hosts = [(host, '8335') for host in NODES]    
    hosts = []
    for host in NODES:
        if len(host) > 6:
            hosts.extend([(host, '8335')])
    root = Tkinter.Tk()
    app = Application(root, hosts)
    root.mainloop()


if __name__ == '__main__':
    main()
