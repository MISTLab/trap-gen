# -*- coding: iso-8859-1 -*-
####################################################################################
#         ___        ___           ___           ___
#        /  /\      /  /\         /  /\         /  /\
#       /  /:/     /  /::\       /  /::\       /  /::\
#      /  /:/     /  /:/\:\     /  /:/\:\     /  /:/\:\
#     /  /:/     /  /:/~/:/    /  /:/~/::\   /  /:/~/:/
#    /  /::\    /__/:/ /:/___ /__/:/ /:/\:\ /__/:/ /:/
#   /__/:/\:\   \  \:\/:::::/ \  \:\/:/__\/ \  \:\/:/
#   \__\/  \:\   \  \::/~~~~   \  \::/       \  \::/
#        \  \:\   \  \:\        \  \:\        \  \:\
#         \  \ \   \  \:\        \  \:\        \  \:\
#          \__\/    \__\/         \__\/         \__\/
#
#   This file is part of TRAP.
#
#   TRAP is free software; you can redistribute it and/or modify
#   it under the terms of the GNU Lesser General Public License as published by
#   the Free Software Foundation; either version 2 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU Lesser General Public License for more details.
#
#   You should have received a copy of the GNU Lesser General Public License
#   along with this TRAP; if not, write to the
#   Free Software Foundation, Inc.,
#   51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA.
#   or see <http://www.gnu.org/licenses/>.
#
#   (c) Luca Fossati, fossati@elet.polimi.it
#
####################################################################################


import trap

#OPER with IForm
oper_Iform = trap.MachineCode([('primary_opcode', 6), ('li', 26)])
#oper_Iform.setVarField('rt', ('GPR', 0), 'out')

#OPER with BForm
oper_Bform = trap.MachineCode([('primary_opcode', 6), ('bo', 5), ('bi', 5), ('bd',14), ('aa',1), ('lk',1)])
oper_Bform.setVarField('bd', ('GPR', 0), 'out')
oper_Bform.setVarField('bo', ('GPR', 0), 'in')
oper_Bform.setVarField('bi', ('GPR', 0), 'in')

#OPER with SCForm
oper_SCform = trap.MachineCode([('primary_opcode', 6), ('////', 5), ('///', 5), ('//',14), ('1',1), ('/',1)])
#oper_SCform.setVarField('rt', ('GPR', 0), 'out')
#oper_SCform.setVarField('ra', ('GPR', 0), 'in')
#oper_SCform.setVarField('rb', ('GPR', 0), 'in')

#OPER with DForm
oper_Dform_1 = trap.MachineCode([('primary_opcode', 6), ('rt', 5), ('ra', 5), ('d',16)])
oper_Dform_1.setVarField('rt', ('GPR', 0), 'out')
oper_Dform_1.setVarField('ra', ('GPR', 0), 'in')
oper_Dform_1.setVarField('d', ('GPR', 0), 'in')
oper_Dform_2 = trap.MachineCode([('primary_opcode', 6), ('rt', 5), ('ra', 5), ('si',16)])
oper_Dform_2.setVarField('rt', ('GPR', 0), 'out')
oper_Dform_2.setVarField('ra', ('GPR', 0), 'in')
oper_Dform_2.setVarField('si', ('GPR', 0), 'in')
oper_Dform_3 = trap.MachineCode([('primary_opcode', 6), ('rs', 5), ('ra', 5), ('d',16)])
oper_Dform_3.setVarField('rs', ('GPR', 0), 'in')
oper_Dform_3.setVarField('ra', ('GPR', 0), 'out')
oper_Dform_3.setVarField('d', ('GPR', 0), 'in')
oper_Dform_4 = trap.MachineCode([('primary_opcode', 6), ('rs', 5), ('ra', 5), ('ui',16)])
oper_Dform_4.setVarField('ra', ('GPR', 0), 'out')
oper_Dform_4.setVarField('rs', ('GPR', 0), 'in')
oper_Dform_4.setVarField('ui', ('GPR', 0), 'in')
oper_Dform_5 = trap.MachineCode([('primary_opcode', 6), ('bf', 3), ('/', 1), ('l', 1), ('ra', 5), ('si',16)])
oper_Dform_5.setVarField('bf', ('GPR', 0), 'in')
oper_Dform_5.setVarField('ra', ('GPR', 0), 'in')
oper_Dform_5.setVarField('si', ('GPR', 0), 'in')
oper_Dform_6 = trap.MachineCode([('primary_opcode', 6), ('bf', 3), ('/', 1), ('l', 1), ('ra', 5), ('ui',16)])
oper_Dform_6.setVarField('bf', ('GPR', 0), 'in')
oper_Dform_6.setVarField('ra', ('GPR', 0), 'in')
oper_Dform_6.setVarField('ui', ('GPR', 0), 'in')
oper_Dform_7 = trap.MachineCode([('primary_opcode', 6), ('to', 5), ('ra', 5), ('si',16)])
#oper_Dform_7.setVarField('rt', ('GPR', 0), 'out')
#oper_Dform_7.setVarField('ra', ('GPR', 0), 'in')
#oper_Dform_7.setVarField('rb', ('GPR', 0), 'in')

