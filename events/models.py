from django.db import models
from django.utils import timezone
import datetime
class Event(models.Model):
	PY = 'primary'
	SY = 'secondary'
	SS = 'success'
	DR = 'danger'
	WG = 'warning'
	IO = 'info'
	DK = 'dark'

	event_category_choices = [
		(PY,'Primary Event'),
	(SY,'Secondary Event'),
	(SS,'Success Event'),
	(DR,'Important Event'),
	(WG,'Awareness Event'),
	(IO,'Informative Event'),
	(DK,'Party Event'),
	]
	lorem_txt = '''Lorem ipsum dolor sit amet, consectetur adipiscing elit. Quisque et risus ac ligula convallis vulputate in eu dui. Fusce in velit luctus mauris eleifend luctus eget interdum enim. Aenean id massa ornare, bibendum turpis quis, imperdiet sapien. Mauris egestas commodo tellus, eu tincidunt ex bibendum in. Nullam eros urna, consectetur quis viverra quis, aliquet nec lorem. Cras quis magna sed sapien tempor viverra eget vitae nisi. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Nullam convallis felis ac enim pretium luctus. Phasellus sit amet sapien blandit, volutpat metus et, sagittis risus. In elit metus, sodales non pulvinar quis, volutpat vel velit. Nunc efficitur fringilla lacus eu suscipit. Nulla condimentum sollicitudin enim sit amet scelerisque. Cras vehicula sed odio ac dapibus. Sed et neque justo.

Aliquam vitae magna ex. Vivamus aliquet lorem a ligula porta ultricies. Donec quam diam, luctus ac luctus et, elementum a nisl. Pellentesque elit libero, aliquam ut lectus id, fringilla mattis ipsum. Vestibulum varius, tortor sit amet pulvinar scelerisque, nisl enim mollis leo, ac ornare odio sem mollis augue. Nunc finibus tincidunt ex. Duis id gravida sapien. In dignissim vestibulum risus, vitae fringilla tortor varius in.

Nullam imperdiet nibh quis ipsum pulvinar ultricies. Donec aliquet ultrices porttitor. Nulla imperdiet est vel lacinia finibus. Aliquam ut diam nec erat pellentesque sagittis. Maecenas tincidunt, massa luctus eleifend bibendum, orci mauris vehicula diam, vel imperdiet massa odio ut nunc. Pellentesque porta, sapien a molestie rutrum, neque turpis bibendum mi, sit amet imperdiet eros velit et orci. Cras quis quam pretium, auctor odio vehicula, volutpat orci. In auctor felis sed ipsum sagittis, quis vestibulum lorem viverra. Mauris sem ante, vestibulum eu erat eu, imperdiet tempus tortor. Vivamus dignissim magna id quam dapibus volutpat. Mauris id rhoncus massa, eu dictum quam.'''


	title = models.CharField(max_length = 100,default="Enter the title Here")
	shrt_text = models.CharField(max_length = 250,default="Say something within 200 words")
	long_text = models.TextField(default=lorem_txt)	
	start_date = models.DateTimeField(default=timezone.now())
	end_date = models.DateTimeField(default=(timezone.now() + datetime.timedelta(days=3)))
	event_category = models.CharField(
        max_length=20,
        choices=event_category_choices,
        default=PY,
    )

	def __str__(self):
		return self.title