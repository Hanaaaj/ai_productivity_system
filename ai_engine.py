from datetime import datetime
import math

class StudyEngine:
    def generate_plan(self, module, exam_date, topics, daily_hours):
        today = datetime.today().date()
        days_remaining = (exam_date - today).days

        if days_remaining <= 0:
            raise ValueError("Exam date must be in the future.")

        topics_per_day = math.ceil(len(topics) / days_remaining)

        schedule = {}
        topic_index = 0

        for day in range(days_remaining):
            daily_topics = topics[topic_index: topic_index + topics_per_day]
            schedule[f"Day {day+1}"] = {
                "topics": daily_topics,
                "study_hours": daily_hours,
                "breaks": "20 min after every 60 min",
                "hydration": "Every 10 minutes",
                "exercise": "After 3 hours study"
            }
            topic_index += topics_per_day

        return {
            "module": module,
            "days_remaining": days_remaining,
            "topics_per_day": topics_per_day,
            "schedule": schedule
        }


class WorkEngine:
    def generate_focus_blocks(self, tasks, priorities):
        combined = list(zip(tasks, priorities))
        combined.sort(key=lambda x: x[1])

        blocks = []
        for task, priority in combined:
            blocks.append({
                "task": task,
                "focus_block": "90 minutes",
                "hydration_reminder": "Every 10 minutes",
                "screen_break": "5 min after 60 minutes",
                "priority": priority
            })
        return blocks


class HealthEngine:
    def calculate_wellness(self, hydration, exercise, sleep):
        score = (hydration * 2) + (exercise / 10) + (sleep * 3)
        return min(score, 100)
