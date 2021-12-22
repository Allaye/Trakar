from datetime import datetime, timezone
from django.db import models
from employee.models import Employee
# Create your models here.


# Create your models here.
class Project(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=False, null=False, max_length=400, default="")
    technology = models.JSONField()
    members = models.ManyToManyField(Employee)
    start_date = models.DateField(default=datetime.now)
    end_date = models.DateField(blank=True, null=True)

    class Meta:
        ordering = ['start_date']


class ProjectActivity(models.Model):
    id = models.AutoField(primary_key=True)
    description = models.TextField(blank=False, null=False, max_length=400, default="")
    project = models.ForeignKey(to=Project, on_delete=models.CASCADE)
    user = models.ForeignKey(to=Employee, on_delete=models.CASCADE)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(blank=True, null=True)
    # activity_duration = models.DurationField(blank)


    def __str__(self):
        """
        convert to a string representation

        Returns:
            string: string representation of the object
                " <title>  : <project> : <user> : <startdate>  : <enddate>"
        """
        if self.end_time is None:
            return f"{self.description} : {self.project.title} : {self.user.username} : {self.start_time} : {'Activity in progress'}"
        else:
            return f"{self.description} : {self.project.title} : {self.user.username} : {self.start_time} : {self.end_time}"

    

    @property
    def is_running(self):
        """
        check if the activity is running

        Returns:
            bool: True if the activity is running, False otherwise
        """
        return self.end_time is None

    @property
    def duration(self):
        """
        get the duration of the activity

        Returns:
            timedelta: duration of the activity
        """
        if self.is_running:
            return round(int(datetime.now(timezone.utc) - self.start_time))
        else:
            return round(int(self.end_time - self.start_time))