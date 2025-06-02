from jinja2 import Template

def exporter_html(data, fichier_html):
    if not data:
        return

    headers = list(data[0].keys())
    template = Template("""
    <html><body>
    <h1>Données JSON</h1>
    <table border="1">
        <tr>
        {% for h in headers %}<th>{{ h }}</th>{% endfor %}
        </tr>
        {% for row in data %}
        <tr>
            {% for h in headers %}<td>{{ row[h] }}</td>{% endfor %}
        </tr>
        {% endfor %}
    </table>
    </body></html>
    """)
    html = template.render(headers=headers, data=data)
    with open(fichier_html, 'w', encoding='utf-8') as f:
        f.write(html)
