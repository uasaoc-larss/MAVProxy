#!/usr/bin/python

import wx

class MasterSelectDialog(wx.Frame):
    def __init__(self, *args, **kwargs):
        super(MasterSelectDialog, self).__init__(*args, **kwargs)
        self.init_ui()

        self.SetSize((500, 400))
        self.SetTitle("Select MAVLink master")
        self.Centre()
        self.Show(True)

    def init_ui(self):
        '''Create the widgets'''
        vbox = wx.BoxSizer(wx.VERTICAL)

        fgrid = wx.FlexGridSizer(2, 2, 5, 5)
        lbl1 = wx.StaticText(self, label="Serial interface")
        lbl2 = wx.StaticText(self, label="Detected system/components")
        self.if_list = wx.ListBox(self, -1, choices=["One", "Two", "Three"])
        self.id_list = wx.ListBox(self, -1, choices=["Red", "Blue", "Green"])
        fgrid.AddMany([(lbl1), (lbl2), (self.if_list, 1, wx.EXPAND), (self.id_list, 1, wx.EXPAND)])
        fgrid.SetFlexibleDirection(wx.VERTICAL)
        fgrid.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_ALL)
        fgrid.AddGrowableCol(0, 0)
        fgrid.AddGrowableCol(1, 0)
        fgrid.AddGrowableRow(1, 1)
        vbox.Add(fgrid, proportion=1, flag=wx.EXPAND|wx.ALL, border=8)

        hbox_buttons = wx.BoxSizer(wx.HORIZONTAL)
        btn_cancel = wx.Button(self, label="Cancel")
        btn_ok = wx.Button(self, label="OK")
        hbox_buttons.Add(btn_cancel)
        hbox_buttons.Add(btn_ok, flag=wx.LEFT, border=5)
        vbox.Add(hbox_buttons, proportion=0, flag=wx.ALIGN_RIGHT|wx.ALL, border=8)

        self.SetSizer(vbox)

class MasterSelect(object):
    def __init__(self):
        self.items = []

    def master_select_init(self):
        '''Create the GUI'''
        app = wx.App()
        MasterSelectDialog(None)
        app.MainLoop()

    def add_item(self, iface, sys_id, comp_id):
        '''Add a detected interface/id pair to the GUI'''
        self.items = [(iface, sys_id, comp_id)]
        #TODO update the item boxes

    #TODO method to poll if an item was selected, or some way of returning selection

if __name__ == '__main__':
    ms = MasterSelect()
    ms.master_select_init()