#OPER with XForm
oper_Xform_1 = trap.MachineCode([('primary_opcode', 6), ('rt', 5), ('ra', 5), ('rb',5), ('xo',10), ('rc',1)])
oper_Xform_1.setVarField('rt', ('GPR', 0), 'out')
oper_Xform_1.setVarField('ra', ('GPR', 0), 'in')
oper_Xform_1.setVarField('rb', ('GPR', 0), 'in')
oper_Xform_2 = trap.MachineCode([('primary_opcode', 6), ('rt', 5), ('ra', 5), ('rb',5), ('xo',10), ('/',1)])
oper_Xform_2.setVarField('rt', ('GPR', 0), 'out')
oper_Xform_2.setVarField('ra', ('GPR', 0), 'in')
oper_Xform_2.setVarField('rb', ('GPR', 0), 'in')
oper_Xform_3 = trap.MachineCode([('primary_opcode', 6), ('rt', 5), ('ra', 5), ('nb',5), ('xo',10), ('/',1)])
oper_Xform_3.setVarField('rt', ('GPR', 0), 'out')
oper_Xform_3.setVarField('ra', ('GPR', 0), 'in')
#oper_Xform_3.setVarField('rb', ('GPR', 0), 'in')
oper_Xform_4 = trap.MachineCode([('primary_opcode', 6), ('rt', 5), ('ra', 5), ('ws',5), ('xo',10), ('/',1)])
oper_Xform_4.setVarField('rt', ('GPR', 0), 'out')
oper_Xform_4.setVarField('ra', ('GPR', 0), 'in')
#oper_Xform_4.setVarField('rb', ('GPR', 0), 'in')
oper_Xform_5 = trap.MachineCode([('primary_opcode', 6), ('rt', 5), ('///', 5), ('rb',5), ('xo',10), ('/',1)])
oper_Xform_5.setVarField('rt', ('GPR', 0), 'out')
oper_Xform_5.setVarField('rb', ('GPR', 0), 'in')
oper_Xform_6 = trap.MachineCode([('primary_opcode', 6), ('rt', 5), ('///', 5), ('//',5), ('xo',10), ('/',1)])
oper_Xform_6.setVarField('rt', ('GPR', 0), 'out')
oper_Xform_7 = trap.MachineCode([('primary_opcode', 6), ('rs', 5), ('ra', 5), ('rb',5), ('xo',10), ('rc',1)])
#oper_Xform_7.setVarField('rt', ('GPR', 0), 'out')
oper_Xform_7.setVarField('ra', ('GPR', 0), 'in')
oper_Xform_7.setVarField('rb', ('GPR', 0), 'in')
oper_Xform_8 = trap.MachineCode([('primary_opcode', 6), ('rs', 5), ('ra', 5), ('rb',5), ('xo',10), ('1',1)])
#oper_Xform_8.setVarField('rt', ('GPR', 0), 'out')
oper_Xform_8.setVarField('ra', ('GPR', 0), 'in')
oper_Xform_8.setVarField('rb', ('GPR', 0), 'in')
oper_Xform_9 = trap.MachineCode([('primary_opcode', 6), ('rs', 5), ('ra', 5), ('rb',5), ('xo',10), ('/',1)])
#oper_Xform_9.setVarField('rt', ('GPR', 0), 'out')
oper_Xform_9.setVarField('ra', ('GPR', 0), 'in')
oper_Xform_9.setVarField('rb', ('GPR', 0), 'in')
oper_Xform_10 = trap.MachineCode([('primary_opcode', 6), ('rs', 5), ('ra', 5), ('nb',5), ('xo',10), ('/',1)])
#oper_Xform_10.setVarField('rt', ('GPR', 0), 'out')
oper_Xform_10.setVarField('ra', ('GPR', 0), 'in')
#oper_Xform_10.setVarField('rb', ('GPR', 0), 'in')
oper_Xform_11 = trap.MachineCode([('primary_opcode', 6), ('rs', 5), ('ra', 5), ('ws',5), ('xo',10), ('/',1)])
#oper_Xform_11.setVarField('rt', ('GPR', 0), 'out')
oper_Xform_11.setVarField('ra', ('GPR', 0), 'in')
#oper_Xform_11.setVarField('rb', ('GPR', 0), 'in')
oper_Xform_12 = trap.MachineCode([('primary_opcode', 6), ('rs', 5), ('ra', 5), ('sh',5), ('xo',10), ('rc',1)])
#oper_Xform_12.setVarField('rt', ('GPR', 0), 'out')
oper_Xform_12.setVarField('ra', ('GPR', 0), 'in')
#oper_Xform_12.setVarField('rb', ('GPR', 0), 'in')
oper_Xform_13 = trap.MachineCode([('primary_opcode', 6), ('rs', 5), ('ra', 5), ('///',5), ('xo',10), ('rc',1)])
#oper_Xform_13.setVarField('rt', ('GPR', 0), 'out')
oper_Xform_13.setVarField('ra', ('GPR', 0), 'in')
#oper_Xform_13.setVarField('rb', ('GPR', 0), 'in')
oper_Xform_14 = trap.MachineCode([('primary_opcode', 6), ('rs', 5), ('///', 5), ('rb',5), ('xo',10), ('/',1)])
#oper_Xform_14.setVarField('rt', ('GPR', 0), 'out')
#oper_Xform_14.setVarField('ra', ('GPR', 0), 'in')
oper_Xform_14.setVarField('rb', ('GPR', 0), 'in')
oper_Xform_15 = trap.MachineCode([('primary_opcode', 6), ('rs', 5), ('///', 5), ('//',5), ('xo',10), ('/',1)])
#oper_Xform_15.setVarField('rt', ('GPR', 0), 'out')
#oper_Xform_15.setVarField('ra', ('GPR', 0), 'in')
#oper_Xform_15.setVarField('rb', ('GPR', 0), 'in')
oper_Xform_16 = trap.MachineCode([('primary_opcode', 6), ('bf', 3), ('//', 1), ('l', 1), ('ra', 5), ('rb', 5),('xo',10), ('/', 1)])
oper_Xform_16.setVarField('bf', ('GPR', 0), 'in')
oper_Xform_16.setVarField('ra', ('GPR', 0), 'in')
oper_Xform_16.setVarField('rb', ('GPR', 0), 'in')
oper_Xform_17 = trap.MachineCode([('primary_opcode', 6), ('bf', 3), ('/', 2), ('bfa', 3), ('//', 2), ('///', 3),('xo',10), ('rc', 1)])
#oper_Xform_17.setVarField('rt', ('GPR', 0), 'out')
#oper_Xform_17.setVarField('ra', ('GPR', 0), 'in')
#oper_Xform_17.setVarField('rb', ('GPR', 0), 'in')
oper_Xform_18 = trap.MachineCode([('primary_opcode', 6), ('bf', 3), ('//', 2), ('///',5),('////',5), ('xo',10), ('/',1)])
#oper_Xform_18.setVarField('rt', ('GPR', 0), 'out')
#oper_Xform_18.setVarField('ra', ('GPR', 0), 'in')
#oper_Xform_18.setVarField('rb', ('GPR', 0), 'in')
oper_Xform_19 = trap.MachineCode([('primary_opcode', 6), ('bf', 3), ('//', 2), ('///',5),('u',5), ('xo',10), ('rc',1)])
#oper_Xform_19.setVarField('rt', ('GPR', 0), 'out')
#oper_Xform_19.setVarField('ra', ('GPR', 0), 'in')
#oper_Xform_19.setVarField('rb', ('GPR', 0), 'in')
oper_Xform_20 = trap.MachineCode([('primary_opcode', 6), ('bf', 3), ('//', 2), ('///',5),('////',5), ('xo',10), ('/',1)])
#oper_Xform_20.setVarField('rt', ('GPR', 0), 'out')
#oper_Xform_20.setVarField('ra', ('GPR', 0), 'in')
#oper_Xform_20.setVarField('rb', ('GPR', 0), 'in')
oper_Xform_21 = trap.MachineCode([('primary_opcode', 6), ('to', 5), ('ra', 5), ('rb',5),('xo',10), ('/',1)])
#oper_Xform_21.setVarField('rt', ('GPR', 0), 'out')
oper_Xform_21.setVarField('ra', ('GPR', 0), 'in')
oper_Xform_21.setVarField('rb', ('GPR', 0), 'in')
oper_Xform_22 = trap.MachineCode([('primary_opcode', 6), ('bt', 5), ('///', 5), ('//',5),('xo',10), ('rc',1)])
#oper_Xform_22.setVarField('rt', ('GPR', 0), 'out')
#oper_Xform_22.setVarField('ra', ('GPR', 0), 'in')
#oper_Xform_22.setVarField('rb', ('GPR', 0), 'in')
oper_Xform_23 = trap.MachineCode([('primary_opcode', 6), ('///', 5), ('ra', 5), ('rb',5),('xo',10), ('/',1)])
oper_Xform_23.setVarField('ra', ('GPR', 0), 'in')
oper_Xform_23.setVarField('rb', ('GPR', 0), 'in')
oper_Xform_24 = trap.MachineCode([('primary_opcode', 6), ('//', 5), ('///', 5), ('////',5),('xo',10), ('/',1)])
#oper_Xform_24.setVarField('rt', ('GPR', 0), 'out')
#oper_Xform_24.setVarField('ra', ('GPR', 0), 'in')
#oper_Xform_24.setVarField('rb', ('GPR', 0), 'in')
oper_Xform_25 = trap.MachineCode([('primary_opcode', 6), ('///', 5), ('////', 5),('e',1), ('//',4),('xo',10), ('/',1)])
#oper_Xform_25.setVarField('rt', ('GPR', 0), 'out')
#oper_Xform_25.setVarField('ra', ('GPR', 0), 'in')
#oper_Xform_25.setVarField('rb', ('GPR', 0), 'in')

