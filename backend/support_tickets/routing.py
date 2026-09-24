from .models import Agent


def assign_agent(category):
    suitable_agents = []

    agents = Agent.objects.filter(is_available=True)

    for agent in agents:
        if category in agent.skills and agent.current_load < agent.capacity:
            suitable_agents.append(agent)

    if not suitable_agents:
        return None

    # Select the agent with the lowest current workload
    suitable_agents.sort(key=lambda agent: agent.current_load)

    selected_agent = suitable_agents[0]

    # Increase workload
    selected_agent.current_load += 1
    selected_agent.save(update_fields=["current_load"])

    return selected_agent.name