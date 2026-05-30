import json
import random
import os

os.makedirs("data", exist_ok=True)

# ----------------------------
# Templates
# ----------------------------
phishing_templates = [
    "Urgent: verify your account at http://fake-login{0}.com",
    "Your account has been suspended. login immediately http://secure{0}.net",
    "Action required: confirm password at http://update{0}.org",
    "PayPal alert: verify identity http://paypal-secure{0}.com",
    "Microsoft security alert: login here http://microsoft-secure{0}.net"
]

legit_templates = [
    "Hey, meeting is scheduled for tomorrow at 10am",
    "Your package will arrive on Friday via UPS",
    "Please review the attached project document",
    "Lunch meeting moved to next week",
    "Here is the report you requested"
]

edge_templates = [
    "Your account activity summary is available",
    "We noticed unusual sign-in activity, please review",
    "Team update: please check recent changes in your account"
]

# ----------------------------
# Builders
# ----------------------------
def make_phishing(i):
    return {
        "email": random.choice(phishing_templates).format(i),
        "label": "phishing"
    }

def make_legit(i):
    return {
        "email": random.choice(legit_templates),
        "label": "legit"
    }

def make_edge(i):
    return {
        "email": random.choice(edge_templates),
        "label": "edge_case"
    }

# ----------------------------
# Generate dataset (300 total target)
# ----------------------------
phishing = [make_phishing(i) for i in range(150)]
legit = [make_legit(i) for i in range(150)]
edge = [make_edge(i) for i in range(30)]

# ----------------------------
# Save files
# ----------------------------
with open("data/phishing_samples.json", "w") as f:
    json.dump(phishing, f, indent=2)

with open("data/legit_samples.json", "w") as f:
    json.dump(legit, f, indent=2)

with open("data/edge_cases.json", "w") as f:
    json.dump(edge, f, indent=2)

print("✅ Dataset generated:")
print("Phishing:", len(phishing))
print("Legit:", len(legit))
print("Edge:", len(edge))
print("TOTAL:", len(phishing) + len(legit) + len(edge))