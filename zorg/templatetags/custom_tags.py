from django import template
from django.utils.html import format_html
from django.urls import reverse

register = template.Library()


@register.simple_tag(takes_context=True)
def side_nav_heading(context, heading):
    return format_html("<div class='bws-sidenav-menu-heading'>{}</div>", heading)


@register.simple_tag(takes_context=True)
def side_nav_link(context, url, icon, label):
    try:
        cur_url = f"{context['request'].resolver_match.app_names[0]}:{context['request'].resolver_match.url_name}"
    except IndexError:
        cur_url = f"{context['request'].resolver_match.url_name}"
    active = "active" if cur_url == url else ""
    template_str = f"""
        <a class="nav-link {active}" href="{reverse(url)}">
                <div class="bws-nav-link-icon"><i class="bi bi-{icon}"></i></div>
                {label}
        </a>
    """
    return format_html(template_str, url, icon, label)


@register.simple_block_tag(takes_context=True, end_name="end_side_nav_drop_down")
def side_nav_drop_down(context, content, id, root_id, drop_down_label, drop_down_icon):
    html_str = """<a data-bs-target='#{id}'
        class='nav-link collapsed'
        href='#'
        data-bs-toggle='collapse'
        aria-expanded='false'
        aria-controls='{id}'>
        <div class='bws-nav-link-icon'><i class='bi bi-{drop_down_icon}'></i></div>
        {drop_down_label}
        <div class='bws-sidenav-collapse-arrow'><i class='bi bi-chevron-double-down'></i></div>
    </a>
    <div id='{id}' class='collapse' data-bs-parent='#{root_id}'><nav class='bws-sidenav-menu-nested nav'>{content}</nav></div>
    """
    return format_html(
        html_str,
        content=content,
        id=id,
        root_id=root_id,
        drop_down_label=drop_down_label,
        drop_down_icon=drop_down_icon,
    )
