from jinja2 import Template

spell_template_rules = """
<html>
<head>
    <meta charset="utf-8">
    <title>List » Spells - DnD 5e</title>
    <link rel="stylesheet" href="style.css?v=5">
    <style>
        body	{background:white url("../images/fond-ph.jpg") repeat}
        .blocCarte h1	{background-color:#6D0000; color:white}
        .bloc table tr:nth-child(even) {background-color:#e0e0ff}
    </style>
</head>                  
<body>
    <div class="titre1">Sorts D&D 5</div>
    <div class="cols2">
        {% for row in data %}
            <div class="bloc">
                <h1>{{ row['nom'] }}</h1>
                <div class="ecole">niveau {{ row['niveau'] }} - {{ row['école'] }} {% if row['rituel'] %}(rituel){% endif %}</div>
                <div><strong>Temps d'incantation</strong> : {{ row["temps_d'incantation"] }}</div>
                <div><strong>Portée</strong> : {{ row['portée'] }}</div>
                <div><strong>Composantes</strong> : {{ row['composantes'] }}</div>
                <div><strong>Durée</strong> : {{ row['durée'] }}</div>
                <div class="description"> {{ row['description'] }}
                    <br>
                    {% if row['à_niveau_supérieur'] %}
                        <strong><em>Aux niveaux supérieurs. </em></strong> : {{ row['à_niveau_supérieur'] }}
                    {% endif %}
                </div>
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
    <link rel="stylesheet" href="style.css?v=5">
    <style>
        body	{background:white url("../images/fond-ph.jpg") repeat}
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
                <h1>{{ row['nom'] }}</h1>
                <div class="ecole">niveau {{ row['niveau'] }} - {{ row['école'] }} {% if row['rituel'] %}(rituel){% endif %}</div>
                <div><strong>Temps d'incantation</strong> : {{ row["temps_d'incantation"] }}</div>
                <div><strong>Portée</strong> : {{ row['portée'] }}</div>
                <div><strong>Composantes</strong> : {{ row['composantes'] }}</div>
                <div><strong>Durée</strong> : {{ row['durée'] }}</div>
                <div class="description"> {{ row['description'] }}
                    <br>
                    {% if row['à_niveau_supérieur'] %}
                        <strong><em>Aux niveaux supérieurs. </em></strong> : {{ row['à_niveau_supérieur'] }}
                    {% endif %}
                </div>
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
    <link rel="stylesheet" href="style.css?v=5">
    <style>
        body	{background:white url("../images/fond-ph.jpg") repeat}
        .blocCarte h1	{background-color:#6D0000; color:white}
        .bloc table tr:nth-child(even) {background-color:#e0e0ff}
    </style>
</head>                  
<body style="background-image:none; max-width:none">
    {% for row in data %}
        <div class="{{ row['card_size'] }}">
            <h1>{{ row['nom'] }}</h1>
            <div class="ecole">niveau {{ row['niveau'] }} - {{ row['école'] }} {% if row['rituel'] %}(rituel){% endif %}</div>
            <div><strong>Temps d'incantation</strong> : {{ row["temps_d'incantation"] }}</div>
            <div><strong>Portée</strong> : {{ row['portée'] }}</div>
            <div><strong>Composantes</strong> : {{ row['composantes'] }}</div>
            <div><strong>Durée</strong> : {{ row['durée'] }}</div>
            <div class="description"> {{ row['description'] }}
                <br>
                {% if row['à_niveau_supérieur'] %}
                    <strong><em>Aux niveaux supérieurs. </em></strong> : {{ row['à_niveau_supérieur'] }}
                {% endif %}
            </div>
        </div>
    {% endfor %}
</body></html>
"""

def html_export(spells, path, mode='rules'):
    if not spells:
        return

    processed_spells = []
    for spell in spells:
        processed = spell.copy()
        processed['description'] = processed['description'].replace('\n', '<br>')
        processed['à_niveau_supérieur'] = processed.get('à_niveau_supérieur', '').replace('\n', '<br>')
        processed['composantes'] = ', '.join(processed['composantes'])
        processed_spells.append(processed)
    spells = processed_spells

    if mode == 'rules':
        template = Template(spell_template_rules)
    elif mode == 'grimoire':
        spells = sort_by_level(spells)
        template = Template(spell_template_grimoire)
    elif mode == 'cards':
        spells = determine_card_size(spells)
        template = Template(spell_template_cards)

    
    html = template.render(data=spells)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)

def sort_by_level(spells):
    """
    Sorts spells by their level.
    """
    spells = sorted(spells, key=lambda x: (x['niveau'], x['nom']))
    current_level = -1
    for i, spell in enumerate(spells):
        if spell['niveau'] > current_level:
            current_level = spell['niveau']
            new_spell = {
                "bandeaulvl": True,
                "text": f'NIVEAU {spell["niveau"]}' if spell['niveau'] > 0 else 'SORTS MINEURS',
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
        total_length = len(sized_spell['description'])
        if "à_niveau_supérieur" in sized_spell:
            total_length += len(sized_spell['à_niveau_supérieur'])
        
        if total_length > 1550:
            sized_spell["card_size"] = "blocCarte blocCarteTTP"
        elif total_length > 800:
            sized_spell["card_size"] = "blocCarte blocCarteTP"
        elif total_length > 500:
            sized_spell["card_size"] = "blocCarte blocCarteP"
        else:
            sized_spell["card_size"] = "blocCarte"
        sized_spells.append(sized_spell)
    return sized_spells
        