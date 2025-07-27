from jinja2 import Template, Environment, FileSystemLoader
from os import getcwd
from model.detailable_model import DetailableModel, MODEL_EXPORT_MODE_HTML_FILES
from model.generic_model import ExplorableModel, ExportOption
from model.feat_model import Feat
from model.spell_model import Spell
from model.maneuvers_model import Maneuver

SPELL = "spell"
FEAT = "feat"
MANEUVER = "maneuver"

export_type_dict = {Feat: FEAT, Spell: SPELL, Maneuver: MANEUVER}


spell_template_rules = """
<html>
<head>
    <meta charset="utf-8">
    <title>List » Spells - DnD 5e</title>
    <link rel="stylesheet" href={{ style_path }}>
    <style>
        body	{background:white url("{{background_image_path}}") repeat}
        .blocCarte h1	{background-color:#6D0000; color:white}
        .bloc table tr:nth-child(even) {background-color:#e0e0ff}
    </style>
</head>
<body>
    <div class="titre1">Sorts D&D 5</div>
    <div class="cols2">
        {% for row in data %}
            <div class="bloc">
                <h1>{{ row["name"] }}</h1>
                {% if show_VO_name %}
                <div class="trad">[ {{ row["vo_name"].capitalize() }} ]</div>
                {% endif %}
                <div class="ecole">niveau {{ row["level"] }} - {{ row["school"] }} {% if row["ritual"] %}(rituel){% endif %}</div>
                <div><strong>Temps d'incantation</strong> : {{ row["casting_time"] }}</div>
                <div><strong>Portée</strong> : {{ row["range"] }}</div>
                <div><strong>Composantes</strong> : {{ row["components"] }}</div>
                <div><strong>Durée</strong> : {{ row["duration"] }}</div>
                <div class="description"> {{ row["description"] }}
                    {% if row["at_higher_levels"] %}
                        <strong><em>Aux niveaux supérieurs. </em></strong> : {{ row["at_higher_levels"] }}
                    {% endif %}
                </div>
                {% if show_source %}
                {% for class_name in row["classes"] %}
                    <div class="classe">{{ class_name }}</div>
                {% endfor %}
                <div class="source">{{ row["source"] }}</div>
                {% endif %}
            </div>
        {% endfor %}
    </div>
</body></html>
"""

spell_template_grimoire = """
<html>
<head>
    <meta charset="utf-8">
    <title>List » Spells - DnD 5e</title>
    <link rel="stylesheet" href={{ style_path }}>
    <style>
        body	{background:white url({{background_image_path}}) repeat}
        .blocCarte h1	{background-color:#6D0000; color:white}
        .bloc table tr:nth-child(even) {background-color:#e0e0ff}
    </style>
</head>
<body>
    <div class="titre1">Grimoire</div>
    <div class="cols2">
        {% for row in data %}
        {% if row['bandeaulvl'] %}<div class="niveau">{{ row['text'] }}</div>
        {% else %}
            <div class="bloc">
                <h1>{{ row['name'] }}</h1>
                {% if show_VO_name %}
                <div class="trad">[ {{ row.get('vo_name', '').capitalize() }} ]</div>
                {% endif %}
                <div class="ecole">niveau {{ row['level'] }} - {{ row['school'] }} {% if row['ritual'] %}(rituel){% endif %}</div>
                <div><strong>Temps d'incantation</strong> : {{ row["casting_time"] }}</div>
                <div><strong>Portée</strong> : {{ row['range'] }}</div>
                <div><strong>Composantes</strong> : {{ row['components'] }}</div>
                <div><strong>Durée</strong> : {{ row['duration'] }}</div>
                <div class="description"> {{ row['description'] }}
                    {% if row['at_higher_levels'] %}
                        <strong><em>Aux niveaux supérieurs. </em></strong> : {{ row['at_higher_levels'] }}
                    {% endif %}
                </div>
                {% if show_source %}
                {% for class_name in row.get('classes', []) %}
                    <div class="classe">{{ class_name }}</div>
                {% endfor %}
                <div class="source">{{ row.get('source') }}</div>
                {% endif %}
            </div>
        {% endif %}
        {% endfor %}
    </div>
</body></html>
"""

