import json
import random

# -----------------------------
# Phishing patterns (varied SOC realism)
# -----------------------------
phishing_templates = [
    "Urgent: verify your {brand} account immediately at {link}",
    "Your {brand} account has been suspended due to suspicious activity. login now {link}",
    "Security alert: unauthorized login detected. confirm identity {link}",
    "Password expired. reset immediately using {link}",
    "Unusual activity detected on your account. verify now {link}",
    "Your payment failed. update billing information {link}",
    "We locked your account for safety. verify access {link}",
    "Critical security update required. click here {link}"
]

# -----------------------------
# Legit patterns
# -----------------------------
legit_templates = [
    "Hey, here is the meeting agenda for tomorrow",
    "Your package has shipped and will arrive on Friday",
    "Please review the attached project document",
    "Team standup notes are attached",
    "Lunch meeting moved to 2pm today",
    "Here is the report you requested",
    "Calendar invite for weekly sync",
    "Project update: milestone completed"
]

# -----------------------------
# Context data
# -----------------------------
brands = ["PayPal", "Microsoft", "Google", "Apple", "Amazon", "Netflix", "Facebook"]
links = [
    "http://secure-login.com",
    "http://verify-account.net",
    "http://security-check.org",
    "http://account-update.com",
    "http://login-required.net"
]

edge_cases = [
    "Your account update may be required",
    "Security notice regarding your login activity",
    "Please confirm recent changes",
    "System alert: action may be needed",
    "We noticed unusual sign-in behavior"
]

# -----------------------------
# Generate phishing
# -----------------------------
def generate_phishing(n):
    data = []
    for _ in range(n):
        template = random.choice(phishing_templates)
        email = template.format(
            brand=random.choice(brands),
            link=random.choice(links)
        )
        data.append({"email": email, "label": "phishing"})
    return data

# -----------------------------
# Generate legit
# -----------------------------
def generate_legit(n):
    data = []
    for _ in range(n):
        email = random.choice(legit_templates)
        data.append({"email": email, "label": "legit"})
    return data

# -----------------------------
# Edge cases
# -----------------------------
def generate_edge(n):
    data = []
    for _ in range(n):
        data.append({
            "email": random.choice(edge_cases),
            "label": "edge"
        })
    return data

# -----------------------------
# Save helper
# -----------------------------
def save(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

# -----------------------------
# MAIN
# -----------------------------
if __name__ == "__main__":

    phishing = generate_phishing(1450)
    legit = generate_legit(1450)
    edge = generate_edge(100)

    save("data/phishing_samples.json", phishing)
    save("data/legit_samples.json", legit)
    save("data/edge_cases.json", edge)

    print("✅ Dataset generated:")
    print("Phishing:", len(phishing))
    print("Legit:", len(legit))
    print("Edge:", len(edge))
    print("TOTAL:", len(phishing) + len(legit) + len(edge))