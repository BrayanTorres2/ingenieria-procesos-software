from google.cloud import language_v1

client = language_v1.LanguageServiceClient()

def analizar_sentimiento(texto):
    document = language_v1.Document(
        content=texto,
        type_=language_v1.Document.Type.PLAIN_TEXT,
        language="es"
    )

    response = client.analyze_sentiment(request={"document": document})
    score = response.document_sentiment.score

    if score > 0.25:
        return "Positivo"
    elif score < -0.25:
        return "Negativo"
    return "Neutral"
