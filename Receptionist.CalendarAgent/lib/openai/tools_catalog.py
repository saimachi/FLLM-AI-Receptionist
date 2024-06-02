"""
Tool reference for the CalendarScheduler agent.
"""
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_calendar_events_today",
            "description": "List basic information about today's calendar events.",
            "parameters": {},
        },
    }
]


METHOD_SIGNATURES = {
    "get_calendar_events_today": []
}