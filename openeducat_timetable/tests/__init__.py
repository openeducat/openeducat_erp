###############################################################################
#
#    OpenEduCat Inc
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<https://www.openeducat.org>).
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

# Pre-existing suite (kept as-is).
from . import test_timetable
from . import test_timetable_robust

# New tier-A/B suite added this session — each file guards a
# specific regression class we hit.
from . import test_install
from . import test_compute_timing
from . import test_compute_name
from . import test_compute_batch_users
from . import test_check_timetable_fields
from . import test_notify_user
from . import test_follower_sync
from . import test_faculty_session_count
from . import test_onchange_batch_populate
from . import test_wizard_generate_timetable
from . import test_migration_backfill
