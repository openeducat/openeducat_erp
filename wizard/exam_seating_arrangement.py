# -*- coding: utf-8 -*-

from osv import osv, fields

class exam_seat_arrange(osv.TransientModel):

    _name = 'exam.seat.arrange'

    _columns = {
                'exam_id': fields.many2one('op.exam','Exam'),
                }

exam_seat_arrange()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
