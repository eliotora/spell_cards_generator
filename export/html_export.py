from jinja2 import Environment, FileSystemLoader
from os import getcwd
from model.detailable_model import DetailableModel, MODEL_EXPORT_MODE_HTML_FILES
from model.generic_model import ExportOption

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
                    f"NIVEAU {spell["level"]}" if spell["level"] > 0 else "SORTS MINEURS"
                ),
            }
            spells.insert(i, new_spell)
            i += 1
    return spells


def determine_card_size(spells):  # TODO: A refaire
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


def html_export(
    items: list[DetailableModel],
    path,
    mode=ExportOption.RULES.value,
    show_source=False,
    show_VO_name=False,
    data_type=DetailableModel,
):
    env = Environment(loader=FileSystemLoader("export/html_templates"))

    template_path = MODEL_EXPORT_MODE_HTML_FILES[(data_type.__name__.lower(), mode)]
    template = env.get_template(template_path)

    style_path = f"file:///{getcwd()}/styles/style.css"
    background_image_path = f"file:///{getcwd().replace("\\", "/")}/images/fond-ph.jpg"

    data = [i.to_html_dict() for i in items]

    if mode == ExportOption.GRIMOIRE.value:
        data = sort_by_level(data)

    if mode == ExportOption.CARDS.value:
        data = determine_card_size(data)
        color = data_type.color

    html = template.render(
        data_class=data_type.__name__,
        data=data,
        show_VO_name=show_VO_name,
        show_source=show_source,
        style_path=style_path,
        background_image_path=background_image_path,
        color=color
    )

    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
