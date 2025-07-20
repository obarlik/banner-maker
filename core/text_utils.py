def get_text_width(font, text):
    try:
        return font.getlength(text)
    except AttributeError:
        return font.getsize(text)[0] 