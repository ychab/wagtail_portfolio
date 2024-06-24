from django import template

register = template.Library()


@register.inclusion_tag("core/cookies_banner.html", takes_context=True)
def cookies_banner(context):  # pragma: no cover
    return {
        "cookie_title": context["settings"]["core"]["portfoliosettings"].cookie_title,
        "cookie_text": context["settings"]["core"]["portfoliosettings"].cookie_text,
    }
