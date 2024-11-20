from django.db import models


def agent_directory_path(instance, filename):
    return 'agent_{0}/{1}'.format(instance.agent.name, filename)

class Agent(models.Model):
    name = models.CharField(max_length=70)
    description = models.CharField(max_length=500)

    def __str__(self):
        return self.name
    
class AgentImages(models.Model):
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to=agent_directory_path)

    def __str__(self):
        return self.agent.name