#OPER with XLForm
oper_XLform_1 = trap.MachineCode([('primary_opcode', 6), ('bt', 5), ('ba', 5),('bb',5),('xo',10), ('/',1)])
oper_XLform_1.setVarField('bt', ('GPR', 0), 'out')
oper_XLform_1.setVarField('ba', ('GPR', 0), 'in')
oper_XLform_1.setVarField('bb', ('GPR', 0), 'in')
oper_XLform_2 = trap.MachineCode([('primary_opcode', 6), ('bc', 5), ('bi', 5),('///',5),('xo',10), ('lk',1)])
oper_XLform_2.setVarField('bc', ('GPR', 0), 'in')
oper_XLform_2.setVarField('bi', ('GPR', 0), 'in')
oper_XLform_3 = trap.MachineCode([('primary_opcode', 6), ('bf', 3), ('//', 2), ('bfa',3), ('///', 2), ('////', 5),('xo',10), ('/',1)])
#oper_XLform_3.setVarField('rt', ('GPR', 0), 'out')
#oper_XLform_3.setVarField('ra', ('GPR', 0), 'in')
#oper_XLform_3.setVarField('rb', ('GPR', 0), 'in')
oper_XLform_4 = trap.MachineCode([('primary_opcode', 6), ('/////', 5), ('////', 5),('///',5),('xo',10), ('/',1)])
#oper_XLform_4.setVarField('rt', ('GPR', 0), 'out')
#oper_XLform_4.setVarField('ra', ('GPR', 0), 'in')
#oper_XLform_4.setVarField('rb', ('GPR', 0), 'in')

