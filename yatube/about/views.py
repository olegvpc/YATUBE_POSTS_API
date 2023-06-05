from django.views.generic.base import TemplateView


class AboutAuthorView(TemplateView):
    # template_name = 'about/author.html'
    template_name = 'about/portfolio.html'

class AboutAuthorViewEng(TemplateView):
    # template_name = 'about/author.html'
    template_name = 'about/portfolio-en.html'


class AboutTechView(TemplateView):
    template_name = 'about/tech.html'