spell_template_cards = """
<html>
<head>
    <meta charset="utf-8">
    <title>List » Spells - DnD 5e</title>
    <link rel="stylesheet" href={{ style_path }}>
    <style>
        body	{background:white url( {{ background_image_path }} ) repeat}
        .blocCarte h1	{background-color:#6D0000; color:white}
        .bloc table tr:nth-child(even) {background-color:#e0e0ff}
    </style>
</head>
<body style="background-image:none; max-width:none">
    <div class="blocCarteContainer">
    {% for row in data %}
        <div class="blocCarte {{ row['card_size'] }}">
            <h1>{{ row['name'] }}</h1>
            <div class="ecole">niveau {{ row['level'] }} - {{ row['school'] }} {% if row['ritual'] %}(rituel){% endif %}</div>
            <div><strong>Temps d'incantation</strong> : {{ row["casting_time"] }}</div>
            <div><strong>Portée</strong> : {{ row['range'] }}</div>
            <div><strong>Composantes</strong> : {{ row['components'] }}</div>
            <div><strong>Durée</strong> : {{ row['duration'] }}</div>
            <div class="description"> {{ row['description'] }}
                {% if row['at_higher_levels'] %}
                    <strong><em>Aux niveaux supérieurs. </em></strong> : {{ row['at_higher_levels'] }}
                {% endif %}
            </div>
            {% if show_source %}
            <div class="source">{{ row.get('source') }}</div>
            {% endif %}
        </div>
    {% endfor %}
    </div>
</body></html>
"""

feat_template_rules = """
<html>
<head>
    <meta charset="utf-8">
    <title>List » Feats - DnD 5e</title>
    <link rel="stylesheet" href={{ style_path }}>
    <style>
        body	{background:white url("{{background_image_path}}") repeat}
        .blocCarte h1	{background-color:#6D0000; color:white}
        .bloc table tr:nth-child(even) {background-color:#e0e0ff}
    </style>
</head>
<body>
    <div class="titre1">Dons D&D 5</div>
    <div class="cols2">
        {% for row in data %}
            <div class="bloc">
                <h1>{{ row['name'] }}</h1>
                {% if show_vo_name %}
                <div class="trad">[ {{ row.get('vo_name', '').capitalize() }} ]</div>
                {% endif %}
                <div class="description"> {{ row['description'] }}</div>
                {% if show_source %}
                {% for class_name in row.get('classes', []) %}
                    <div class="classe">{{ class_name }}</div>
                {% endfor %}
                <div class="source">{{ row.get('source') }}</div>
                {% endif %}
            </div>
        {% endfor %}
    </div>
</body></html>
"""

feat_template_cards = """
<html>
<head>
    <meta charset="utf-8">
    <title>List » Feats - DnD 5e</title>
    <link rel="stylesheet" href={{ style_path }}>
    <style>
        body	{background:white url( {{ background_image_path }} ) repeat}
        .blocCarte h1	{background-color:#C93C0C; color:white}
        .bloc table tr:nth-child(even) {background-color:#e0e0ff}
    </style>
</head>
<body style="background-image:none; max-width:none">
    <div class="blocCarteContainer">
    {% for row in data %}
        <div class="blocCarte {{ row['card_size'] }}">
            <h1>{{ row['name'] }}</h1>
            <div class="description"> {{ row['description'] }}
            </div>
            {% if show_source %}
            <div class="source">{{ row.get('source') }}</div>
            {% endif %}
        </div>
    {% endfor %}
    </div>
</body></html>
"""


def sort_by_level(spells):
    """
    Sorts spells by their level.
    """
    spells = sorted(spells, key=lambda x: (x["level"], x["name"]))
    current_level = -1
    for i, spell in enumerate(spells):
        if spell["level"] > current_level:
            current_level = spell["level"]
            new_spell = {
                "bandeaulvl": True,
                "text": (
                    f'NIVEAU {spell["level"]}'
                    if spell["level"] > 0
                    else "SORTS MINEURS"
                ),
            }
            spells.insert(i, new_spell)
            i += 1
    return spells


