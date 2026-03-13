# openEMIS 🎓

[![License: LGPL v3](https://img.shields.io/badge/License-LGPL%20v3-blue.svg)](LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/eodenyire/openEMIS.svg)](https://github.com/eodenyire/openEMIS/stargazers)

## Introduction 🚀

openEMIS is a powerful, feature-rich **Open Source Educational Management Information System (EMIS)** designed to streamline academic and administrative processes in educational institutions. Whether you're managing admissions, academics, finance, or human resources, openEMIS provides an integrated platform that empowers your institution with flexibility and innovation. Join our community to transform education management and embrace the future of learning! 🌟

Built on **Odoo 18.0**, openEMIS is fully modular – install only what you need and extend it as your institution grows.

---

## Table of Contents
- [Features 🚀📚](#features-)
- [Module Overview 📦](#module-overview-)
- [Demo & Live Links 🌐](#demo--live-links-)
- [Installation](#installation)
- [Data Population 🗄️](#data-population-)
- [Documentation 📖](#documentation-)
- [Community & Support 🤝](#community--support-)
- [Roadmap 🗺️](#roadmap-)
- [License 📄](#license-)
- [Contact 📞](#contact-)

---

## Features 🚀📚

openEMIS offers a comprehensive suite of features tailored for modern educational institutions:

- **Admissions & Registration** 🎟️: Simplify enrollment and registration processes.
- **Student Information Management** 👨‍🎓👩‍🎓: Manage student profiles, academic history, and personal details.
- **Course & Batch Management** 📚: Organize courses, batches, and scheduling with ease.
- **Examination Management** 📝: Streamline exam scheduling, evaluation, and result processing.
- **Fee & Finance Management** 💰: Automate fee collection, invoicing, and financial reporting.
- **Attendance & Timetable** ⏰: Keep track of attendance and manage class schedules efficiently.
- **Library Management** 📖: Handle book lending, cataloging, and member management.  Resources are categorised by grade level (Grade 1–12), subject, topic, and format (video, audio, PDF, Word, CSV, etc.).
- **DigiGuide – Digital Career Guidance** 🎯: Track CBC academic performance (weekly assignments, mid-term, termly and annual exams) and predict national exam results for Grade 3, 6, 9 and 12.  Integrates with the **KUCCPS API** to fetch university and college career requirements and surface eligible careers for each student.
- **Mentorship Platform** 🤝: Connect students with approved mentors (professionals, teachers, parents) through direct messages (DMs) and group discussion forums.  AI-assisted question routing directs questions to the most relevant mentor.
- **Educational Blog** ✍️: A platform for mentors, teachers and professionals to publish educational articles accessible to all students.  Includes category management, comment moderation and grade-level tagging.
- **Transport & Hostel Management** 🚍🏠: Oversee transportation logistics and hostel accommodations.
- **Communication Tools** 📢: Enhance collaboration with integrated messaging and notifications.
- **Reporting & Analytics** 📊: Generate insightful reports for data-driven decision-making.
- **HR & Payroll Management** 👥: Manage staff records, payroll, and performance reviews.
- **Customizable & Modular** 🔧: Adapt or extend modules to meet your institution's unique needs.
- **Secure & Scalable** 🔒: Robust security features ensure your data is protected while scaling with your growth.

For a full list of features, please visit our [Features Page](https://www.openemis.org/features) 😊

---

## Module Overview 📦

| Module | Description |
|--------|-------------|
| [`openeducat_core`](openeducat_core/README.md) | Foundation: students, courses, subjects, faculties, academic years & terms |
| [`openeducat_admission`](openeducat_admission/README.md) | Admissions & enrolment workflow |
| [`openeducat_activity`](openeducat_activity/README.md) | Extra-curricular activities management |
| [`openeducat_assignment`](openeducat_assignment/README.md) | Assignment creation, submission & grading |
| [`openeducat_attendance`](openeducat_attendance/README.md) | Student & faculty attendance tracking |
| [`openeducat_classroom`](openeducat_classroom/README.md) | Classroom management |
| [`openeducat_exam`](openeducat_exam/README.md) | Examination scheduling, mark sheets & grade configuration |
| [`openeducat_fees`](openeducat_fees/README.md) | Fee structure, invoicing and payment tracking |
| [`openeducat_library`](openeducat_library/README.md) | Library management with CBC grade-level, subject, topic & format categorisation |
| [`openeducat_timetable`](openeducat_timetable/README.md) | Class timetable generation and management |
| [`openeducat_parent`](openeducat_parent/README.md) | Parent portal and parent–student linking |
| [`openeducat_facility`](openeducat_facility/README.md) | School facilities management |
| [`openeducat_digiguide`](openeducat_digiguide/README.md) | 🆕 Digital Career Guidance: CBC performance tracking, national exam prediction & KUCCPS career integration |
| [`openeducat_mentorship`](openeducat_mentorship/README.md) | 🆕 Mentorship platform: mentor registration, DMs, group forums |
| [`openeducat_blog`](openeducat_blog/README.md) | 🆕 Educational blog for mentors, teachers & professionals |
| [`openeducat_erp`](openeducat_erp/README.md) | Meta-module that bundles all core modules |
| [`theme_web_openeducat`](theme_web_openeducat/README.md) | Custom UI theme |

---

## Demo & Live Links 🌐

Experience openEMIS firsthand:
- **Online Demo**: [Try our live demo](https://www.openemis.org/demo) 🎥
- **Official Website**: [Visit openEMIS.org](https://www.openemis.org) 🌟
- **Community Meetings & Webinars**:
  - [Join our next community meeting](https://www.openemis.org/meeting) 🤝
  - [Register for upcoming webinars](https://www.openemis.org/events) 🎤

---

## Installation 🛠️

Follow these steps to set up openEMIS:

1. Clone the repository: `git clone https://github.com/eodenyire/openEMIS.git`
2. Place modules in your Odoo addons directory
3. Install dependencies: `pip install -r requirements.txt` (if applicable)
4. Start Odoo and install the `openEMIS ERP` module from the Apps menu
5. Load demo data by enabling "Load Demo Data" during installation

For detailed setup instructions, refer to the [Odoo documentation](https://www.odoo.com/documentation/18.0/).

> **Docker Quick-Start**
> ```bash
> docker-compose up -d
> ```
> The compose file starts PostgreSQL and Odoo 18.0 together.  Open `http://localhost:8069` to access the interface.

---

## Data Population 🗄️

openEMIS ships with a comprehensive data seeding script to populate your database with realistic test data:

```bash
python scripts/generate_demo_data.py
```

This script generates:
- **100 Classrooms** (R001–R100, capacity 30 each)
- **100 Staff / Faculty** members
- **100 Parents** (with partner and user accounts)
- **100 Students** per class (mapped to courses and batches)

The generated XML files are placed in each module's `demo/` directory and are loaded automatically during demo-data installation.

---

## Documentation 📖

Learn more about openEMIS:
- **Documentation Portal**: [openEMIS Documentation](https://www.openemis.org/docs/)
- **User Guides**: Comprehensive guides to help you master the system quickly.
- Each module contains its own **README.md** with detailed model descriptions, field definitions and usage instructions.

---

## Community & Support 🤝

Join our active and vibrant community:
- **Issue Tracker**: Report bugs and request features on [GitHub Issues](https://github.com/eodenyire/openEMIS/issues)
- **Community Chat**: Connect with peers on our community channels

---

## Roadmap 🗺️

We're continuously evolving! Here's a glimpse of what's coming:
- **DigiGuide ML Enhancements** 🤖: Upgrade the national-exam prediction engine from weighted averages to a machine-learning model trained on historical national results.
- **KUCCPS Live Integration** 🔗: Automate nightly synchronisation with the official KUCCPS API when it becomes publicly available.
- **Mentorship Mobile App** 📱: Native iOS/Android companion for the mentorship module.
- **Blog Portal** 🌐: Public-facing web portal (Odoo Website) for the educational blog.
- **Enhanced Mobile Experience** 📱: Optimizing for a seamless mobile interface.
- **Performance Optimization** ⚡: Continuous improvements for faster and smoother operations.

Stay tuned for future updates and contribute to shaping our roadmap!

---

## License 📄

openEMIS is distributed under the **LGPL-3.0 License**. See the [LICENSE](LICENSE) file for more details.

---

## Contact 📞

Have questions or need support? Get in touch:
- **Email**: [support@openemis.org](mailto:support@openemis.org)
- **GitHub**: [https://github.com/eodenyire/openEMIS](https://github.com/eodenyire/openEMIS)

---

Thank you for choosing **openEMIS** – empowering educational institutions with open source technology. We appreciate your support and look forward to your contributions! 🙌

*Happy Learning & Coding! 💻🎉*
