#!/usr/bin/python

import threading, sys, re
import wx

class MasterSelectDialog(wx.Frame):
    def __init__(self, calling_object, sema, *args, **kwargs):
        super(MasterSelectDialog, self).__init__(*args, **kwargs)
        self.calling_object = calling_object
        self.items = {}
        self.init_ui()

        self.SetSize((500, 400))
        self.SetTitle("Select MAVLink master")
        self.Centre()
        self.Show(True)
        sema.release()


    def init_ui(self):
        '''Create the widgets'''
        vbox = wx.BoxSizer(wx.VERTICAL)

        fgrid = wx.FlexGridSizer(2, 2, 5, 5)
        lbl1 = wx.StaticText(self, label="Serial interface")
        lbl2 = wx.StaticText(self, label="Detected systems and components")
        self.if_list = wx.ListBox(self, -1)
        self.id_list = wx.ListBox(self, -1)
        self.id_list.Disable()
        fgrid.AddMany([(lbl1), (lbl2), (self.if_list, 1, wx.EXPAND), (self.id_list, 1, wx.EXPAND)])
        fgrid.SetFlexibleDirection(wx.VERTICAL)
        fgrid.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_ALL)
        fgrid.AddGrowableCol(0, 0)
        fgrid.AddGrowableCol(1, 0)
        fgrid.AddGrowableRow(1, 1)
        vbox.Add(fgrid, proportion=1, flag=wx.EXPAND|wx.ALL, border=8)

        hbox_buttons = wx.BoxSizer(wx.HORIZONTAL)
        self.btn_cancel = wx.Button(self, wx.ID_CANCEL, label="Cancel")
        self.btn_ok = wx.Button(self, wx.ID_OK, label="OK")
        self.btn_ok.Disable()
        hbox_buttons.Add(self.btn_cancel)
        hbox_buttons.Add(self.btn_ok, flag=wx.LEFT, border=5)
        vbox.Add(hbox_buttons, proportion=0, flag=wx.ALIGN_RIGHT|wx.ALL, border=8)

        self.SetSizer(vbox)

        self.Bind(wx.EVT_LISTBOX, self.on_iface_selected, id=self.if_list.GetId())
        self.Bind(wx.EVT_BUTTON, self.on_exit, id=wx.ID_CANCEL)
        self.Bind(wx.EVT_BUTTON, self.on_select, id=wx.ID_OK)

    def add_item(self, iface, sys_id, comp_id):
        '''Add a new interface/id pair to the lists'''
        if iface in self.items:
            self.items[iface].append((sys_id, comp_id))
            if iface == self.if_list.GetStringSelection():
                self.populate_id_list(self.items[iface])
        else:
            self.items[iface] = [(sys_id, comp_id)]
            self.if_list.Insert(iface, 0)
        self.btn_ok.Enable()

    def add_iface(self, iface):
        '''Add an interface with no detected systems or components'''
        if iface not in self.items:
            self.items[iface] = []
            self.if_list.Insert(iface, 0)
        self.btn_ok.Enable()

    def on_iface_selected(self, e):
        '''Show the appropriate sys/comps when an interface is selected'''
        self.populate_id_list(self.items[e.GetString()])
        self.calling_object.on_selection(e.GetString(), False)
    
    def populate_id_list(self, ids):
        '''Clear the id list and refill it from the provided list'''
        self.id_list.Set(["System " + str(x[0]) + ", Component " + str(x[1]) for x in ids])
        #self.id_list.SetSelection(0)

    def on_exit(self, e):
        self.calling_object.on_selection(None, True)
        self.Close()

    def on_select(self, e):
        #ids = re.findall("\d+", self.id_list.GetStringSelection())
        #self.calling_object.on_selection(self.if_list.GetStringSelection(), int(ids[0]), int(ids[1]))
        self.calling_object.on_selection(self.if_list.GetStringSelection(), True)
        self.Close()

class MasterSelect(object):
    def __init__(self, ifaces):
        self.selection = None
        self.is_selection_made = False
        self.dialog = None
        sema = threading.Semaphore(0)
        t = threading.Thread(target=self.master_select_init, args=(sema,))
        t.start()
        sema.acquire()
        #TODO create a thread to listen on each interface to autodetect

    def master_select_init(self, sema):
        '''Create the GUI'''
        app = wx.App()
        self.dialog = MasterSelectDialog(self, sema, None)
        app.MainLoop()

    def add_item(self, iface, sys_id, comp_id):
        '''Add a detected interface/id pair to the GUI'''
        self.dialog.add_item(iface, sys_id, comp_id)

    def on_selection(self, iface, is_closed):
        '''Receive the user selection from the dialog'''
        self.selection = iface
        self.is_selection_made = is_closed

    def get_selection(self):
        '''Poll to see if a selection is made. Return False if no, or iface name/none if selected or cancelled.'''
        return self.is_selection_made and self.selection

if __name__ == '__main__':
    ms = MasterSelect([])
    ms.dialog.add_iface("Purple")
    ms.add_item("Red", 1, 1)
    ms.add_item("Red", 2, 2)
    ms.add_item("Green", 3, 3)
    ms.add_item("Blue", 4, 4)
    ms.dialog.add_iface("Red")
    while True:
        selection = ms.get_selection()
        if selection == None:
            print "Cancel"
            break
        elif selection != False:
            print selection
            break
