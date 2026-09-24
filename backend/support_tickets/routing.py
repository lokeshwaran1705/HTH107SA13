AGENTS = [
    {
        "name": "Priya",
        "skills": ["payment", "refund"],
        "load": 2,
        "capacity": 5,
    },
    {
        "name": "Arun",
        "skills": ["technical", "login"],
        "load": 1,
        "capacity": 5,
    },
    {
        "name": "Karthik",
        "skills": ["delivery", "account"],
        "load": 4,
        "capacity": 5,
    },
    {
        "name": "Meena",
        "skills": ["payment", "account"],
        "load": 1,
        "capacity": 5,
    },
]


def assign_agent(category):
    suitable_agents = [
        agent
        for agent in AGENTS
        if category in agent["skills"]
        and agent["load"] < agent["capacity"]
    ]

    if not suitable_agents:
        return None

    suitable_agents.sort(key=lambda agent: agent["load"])

    return suitable_agents[0]["name"]