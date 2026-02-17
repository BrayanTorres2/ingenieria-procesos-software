import re
import unicodedata

MIN_PALABRAS = 3

PALABRAS_GENERICAS = {
    "na", "n/a", "no aplica", "ninguno", "sin comentario",
    ".", "..", "...", "-", "--", "x", "xx", "ok", "none"
}

def normalizar_texto(texto):
    texto = texto.lower().strip()
    texto = unicodedata.normalize("NFKD", texto)
    return "".join(c for c in texto if not unicodedata.combining(c))

def es_solo_simbolos(texto):
    return not bool(re.search(r"[a-záéíóúñ]", texto))

def es_texto_basura(texto):
    return bool(re.fullmatch(r"(.)\1{4,}", texto)) or len(set(texto)) <= 2

def tiene_palabras_validas(texto):
    palabras = re.findall(r"[a-záéíóúñ]{3,}", texto)
    return len(palabras) >= MIN_PALABRAS
