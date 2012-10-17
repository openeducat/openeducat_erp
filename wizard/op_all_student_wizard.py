# -*- coding: utf-8 -*-

from osv import osv, fields

class op_all_student_wizard(osv.osv_memory):

    _name = 'op.all.student'
    
    _columns = {
                
                'student_ids': fields.many2many('res.partner', 'student_student_rel', 'op_student_id', 'student_id', string='Add Student(s)'),
                }
    
    
    def confirm_student(self, cr, uid, ids, context={}):
        value = {}
        partner_pool = self.pool.get("res.partner")
        data = self.read(cr, uid, ids)[0]
        
        data.update({'ids':context.get('active_ids',[]), 'student_ids': data['student_ids']})
        
        print 'data________',data
        print context.get('active_id',False)
        for student_data in data['student_ids']:
            dic = {}
            student = partner_pool.browse(cr,uid, student_data)
            dic = {
                   'student_id':student.id,
                   'present':True,
                   'attendance_id': context.get('active_id'),
                   }

            cr_id = self.pool.get('op.attendance.line').create(cr, uid, dic, context=context)
            print "RRRRRRRRRRRRRRRRRRRRRRRRRR__________",cr_id
        value = {'type': 'ir.actions.act_window_close'}
        return value
    
         
op_all_student_wizard()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
