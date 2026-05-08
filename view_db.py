from app import app, db
from models import ContactMessage, VisitorLog
from sqlalchemy import desc

def view_data():
    with app.app_context():
        print("\n--- RECENT MESSAGES ---")
        messages = ContactMessage.query.order_by(desc(ContactMessage.timestamp)).limit(5).all()
        for m in messages:
            print(f"[{m.timestamp}] {m.name} ({m.email}): {m.subject} -> {m.message[:50]}...")

        print("\n--- RECENT VISITOR LOGS ---")
        logs = VisitorLog.query.order_by(desc(VisitorLog.timestamp)).limit(10).all()
        for l in logs:
            print(f"[{l.timestamp}] IP: {l.ip_address} | Path: {l.path}")

if __name__ == "__main__":
    view_data()
