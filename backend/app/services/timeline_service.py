from datetime import datetime

timeline = []


def add_timeline(title, description, impact=None):
    timeline.append({
        "time": datetime.now().strftime("%H:%M:%S"),
        "title": title,
        "description": description,
        "impact": impact or {}
    })


def get_timeline():
    return timeline[::-1]