#OPER with XFXForm
oper_XFXForm_1 = trap.MachineCode([('primary_opcode', 6), ('rt', 5), ('sprf', 10), ('xo',10), ('/',1)])
oper_XFXForm_1.setVarField('rt', ('GPR', 0), 'out')
#oper_XFXForm_1.setVarField('ra', ('GPR', 0), 'in')
#oper_XFXForm_1.setVarField('rb', ('GPR', 0), 'in')
oper_XFXForm_2 = trap.MachineCode([('primary_opcode', 6), ('rt', 5), ('dcrf', 10), ('xo',10), ('/',1)])
oper_XFXForm_2.setVarField('rt', ('GPR', 0), 'out')
#oper_XFXForm_2.setVarField('ra', ('GPR', 0), 'in')
#oper_XFXForm_2.setVarField('rb', ('GPR', 0), 'in')
oper_XFXForm_3 = trap.MachineCode([('primary_opcode', 6), ('rt', 5),('///', 1), ('fxm', 8),('//', 1), ('xo',10), ('/',1)])
oper_XFXForm_3.setVarField('rt', ('GPR', 0), 'out')
#oper_XFXForm_3.setVarField('ra', ('GPR', 0), 'in')
#oper_XFXForm_3.setVarField('rb', ('GPR', 0), 'in')
oper_XFXForm_4 = trap.MachineCode([('primary_opcode', 6), ('rs', 5), ('sprf', 10), ('xo',10), ('/',1)])
#oper_XFXForm_4.setVarField('rt', ('GPR', 0), 'out')
#oper_XFXForm_4.setVarField('ra', ('GPR', 0), 'in')
#oper_XFXForm_4.setVarField('rb', ('GPR', 0), 'in')
oper_XFXForm_5 = trap.MachineCode([('primary_opcode', 6), ('rs', 5), ('dcrf', 10), ('xo',10), ('/',1)])
#oper_XFXForm_5.setVarField('rt', ('GPR', 0), 'out')
#oper_XFXForm_5.setVarField('ra', ('GPR', 0), 'in')
#oper_XFXForm_5.setVarField('rb', ('GPR', 0), 'in')

