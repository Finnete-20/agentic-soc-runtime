SOC_DATASET = [

# =========================
# 🔴 PHISHING (1)
# =========================

{
"email": """
Subject: Urgent Password Reset Required

Your Microsoft account has been suspended due to suspicious activity.

Verify immediately:
https://secure-microsoftverify-login.com
""",
"label": 1
},

{
"email": """
Subject: Payroll Update Required

Update your banking details immediately or payroll will be delayed:
https://employee-payroll-update.net
""",
"label": 1
},

{
"email": """
Subject: GVSU Enrollment Form

Michael Brown <gvsuenrollment.help@gmail.com>

Complete here:
https://forms.gle/r1yZEXiJ1ms6Rsw58
""",
"label": 1
},

{
"email": """
Subject: Account Locked - Immediate Action Required

Your account has been locked. Verify now:
https://account-verify-security.com
""",
"label": 1
},

{
"email": """
Subject: Package Delivery Failed

Reschedule delivery immediately:
https://delivery-reschedule.info
""",
"label": 1
},

{
"email": """
Subject: Student Loan Verification Required

Confirm eligibility now:
https://student-loan-verify.net
""",
"label": 1
},

{
"email": """
Subject: Microsoft Security Alert

Unusual login detected. Confirm identity:
https://security-microsoft-alert.com
""",
"label": 1
},

{
"email": """
Subject: HR Benefits Expiring Today

Your employee benefits expire. Confirm now:
https://hr-benefits-update.org
""",
"label": 1
},

{
"email": """
Subject: IT Admin Alert

Your workstation will be locked unless verified:
https://it-admin-security-check.com
""",
"label": 1
},

{
"email": """
Subject: Tax Refund Available

Claim your refund here:
https://irs-tax-refund-check.net
""",
"label": 1
},

{
"email": """
Subject: Zoom Account Suspended

Login to restore access:
https://zoom-security-login.net
""",
"label": 1
},

{
"email": """
Subject: Bank Verification Required

Confirm identity to avoid account freeze:
https://bank-secure-verify.com
""",
"label": 1
},

{
"email": """
Subject: Scholarship Approval Pending

Submit verification here:
https://scholarship-approval.net
""",
"label": 1
},

{
"email": """
Subject: DocuSign Document Pending

Sign document immediately:
https://docusign-secure-sign.net
""",
"label": 1
},

{
"email": """
Subject: Shared File Access Expiring

Re-authenticate access:
https://file-share-security.net
""",
"label": 1
},

# =========================
# 🟢 LEGIT (0)
# =========================

{
"email": "Team meeting tomorrow at 10am in Conference Room B.",
"label": 0
},

{
"email": "Updated syllabus has been posted on Blackboard.",
"label": 0
},

{
"email": "Project status report attached for review.",
"label": 0
},

{
"email": "Reminder: faculty workshop next Thursday.",
"label": 0
},

{
"email": "Monthly newsletter is now available on the university site.",
"label": 0
},

{
"email": "Your expense reimbursement has been processed.",
"label": 0
},

{
"email": "Please submit final project documentation by Monday.",
"label": 0
},

{
"email": "Research meeting moved to 3 PM Thursday.",
"label": 0
},

{
"email": "Class schedule updated for Fall semester.",
"label": 0
},

{
"email": "IT maintenance scheduled for Sunday 2AM–4AM.",
"label": 0
},

{
"email": "Campus library hours have been updated.",
"label": 0
},

{
"email": "Faculty lunch event scheduled for Friday noon.",
"label": 0
},

{
"email": "Your parking permit renewal is complete.",
"label": 0
},

{
"email": "Academic advising appointments are now open.",
"label": 0
},

{
"email": "Blackboard system update completed successfully.",
"label": 0
},

# =========================
# ⚠️ EDGE CASES (0 but tricky)
# =========================

{
"email": """
Subject: Microsoft Security Notification

We noticed unusual activity.
If this was you, no action is needed.
Login here:
https://account.microsoft.com
""",
"label": 0
},

{
"email": """
Subject: Phishing Simulation Training

This is a security awareness exercise.
Do not enter credentials.
""",
"label": 0
},

{
"email": """
Subject: Google Form Request (Internal Survey)

Please complete this internal survey form for HR feedback.
""",
"label": 0
},

{
"email": """
Subject: Password Reset Request

If you requested this, continue:
https://account.microsoft.com/password
Otherwise ignore.
""",
"label": 0
},

{
"email": """
Subject: Urgent but Legit System Maintenance

System update will occur tonight.
No action required.
""",
"label": 0
},

{
"email": """
Subject: Invoice Attached for Review

Please review attached invoice PDF.
""",
"label": 0
},

{
"email": """
Subject: Zoom Meeting Invitation

Join meeting at scheduled time:
https://zoom.us/j/123456
(no action required before meeting time)
""",
"label": 0
},

{
"email": """
Subject: Security Awareness Reminder

Never share credentials via email or forms.
""",
"label": 0
},

{
"email": """
Subject: HR Update - Policy Changes

New HR policy document attached.
""",
"label": 0
},

{
"email": """
Subject: Google Drive Shared Document

A document has been shared with you by a colleague.
""",
"label": 0
},

]