# -*- coding: utf-8 -*-

from osv import osv, fields

class book_request_queue(osv.osv_memory):

    _name = 'book.request.queue'

    _columns = {
                'date_from': fields.date('From Date', required=True),
                'date_to': fields.date('To Date', required=True),
#                'book_ids': fields.many2many('op.book', 'op_queue_book_rl', 'op_book_id', 'op_queue_id', 'Book'),
                'book_id': fields.many2one('op.book', 'Book'),
                }

    def add_book_request_queue(self, cr, uid, ids, context={}):
        value = {}
        
        queue_pool = self.pool.get('op.book.queue')
        book_pool = self.pool.get('op.book')
        
        for this_obj in self.browse(cr, uid, ids, context):
            queue_data = {
                          'partner_id': self.pool.get('res.users').browse(cr, uid, uid, context).partner_id.id,
                          'date_from': this_obj.date_from,
                          'date_to': this_obj.date_to,
                          }
            
            id_book = book_pool.read(cr, uid, this_obj.book_id.id, ['id_book'])['id_book']
            
            if id_book:
                search_book = book_pool.search(cr, uid, [('id_book','=', id_book)])
                
                if search_book:
                    queue_data.update({'book_ids': [(6,0,search_book)]})

            else:
                queue_data.update({'book_ids': [(6,0,[this_obj.book_id.id])]})

            queue_pool.create(cr, uid, queue_data, context)
            
            value = {'type': 'ir.actions.act_window_close'}
        return value


book_request_queue()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