#OPER with X0Form
oper_X0form_1 = trap.MachineCode([('primary_opcode', 6), ('rt', 5), ('ra', 5), ('rb',5), ('oe',1), ('xo',9), ('rc',1)])
oper_X0form_1.setVarField('rt', ('GPR', 0), 'out')
oper_X0form_1.setVarField('ra', ('GPR', 0), 'in')
oper_X0form_1.setVarField('rb', ('GPR', 0), 'in')
oper_X0form_2 = trap.MachineCode([('primary_opcode', 6), ('rt', 5), ('ra', 5), ('///',5), ('/',1), ('xo',9), ('rc',1)])
oper_X0form_2.setVarField('rt', ('GPR', 0), 'out')
oper_X0form_2.setVarField('ra', ('GPR', 0), 'in')

#OPER with MForm
oper_Mform_1 = trap.MachineCode([('primary_opcode', 6), ('rs', 5), ('ra', 5), ('rb',5), ('mb',5), ('me',5), ('rc',1)])
#oper_Mform_1.setVarField('rt', ('GPR', 0), 'out')
oper_Mform_1.setVarField('ra', ('GPR', 0), 'in')
oper_Mform_1.setVarField('rb', ('GPR', 0), 'in')
oper_Mform_2 = trap.MachineCode([('primary_opcode', 6), ('rs', 5), ('ra', 5), ('sh',5), ('mb',5), ('me',5), ('rc',1)])
#oper_Mform_2.setVarField('rt', ('GPR', 0), 'out')
oper_Mform_2.setVarField('ra', ('GPR', 0), 'in')
#oper_mform_2.setVarField('rb', ('GPR', 0), 'in')