def determine_card_size(spells):
    """
    Determines the card size based on the number of spells.
    """
    sized_spells = []
    for spell in spells:
        sized_spell = spell.copy()
        total_length = len(sized_spell["main_text"])
        if "à_niveau_supérieur" in sized_spell:
            total_length += len(sized_spell["à_niveau_supérieur"])

        if total_length > 1250:
            sized_spell["card_size"] = "blocCarte blocCarteTTP"
        elif total_length > 800:
            sized_spell["card_size"] = "blocCarte blocCarteTP"
        elif total_length > 400:
            sized_spell["card_size"] = "blocCarte blocCarteP"
        else:
            sized_spell["card_size"] = "blocCarte"
        sized_spells.append(sized_spell)
    return sized_spells


#### NEW


def html_export(
    items: list[ExplorableModel],
    path,
    mode=ExportOption.RULES,
    show_source=False,
    show_VO_name=False,
    data_type=None,
):
    if not items or not data_type:
        return

    data_type = export_type_dict[data_type]

    processed_items = []
    for item in items:
        data = item.to_dict()
        data["description"] = data["description"].replace("\n", "<br>")
        if data["description"][-4:] != "<br>":
            data["description"] += "<br>"
        if "at_higher_levels" in data:
            data["at_higher_levels"] = data.get("at_higher_levels", "").replace(
                "\n", "<br>"
            )
        if "components" in data:
            data["components"] = ", ".join(data["components"])
        processed_items.append(data)
    items = processed_items

    if data_type == SPELL:
        if mode == ExportOption.RULES:
            template = Template(spell_template_rules)
        elif mode == ExportOption.GRIMOIRE:
            items = sort_by_level(items)
            template = Template(spell_template_grimoire)
        elif mode == ExportOption.CARDS:
            items = determine_card_size(items)
            template = Template(spell_template_cards)
    elif data_type == FEAT:
        if mode == ExportOption.RULES:
            template = Template(feat_template_rules)
        elif mode == ExportOption.CARDS:
            items = determine_card_size(items)
            template = Template(feat_template_cards)

    style_path = f"file:///{getcwd()}/styles/style.css"
    background_image_path = f"file:///{getcwd().replace("\\", "/")}/images/fond-ph.jpg"

    html = template.render(
        data=items,
        show_source=show_source,
        show_VO_name=show_VO_name,
        style_path=style_path,
        background_image_path=background_image_path,
    )
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)


type_mode_template={
    (Spell.__name__, ExportOption.RULES): "spell_rules.html",
    (Spell.__name__, ExportOption.GRIMOIRE): "spell_grimoire.html",
    (Spell.__name__, ExportOption.CARDS): "spell_cards.html",
    (Feat.__name__, ExportOption.RULES): "feat_rules.html",
    (Feat.__name__, ExportOption.CARDS): "generic_cards.html"
}

def html_export2(
    items: list[DetailableModel],
    path,
    mode=ExportOption.RULES.value,
    show_source=False,
    show_VO_name=False,
    data_type=None,
):
    env = Environment(loader=FileSystemLoader('export/html_templates'))


    template_path = MODEL_EXPORT_MODE_HTML_FILES[(data_type.__name__.lower(), mode)]
    template = env.get_template(template_path)

    style_path = f"file:///{getcwd()}/styles/style.css"
    background_image_path = f"file:///{getcwd().replace("\\", "/")}/images/fond-ph.jpg"

    data = [i.to_html_dict() for i in items]

    if mode == ExportOption.CARDS.value:
        data = determine_card_size(data)

    html = template.render(
        data_class=data_type.__name__,
        data=data,
        show_VO_name=show_VO_name,
        show_source=show_source,
        style_path=style_path,
        background_image_path=background_image_path
    )

    with open(path, "w", encoding="utf-8") as f:
        f.write(html)

