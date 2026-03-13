###############################################################################
#
#    openEMIS
#    Copyright (C) 2009-TODAY openEMIS(<https://www.openemis.org>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################

from odoo import fields, models

CBC_GRADE_LEVELS = [
    ('all', 'All Grades'),
    ('grade_1', 'Grade 1'),
    ('grade_2', 'Grade 2'),
    ('grade_3', 'Grade 3'),
    ('grade_4', 'Grade 4'),
    ('grade_5', 'Grade 5'),
    ('grade_6', 'Grade 6'),
    ('grade_7', 'Grade 7'),
    ('grade_8', 'Grade 8'),
    ('grade_9', 'Grade 9'),
    ('grade_10', 'Grade 10'),
    ('grade_11', 'Grade 11'),
    ('grade_12', 'Grade 12'),
    ('college', 'College / University'),
]

RESOURCE_FORMATS = [
    ('book', 'Book (Physical)'),
    ('pdf', 'PDF Document'),
    ('word', 'Word Document'),
    ('excel', 'Excel / CSV Spreadsheet'),
    ('video', 'Video'),
    ('audio', 'Audio / Podcast'),
    ('image', 'Image / Infographic'),
    ('presentation', 'Presentation (PPT/Slides)'),
    ('ebook', 'E-Book'),
    ('other', 'Other'),
]


class OpMedia(models.Model):
    _name = "op.media"
    _description = "Media Details"
    _inherit = "mail.thread"
    _order = "name"

    name = fields.Char('Title', size=128, required=True)
    isbn = fields.Char('ISBN Code', size=64)
    tags = fields.Many2many('op.tag', string='Tag(s)')
    author_ids = fields.Many2many(
        'op.author', string='Author(s)', required=True)
    edition = fields.Char('Edition')
    description = fields.Text('Description')
    publisher_ids = fields.Many2many(
        'op.publisher', string='Publisher(s)', required=True)
    course_ids = fields.Many2many('op.course', string='Course')
    movement_line = fields.One2many('op.media.movement', 'media_id',
                                    'Movements')
    subject_ids = fields.Many2many(
        'op.subject', string='Subjects')
    internal_code = fields.Char('Internal Code', size=64)
    queue_ids = fields.One2many('op.media.queue', 'media_id', 'Media Queue')
    unit_ids = fields.One2many('op.media.unit', 'media_id', 'Units')
    media_type_id = fields.Many2one('op.media.type', 'Media Type')
    active = fields.Boolean(default=True)
    # CBC Categorisation fields
    grade_level = fields.Selection(
        CBC_GRADE_LEVELS, string='Grade Level', default='all',
        help="Target CBC grade level for this learning resource")
    topic = fields.Char(
        'Topic', size=256,
        help="Specific topic within the subject, e.g. 'Fractions' or "
             "'The Water Cycle'")
    resource_format = fields.Selection(
        RESOURCE_FORMATS, string='Resource Format', default='book',
        help="Format of the learning resource (video, PDF, audio, etc.)")

    _sql_constraints = [
        ('unique_name_isbn',
         'unique(isbn)',
         'ISBN code must be unique per media!'),
        ('unique_name_internal_code',
         'unique(internal_code)',
         'Internal Code must be unique per media!'),
    ]
