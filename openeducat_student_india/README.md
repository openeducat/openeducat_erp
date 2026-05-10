# OpenEduCat Student India Module

This module extends the OpenEduCat student model with India-specific customizations.

## Overview

The `openeducat_student_india` module customizes the student model for Indian educational institutions by:
- Adding India-specific fields: Aadhar Number, Religion, and Caste
- Hiding unnecessary fields from the UI (Visa Info, Nationality) while preserving data in the database
- Setting default country to India for all new students
- Providing proper validation for all new fields

## Features

### New Fields

1. **Aadhar Number** (Optional)
   - Format: 12-digit unique number
   - Validation: Exact 12 digits, numeric only
   - Constraint: Unique per student (prevents duplicates)
   - Stored in database for identification and compliance

2. **Religion** (Optional)
   - Selection options: Hindu, Muslim, Christian, Sikh, Buddhist, Jain, Other
   - Used for institutional records and demographic tracking

3. **Caste** (Optional)
   - Selection options: General, SC (Scheduled Caste), ST (Scheduled Tribe), OBC-NCL, OBC-CL
   - Used for scholarship eligibility, reservations, and affirmative action tracking

### Default Country

- **Country** - Automatically set to **India** for all new students
- Inherits from res.partner address fields
- Can be overridden if needed for specific cases

### Hidden Fields

The following fields are hidden from the student form UI but remain in the database for backward compatibility:
- **Visa Info** - No longer required for Indian students
- **Nationality** - Assumed Indian for all students in this configuration

## Installation

1. Place the module in your Odoo addons directory
2. Install the module through Odoo UI or command line:
   ```bash
   odoo -d database_name -u openeducat_student_india
   ```

## Deployment to Production

### Prerequisites
- Odoo 18.0 with openeducat_core already deployed
- Database backup (recommended)

### Deployment Steps

1. **Pull Latest Code**
   ```bash
   cd /path/to/openeducat_erp
   git pull origin 18.0
   ```

2. **Install Module via Command Line**
   ```bash
   odoo -d production_database_name -u openeducat_student_india --stop-after-init
   ```

   Or **via Web UI:**
   - Log in as Administrator
   - Go to Apps → Search "OpenEduCat Student India"
   - Click Install

3. **Restart Odoo Service** (if needed)
   ```bash
   systemctl restart odoo
   # or
   supervisorctl restart openeducat_erp
   ```

4. **Verify Installation**
   - Open any student record
   - Confirm "India Specific Information" section appears
   - Verify Aadhar Number, Religion, Caste fields are present
   - Confirm Visa Info and Nationality are hidden

### Data Safety
- **Zero Data Loss**: All existing student records are preserved
- **Backward Compatible**: Old fields (visa_info, nationality) remain in database
- **No Migration Required**: Module installs without data migration scripts

### Rollback (if needed)
```bash
# Uninstall module
odoo -d production_database_name -u openeducat_student_india --uninstall-all

# Revert code changes
git reset --hard HEAD~8
git push --force origin 18.0
```

## Usage

After installation:
1. Open any student record (create new or edit existing)
2. You'll see the new "India Specific Information" section with the new fields
3. **Country field** automatically defaults to India for new students
4. Fill in Aadhar number (12 digits), Religion, and Caste as needed
5. The form will validate Aadhar format automatically (must be exactly 12 digits)
6. Try to create duplicate Aadhar numbers - system will prevent it with validation error

### Form Layout
```
Personal Information
├── First Name, Middle Name, Last Name
├── Birth Date, Gender, Blood Group
└── Emergency Contact

India Specific Information (NEW)
├── Aadhar Number (12-digit validation)
├── Religion (dropdown: Hindu/Muslim/Christian/Sikh/Buddhist/Jain/Other)
└── Caste (dropdown: General/SC/ST/OBC-NCL/OBC-CL)

Address Information
├── Street, City, State, ZIP
└── Country (defaults to India, can be overridden)
```

## Validation Rules

- **Aadhar Number**: Must be exactly 12 numeric digits if provided. System prevents duplicate Aadhar numbers.
- **Religion & Caste**: Free selection from predefined lists based on Indian demographics

## Data Migration

This module preserves all existing student data:
- Existing visa_info and nationality values remain in the database
- These fields are simply hidden from forms and list views
- If needed in the future, the fields can be made visible again by removing the view customizations

## Testing

Run the module tests when Odoo is running:
```bash
odoo -d database_name -i openeducat_student_india --test-tags=openeducat_student_india
```

All tests verify:
- Aadhar validation (format, uniqueness, optional)
- Religion and Caste selection options
- Backward compatibility with existing fields

## Dependencies

- `openeducat_core` >= 18.0

## License

LGPL-3.0 (Same as OpenEduCat)

## Author

OpenEduCat Inc
