#!/usr/bin/python

import wx

class MasterSelect(wx.Frame):
    def __init__(self, *args, **kwargs):
        super(MasterSelect, self).__init__(*args, **kwargs)
        self.init_ui()

        self.SetSize((600, 400))
        self.SetTitle("Select MAVLink master")
        self.Centre()
        self.Show(True)

    def init_ui(self):
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        hbox_label = wx.BoxSizer(wx.HORIZONTAL)
        lbl1 = wx.StaticText(panel, label="Serial interface")
        hbox_label.Add(lbl1, flag=wx.EXPAND|wx.RIGHT|wx.LEFT, border=8)
        lbl2 = wx.StaticText(panel, label="Detected system/components")
        hbox_label.Add(lbl2, flag=wx.EXPAND|wx.RIGHT|wx.LEFT, border=8)
        vbox.Add(hbox_label, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=20)

        panel.SetSizer(vbox)

def master_select_init():
    app = wx.App()
    MasterSelect(None)
    app.MainLoop()

if __name__ == '__main__':
    master_select_init()
