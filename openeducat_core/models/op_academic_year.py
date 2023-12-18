# -*- coding: utf-8 -*-
# Part of OpenEduCat. See LICENSE file for full copyright & licensing details.

##############################################################################
#
#    OpenEduCat Inc
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<http://www.openeducat.org>).
#
##############################################################################

from odoo import models, fields
from datetime import timedelta


class OpAcademicYear(models.Model):
    _name = 'op.academic.year'
    _description = "Academic Year"

    name = fields.Char('Name', required=True)
    start_date = fields.Date('Start Date', required=True)
    end_date = fields.Date('End Date', required=True)

    term_structure = fields.Selection([('two_sem', 'Two Semesters'),
                                       ('two_sem_qua', 'Two Semesters '
                                                       'subdivided by Quarters'),
                                       ('two_sem_final', 'Two Semesters subdivided'
                                                         ' by Quarters and '
                                                         'Final Exams'),
                                       ('three_sem', 'Three Trimesters'),
                                       ('four_Quarter', 'Four Quarters'),
                                       ('final_year', 'Final Year Grades'
                                                      ' subdivided by Quarters'),
                                       ('others', 'Other(overlapping terms,'
                                                  ' custom schedules)')],
                                      string='Term Structure', default='two_sem',
                                      required=True)
    academic_term_ids = fields.One2many('op.academic.term', 'academic_year_id',
                                        string='Academic Terms')
    create_boolean = fields.Boolean()
    company_id = fields.Many2one(
        'res.company', string='Company',
        default=lambda self: self.env.company)

    def term_create(self):
        num = 0
        final = 1
        academic_terms = self.env['op.academic.term'].search([])
        self.create_boolean = True
        if self.term_structure == 'two_sem':
            for record in self:
                if not record.academic_term_ids:
                    from_d = self.start_date
                    to_d = self.end_date
                    delta = to_d - from_d
                    res = []
                    day = (delta.days + 1) / 2
                    vals = {'name': 'Semester 1',
                            'from_date': from_d,
                            'to_date': (from_d + timedelta(days=day))}
                    res.append(vals)
                    vals = {'name': 'Semester 2',
                            'from_date': (from_d + timedelta(days=day + 1)),
                            'to_date': to_d}
                    res.append(vals)
                    for term in res:
                        academic_terms.create({
                            'name': term['name'],
                            'term_start_date': term['from_date'],
                            'term_end_date': term['to_date'],
                            'academic_year_id': self.id
                        })

        elif self.term_structure == 'two_sem_qua':
            for record in self:
                if not record.academic_term_ids:
                    from_d = self.start_date
                    to_d = self.end_date
                    delta = to_d - from_d
                    res = []
                    day = (delta.days + 1) / 2
                    vals = {'name': 'Semester 1',
                            'from_date': from_d,
                            'to_date': (from_d + timedelta(days=day))}
                    res.append(vals)
                    vals = {'name': 'Semester 2',
                            'from_date': (from_d + timedelta(days=day + 1)),
                            'to_date': to_d}
                    res.append(vals)
                    for term in res:
                        academic_terms.create({
                            'name': term['name'],
                            'term_start_date': term['from_date'],
                            'term_end_date': term['to_date'],
                            'academic_year_id': self.id
                        })
                        for sub_term in self.academic_term_ids:
                            sub_from_d = sub_term.term_start_date
                            sub_to_d = sub_term.term_end_date
                            delta = sub_to_d - sub_from_d
                            result = []
                            day = (delta.days + 1) / 2
                            vals = {'name': 'Quarter' + ' ' + str(num+1),
                                    'from_date': sub_from_d,
                                    'to_date': (sub_from_d + timedelta(days=day))}
                            result.append(vals)
                            vals = {'name': 'Quarter' + ' ' + str(num+2),
                                    'from_date': (sub_from_d + timedelta(
                                        days=day + 1)),
                                    'to_date': sub_to_d}
                            result.append(vals)
                        num = num + 2

                        for in_terms in result:
                            academic_terms.create({
                                'name': in_terms['name'],
                                'term_start_date': in_terms['from_date'],
                                'term_end_date': in_terms['to_date'],
                                'academic_year_id': self.id,
                                'parent_term': sub_term.id
                            })

        elif self.term_structure == 'two_sem_final':
            for record in self:
                if not record.academic_term_ids:
                    from_d = self.start_date
                    to_d = self.end_date
                    delta = to_d - from_d
                    res = []
                    day = (delta.days + 1) / 2
                    vals = {'name': 'Semester 1',
                            'from_date': from_d,
                            'to_date': (from_d + timedelta(days=day))}
                    res.append(vals)
                    vals = {'name': 'Semester 2',
                            'from_date': (from_d + timedelta(days=day + 1)),
                            'to_date': to_d}
                    res.append(vals)

                    for term in res:
                        academic_terms.create({
                            'name': term['name'],
                            'term_start_date': term['from_date'],
                            'term_end_date': term['to_date'],
                            'academic_year_id': self.id
                        })

                        for sub_term in self.academic_term_ids:
                            sub_from_d = sub_term.term_start_date
                            sub_to_d = sub_term.term_end_date
                            delta = sub_to_d - sub_from_d
                            result = []

                            day = (delta.days + 1) / 2
                            vals = {'name': 'Quarter' + ' ' + str(num+1),
                                    'from_date': sub_from_d,
                                    'to_date': (sub_from_d + timedelta(days=day))}
                            result.append(vals)
                            vals = {'name': 'Quarter' + ' ' + str(num + 2),
                                    'from_date': (sub_from_d + timedelta(
                                        days=day + 1)),
                                    'to_date': (sub_from_d + timedelta(
                                        days=delta.days - 1))}
                            result.append(vals)
                            vals = {'name': 'Final Exam' + ' ' + str(final),
                                    'from_date': sub_to_d,
                                    'to_date': sub_to_d}
                            result.append(vals)
                        num = num + 2
                        final = final + 1

                        for in_terms in result:
                            academic_terms.create({
                                'name': in_terms['name'],
                                'term_start_date': in_terms['from_date'],
                                'term_end_date': in_terms['to_date'],
                                'academic_year_id': self.id,
                                'parent_term': sub_term.id
                            })

        elif self.term_structure == 'three_sem':
            for record in self:
                if not record.academic_term_ids:
                    from_d = self.start_date
                    to_d = self.end_date
                    delta = to_d - from_d
                    res = []
                    day = (delta.days + 1) / 3
                    to_date1 = (from_d + timedelta(days=day))
                    from_date1 = (from_d + timedelta(days=day + 1))
                    to_date2 = (from_date1 + timedelta(days=day))
                    from_date2 = (from_date1 + timedelta(days=day + 1))

                    vals = {'name': 'Semester 1',
                            'from_date': from_d,
                            'to_date': to_date1}
                    res.append(vals)

                    vals = {'name': 'Semester 2',
                            'from_date': from_date1,
                            'to_date': to_date2}
                    res.append(vals)

                    vals = {'name': 'Semester 3',
                            'from_date': from_date2,
                            'to_date': to_d}
                    res.append(vals)
                    for term in res:
                        academic_terms.create({
                            'name': term['name'],
                            'term_start_date': term['from_date'],
                            'term_end_date': term['to_date'],
                            'academic_year_id': self.id
                        })

        elif self.term_structure == 'four_Quarter':
            for record in self:
                if not record.academic_term_ids:
                    from_d = self.start_date
                    to_d = self.end_date
                    delta = to_d - from_d
                    res = []
                    day = (delta.days + 1) / 4

                    to_date1 = (from_d + timedelta(days=day))
                    from_date1 = (from_d + timedelta(days=day + 1))
                    to_date2 = (from_date1 + timedelta(days=day))
                    from_date2 = (from_date1 + timedelta(days=day + 1))
                    to_date3 = (from_date2 + timedelta(days=day))
                    from_date3 = (from_date2 + timedelta(days=day + 1))

                    vals = {'name': 'Semester 1',
                            'from_date': from_d,
                            'to_date': to_date1}
                    res.append(vals)

                    vals = {'name': 'Semester 2',
                            'from_date': from_date1,
                            'to_date': to_date2}
                    res.append(vals)

                    vals = {'name': 'Semester 3',
                            'from_date': from_date2,
                            'to_date': to_date3}
                    res.append(vals)

                    vals = {'name': 'Semester 4',
                            'from_date': from_date3,
                            'to_date': to_d}
                    res.append(vals)

                    for term in res:
                        academic_terms.create({
                            'name': term['name'],
                            'term_start_date': term['from_date'],
                            'term_end_date': term['to_date'],
                            'academic_year_id': self.id
                        })

        elif self.term_structure == 'final_year':
            for record in self:
                if not record.academic_term_ids:
                    from_d = self.start_date
                    to_d = self.end_date
                    res = []
                    res.append({'name': 'Semester 1',
                                'from_date': from_d,
                                'to_date': to_d})

                    for term in res:
                        academic_terms.create({
                            'name': term['name'],
                            'term_start_date': term['from_date'],
                            'term_end_date': term['to_date'],
                            'academic_year_id': self.id
                        })
                    for sub_term in self.academic_term_ids:
                        sub_from_d = sub_term.term_start_date
                        sub_to_d = sub_term.term_end_date
                        delta = sub_to_d - sub_from_d
                        result = []
                        day = (delta.days + 1) / 4

                        to_date1 = (from_d + timedelta(days=day))
                        from_date1 = (from_d + timedelta(days=day + 1))
                        to_date2 = (from_date1 + timedelta(days=day))
                        from_date2 = (from_date1 + timedelta(days=day + 1))
                        to_date3 = (from_date2 + timedelta(days=day))
                        from_date3 = (from_date2 + timedelta(days=day + 1))

                        vals = {'name': 'Quarter 1',
                                'from_date': from_d,
                                'to_date': to_date1}
                        result.append(vals)

                        vals = {'name': 'Quarter 2',
                                'from_date': from_date1,
                                'to_date': to_date2}
                        result.append(vals)

                        vals = {'name': 'Quarter 3',
                                'from_date': from_date2,
                                'to_date': to_date3}
                        result.append(vals)

                        vals = {'name': 'Quarter 4',
                                'from_date': from_date3,
                                'to_date': to_d}
                        result.append(vals)

                        for in_terms in result:
                            academic_terms.create({
                                'name': in_terms['name'],
                                'term_start_date': in_terms['from_date'],
                                'term_end_date': in_terms['to_date'],
                                'academic_year_id': self.id,
                                'parent_term': sub_term.id
                            })
