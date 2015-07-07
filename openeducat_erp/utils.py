# -*- coding: utf-8 -*-
###############################################################################
#
#    Tech-Receptives Solutions Pvt. Ltd.
#    Copyright (C) 2009-TODAY Tech-Receptives(<http://www.techreceptives.com>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################

from datetime import datetime
import base64
import logging
try:
    from reportlab.graphics.barcode import createBarcodeDrawing
except:
    _logger = logging.getLogger(__name__)
    _logger.info("ERROR IMPORTING REPORT LAB")

from openerp.osv import osv


def get_barcode_image(value, width=False, hight=False, hr=True, code='QR'):
    """ genrating image for barcode """
    options = {}
    if width:
        options['width'] = width
    if hight:
        options['hight'] = hight
    if hr:
        options['humanReadable'] = hr
    try:
        ret_val = createBarcodeDrawing(code, value=str(value), **options)
    except Exception, e:
        raise osv.except_osv('Error', e)
    return base64.encodestring(ret_val.asString('jpg'))


def server_to_local_timestamp(src_tstamp_str, src_format, dst_format,
                              dst_tz_name, tz_offset=True,
                              ignore_unparsable_time=True, server_tz=False):
    """
    Convert a source timestamp string into a destination timestamp string,
    attempting to apply the correct offset if both the server and local
    timezone are recognized, or no offset at all if they aren't or if tz_offset
    is false (i.e. assuming they are both in the same TZ).

    WARNING: This method is here to allow formatting dates correctly for
             inclusion in strings where the client would not be able to
             format/offset it correctly. DO NOT use it for returning date
             fields directly, these are supposed to be handled by the client!!

    @param src_tstamp_str: the str value containing the timestamp in the
                           server timezone.
    @param src_format: the format to use when parsing the server timestamp.
    @param dst_format: the format to use when formatting the resulting
                       timestamp for the local/client timezone.
    @param dst_tz_name: name of the destination timezone (such as the 'tz'
                        value of the client context)
    @param ignore_unparsable_time: if True, return False if src_tstamp_str
                                   cannot be parsed using src_format or
                                   formatted using dst_format.

    @return local/client formatted timestamp, expressed in the local/client
            timezone if possible and if tz_offset is true, or src_tstamp_str if
            timezone offset could not be determined.
    """
    if not src_tstamp_str:
        return False

    res = src_tstamp_str
    if src_format and dst_format:
        # find out server timezone
        if not server_tz:
            server_tz = "UTC"
        # dt_value needs to be a datetime.datetime object (so no
        # time.struct_time or mx.DateTime.DateTime here!)
        dt_value = datetime.strptime(src_tstamp_str, src_format)
        if tz_offset and dst_tz_name:
            import pytz
            src_tz = pytz.timezone(server_tz)
            dst_tz = pytz.timezone(dst_tz_name)
            src_dt = src_tz.localize(dt_value, is_dst=True)
            dt_value = src_dt.astimezone(dst_tz)
        res = dt_value.strftime(dst_format)
        # Normal ways to end up here are if strptime or strftime failed
        if not ignore_unparsable_time:
            return False
    return res
