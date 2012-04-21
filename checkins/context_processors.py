from django.conf import settings

def development_settings(request):
    context_extras = dict(
        TEMPLATE_DEBUG=settings.TEMPLATE_DEBUG,
        TWITTER_CONSUMER_KEY=getattr(settings, 'TWITTER_CONSUMER_KEY', None),
        GA_UID=getattr(settings, 'GA_UID', None),
        GOOGLE_API_KEY=getattr(settings, 'GOOGLE_API_KEY', None),
        )
    return context_extras
