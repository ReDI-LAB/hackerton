from dotenv import load_dotenv
import os
import requests
import json
import re

load_dotenv()

# --- 1. Get your API Key ---
# You can get a free API key from OpenRouter after creating an account at:
# https://openrouter.ai/
# Simply click "Create Account" and then find your API key in your account settings.
API_KEY = os.getenv("SECRET_KEY")

# The URL for the OpenRouter API endpoint
API_URL = "https://openrouter.ai/api/v1/chat/completions"

# --- 2. Define the System Message and RAG Data ---
# This message sets the persona or instructions for the model.
SYSTEM_PROMPT = """You are a helpful and friendly AI assistant you are helping a users to fill out a form. go through 
the context information and answer step by step the question from the user and then if none of the context is relevant 
return sorry no information is found. Don't make up the information"""

# This is a simple data source for demons
# tration purposes.
# In a real-world application, this would be a database or an index of documents.
KNOWLEDGE_BASE = {
    "Anmeldung bei der Meldebehörde": '''Anmeldung bei der Meldebehörde Erläuterungen zum Ausfüllen des Meldescheins Allgemeine Hinweise Der Meldeschein ist wahrheitsgemäß und vollständig in deutlicher Schrift auszufüllen zu unterschreiben und innerhalb von zwei Wochen nach dem Beziehen der Wohnung der Meldebehörde Gemeinde Verwaltungsgemeinschaft Stadt zuzuleiten Sie haben der Meldebehörde auf Verlangen die erforderlichen Auskünfte zu erteilen persönlich zu erscheinen und die zum Nachweis der Angaben erforderlichen Unterlagen vorzulegen Falls eine Antwort für Sie nicht zutrifft machen Sie bitte einen Strich Bitte kreuzen Sie falls Kästchen vorhanden sind zutreffende Antworten an Grundsätzlich ist für jede anzumeldende Person ein eigener Meldeschein zu verwenden Ehegatten Lebenspartner Eltern und minderjährige Kinder mit denselben bisherigen und künftigen Wohnungen sollen gemeinsam einen Meldeschein verwenden In diesem Fall genügt es wenn einer der Meldepflichtigen den Meldeschein unterschreibt Bei einer Anmeldung von mehr als Personen verwenden Sie bitte einen weiteren Meldeschein Die Anmeldung bei der Meldebehörde befreit nicht von der Verpflichtung den Wohnungswechsel ggf anderen Behörden z B der Kraftfahrzeugzulassungsstelle mitzuteilen Bei dekroniscie Aurenatsting it der Prung delaschist m ergeepass und soweit vorhanden Das Bundesmeldegesetz BMG räumt dem Betroffenen die Möglichkeit ein folgenden Datenübermittlungen und Auskunftserteilungen zu widersprechen an Parteien Wählergruppen und andere Träger von Wahlvorschlägen im Zusammenhang mit allgemeinen Wahlen und Abstimmungen auf staatlicher oder kommunaler Ebene Abs an öffentlichrechtliche Religionsgesellschaften wenn Sie als Familienangehöriger keiner oder nicht derselben öffentlichrechtlichen Religionsgesellschaft angehören wie Ihr Ehegatte oder Itenuberihung af de ientichtechtichen Reglonsgesalschaten Ihter Ellern u Wide sprechen Werden die Daten für Zwecke des Steuererhebungsrechts der jeweiligen öffentlichrechtlichen Religionsgesellschaft übermittelt gilt dieses Widerspruchsrecht nicht Abs Satz BMG über Alters und Ehejubiläen an Parteien Wählergruppen Mitglieder parlamentarischer Vertretungskörperschaften und Bewerber für diese sowie an Presse und Rundfunk Abs an Adressbuchverlage Abs BMG an das Bundesamt für das Personalmanagement der Bundeswehr zum Zweck der Übersendung von Informationsmaterial zum freiwilligen Wehrdienst Abs BMG i V m c Abs Soldatengesetz SG Soweit Sie der Erteilung einer Auskunft oder Datenübermittlung aus dem Melderegister in einem oder mehreren der genannten Fälle widersprechen wollen hält die Meldebehörde ein entsprechendes Formblatt Melderegisterauskünfte nach Abs BMG für Zwecke der Werbung oder des Adresshandels werden von der Meldebehörde nur erteilt wenn der Antragsteller erklärt dass Sie ihm gegenüber in die Übermittlung Ihrer Daten zu diesen Zwecken eingewilligt haben Ausfüllen des Meldescheins Einzugsdatum Reihenfolge Tag Monat Jahr Hauptwohnung ist die vorwiegend benutzte Wohnung des Einwohners Hauptwohnung eines verheirateten oder eine Lebenspartnerschaft führenden Einwohners der nicht dauernd getrennt lebt von seiner Familie oder seinem Lebenspartner ist die vorwiegend benutzte Wohnung der Familie oder der Lebenspartner Bei minderjährigen Personen ist die Hauptwohnung die Wohnung der Personensorgeberechtigten Leben die Personensorgeberechtigten getrennt ist Hauptwohnung die Wohnung des Personensorgeberechtigten Eltern die von dem Minderjährigen vorwiegend benutzt wird Bei einem entsprechenden Antrag gilt diese Regelung für behinderte Personen auch bis zur Vollendung des Lebensjahres und zwar auch dann wenn sie in einer Behinderteneinrichtung leben In Zweifelsfällen ist die vorwiegend benutzte Wohnung dort wo der Schwerpunkt der Lebensbeziehungen liegt Nebenwohnung ist jede weitere Wohnung im Bundesgebiet Familienname Es ist der vollständige aktuelle Familienname einschließlich der Namensbestandteile anzugeben Vornamen sind nur in der personenstandsrechtlich beurkundeten Form anzugeben Doktorgrad im Bundesgebiet erworben Für melderechtliche Zwecke ist lediglich die Angabe des Doktorgrades in der abgekürzten Form Dr ohne weiteren Zusatz z B med erforderlich Wenn er ehrenhalber verliehen ist ist der Zusatz h e h oder E h hinzuzufügen Doktorgrad im Ausland erworben Dieser kann in das Melderegister nur dann eingetragen werden wenn der Inhaber in der Bundesrepublik Deutschland zur Führung der Abkürzung Dr berechtigt ist Eine Aussage welche ausländischen akademischen Grade hiervon betroffen sind kann auf Grund der gesetzlichen Vorgaben des Bayerischen Hochschulgesetzes nicht generell erfolgen Die Prüfung der Führungsberechtigung und der damit verbundenen Eintragungsfähigkeit ins Melderegister kann nur bei einer Vorlage der Promotionsurkunde im Original und deren beglaubigter Übersetzung ins Deutsche erfolgen Geburtsdatum Reihenfolge Tag Monat Jahr Familienstand Hier ist der personenstandsrechtliche Familienstand anzugeben LD ledig VH verheiratet VW verwitwet GS geschieden LP eingetragene Lebenspartnerschaft LV Lebenspartner verstorben LA Lebenspartnerschaft aufgehoben Staatsangehörigkeit Personen mit mehrfacher Staatsangehörigkeit haben sämtliche Staatsangehörigkeiten Staatenlose ggf auch ihre letzte Staatsangehörigkeit anzugeben Religion Für melderechtliche Zwecke ist die Angabe der Zugehörigkeit zu einer öffentlichrechtlichen Religionsgesellschaft erforderlich Bitte verwenden Sie in folgenden Fällen die angegebenen Abkürzungen rk römischkatholisch ak altkatholisch ev evangelisch It evangelischlutherisch rf evangelischreformiert isby israelische Kultusgemeinden in Bayern oa keiner öffentlichrechtlichen Religionsgesellschaft angehörig Soweit Sie einer anderen öffentlichrechtlichen Religionsgesellschaft angehören ist deren vollständige Bezeichnung anzugeben Die Speicherung der Steueridentifikationsnummer oder der vorläufigen Bearbeitungsmerkmale beruht auf c des Einkommensteuergesetzes Pass und Ausweisdaten Für die Angabe der Art des Ausweisdokuments Personalausweis Reisepass Kinderreisepass verwenden Sie bitte die angegebenen Abkürzungen PA Personalausweis RP Reisepass KRP Kinderreisepass Gesetzliche Vertreter Die gesetzlichen Vertreter sind nur bei der Anmeldung von Minderjährigen und von Personen für die ein Betreuer bestellt ist der den Aufenthalt bestimmen kann anzugeben Die Angabe entfällt bei der gemeinsamen Anmeldung von Eltern und Kindern Umzug und Änderung der Anschrift Wohnsitzanmeldung Wenn Sie nach München ziehen müssen Sie sich so schnell wie möglich anmelden auch bei einer Ummeldung innerhalb der Stadt Der Gesetzgeber sieht Tage vor Wohnsitz abmelden Wenn Sie ins Ausland wegziehen eine Nebenwohnung aufgeben oder keinen festen Wohnsitz mehr haben müssen Sie sich abmelden Wohnsitzanmeldung Familie Wenn Sie als Familie nach München ziehen müssen Sie sich innerhalb von Tagen anmelden auch wenn Sie innerhalb der Stadt umziehen Adressänderung Personalausweis Reisepass eAT Wenn Sie innerhalb Münchens umziehen nach München ziehen oder sich Ihre Adresse geändert hat sollten Sie die Adresse in Ihren Ausweisdokumenten ändern lassen Zweitwohnungsteuer Wenn Sie oder Familienangehörige neben Ihrer Hauptwohnung weitere Wohnungen in München nutzen müssen Sie Zweitwohnungsteuern zahlen Befreiung von der Zweitwohnungsteuer Wenn die Summe Ihrer positiven Einkünfte vor zwei Jahren unter Euro lag können Sie sich für das aktuelle Jahr von der Zweitwohnungsteuer befreien lassen Änderung von Namen oder Geschlecht Namensänderung im Führerschein Nach einer Namensänderung empfehlen wir den Austausch des Führerscheins besonders bei Reisen ins Ausland er ist jedoch nicht zwingend vorgeschrieben Namensänderung in den Fahrzeugpapieren Wenn sich der Name der Person oder die Firmenbezeichnung auf die ein Fahrzeug zugelassen ist ändert muss dies in den Fahrzeugpapieren eingetragen werden Erklärung zur Reihenfolge der Vornamen Sie möchten die Reihenfolge Ihrer Vornamen ändern Dann können Sie das unter bestimmten Voraussetzungen beantragen Änderung der Personendaten im Melderegister Nach einer Heirat Scheidung oder Namensänderung im Ausland haben sich Ihre Personendaten geändert Dies müssen Sie ins Melderegister eintragen lassen Anpassung des Geschlechtseintrags und Vornamens Selbstbestimmungsgesetz Ihr amtlich eingetragenes Geschlecht entspricht nicht Ihrer Persönlichkeit Dann können Sie bestimmen wie Ihr Geschlecht und ihr Vorname zukünftig angegeben werden Namensänderung Ein Vor oder Familienname darf nur geändert werden wenn ein wichtiger Grund Namensänderungsgesetz die Änderung rechtfertigt Kirchenaustritt Kirchenaustritt Wer aus der Kirche Religionsgemeinschaft oder weltanschaulichen Gemeinschaft austreten will kann das vor dem Standesamt oder Notar erklären Kirchenaustrittsbescheinigung Der Wohnungsgeber ist verpflichtet bei der Anmeldung einer Wohnung mitzuwirken Das Bundesmeldegesetz sieht in vor dass der Wohnungsgeber oder eine von ihm beauftragte Person dem Meldepflichtigen eine Bestätigung des Einzugs zur Vorlage bei der Meldebehörde ausstellen muss Wohnungsgeber ist wer die Wohnung im Sinne des Bundesmeldegesetzes jeder umschlossene Raum der zum Wohnen oder Schlafen benutzt wird zur Verfügung stellt Wohnungsgeber sind in erster Linie die Vermieter oder deren Beauftragte z B Wohnungsverwaltungen Wohnungsgeber können auch Hauptmieter sein die Wohnraum untervermieten Die Wohnungsgeberbestätigung muss folgende Angaben enthalten Name und Anschrift des Wohnungsgebers und wenn dieser nicht Eigentümer ist auch den Namen des Eigentümers Datum des tatsächlichen Einzugs die Anschrift der Wohnung die Namen aller meldepflichtigen Personen die einziehen Die bloße Vorlage des Mietvertrags erfüllt nicht die gesetzlich bestimmten Voraussetzungen da in ihm in der Regel nicht alle benötigten Angaben enthalten sind Die Bestätigung des Wohnungsgebers kann auch elektronisch gegenüber der Meldebehörde erfolgen In dem Fall erhalten Sie von Ihrem Vermieter ein sogenanntes Zuordnungsmerkmal welches ihm zuvor von der Meldebehörde mitgeteilt wurde Weigert sich der Wohnungsgeber oder eine von ihm beauftragte Person die Bestätigung auszustellen oder ist es Ihnen aus anderen Gründen nicht möglich die Bestätigung rechtzeitig zu erhalten müssen Sie dies der Meldebehörde unverzüglich mitteilen Verfahrensablauf Die Wohnungsgeberbestätigung erhalten Sie von Ihrem Vermieter Es besteht für Wohnungsgeber auch die Möglichkeit die Bestätigung elektronisch gegenüber der Meldebehörde abzugeben wenn die GemeindeStadtverwaltung einen entsprechenden Zugang eröffnet hat In dem Fall erhalten Sie von Ihrem Vermieter ein sogenanntes Zuordnungsmerkmal welches ihm von der Meldebehörde mitgeteilt wird Wenn Sie sich bei der Meldebehörde anmelden legen Sie die Wohnungsgeberbestätigung vor oder geben das Zuordnungsmerkmal an Verfahrensablauf Die Wohnungsgeberbestätigung erhalten Sie von Ihrem Vermieter Es besteht für Wohnungsgeber auch die Möglichkeit die Bestätigung elektronisch gegenüber der Meldebehörde abzugeben wenn die GemeindeStadtverwaltung einen entsprechenden Zugang eröffnet hat In dem Fall erhalten Sie von Ihrem Vermieter ein sogenanntes Zuordnungsmerkmal welches ihm von der Meldebehörde mitgeteilt wird Wenn Sie sich bei der Meldebehörde anmelden legen Sie die Wohnungsgeberbestätigung vor oder geben das Zuordnungsmerkmal an Kosten Für die Ausstellung der Wohnungsgeberbestätigung fallen keine Gebühren an Fristen Der Wohnungsgeber ist verpflichtet die Bestätigung spätestens zwei Wochen nach dem Einzug auszustellen Weigert sich der Wohnungsgeber die Bestätigung auszustellen oder ist es Ihnen aus anderen Gründen nicht möglich die Bestätigung zu erhalten müssen Sie dies der Meldebehörde unverzüglich mitteilen Besondere Hinweise Wenn die Bestätigung vom Wohnungsgeber nicht nicht richtig oder nicht rechtzeitig ausgestellt wird begeht er eine Ordnungswidrigkeit die mit einer Geldbuße bis zu EUR geahndet werden kann Es ist verboten eine Wohnungsanschrift für eine Anmeldung einem Dritten anzubieten oder zur Verfügung zu stellen obwohl ein tatsächlicher Bezug der Wohnung durch einen Dritten weder stattfindet noch beabsichtigt ist Ein Verstoß gegen dieses Verbot stellt eine Ordnungswidrigkeit dar und kann mit einer Geldbuße bis zu Euro geahndet werden Bundesmeldegesetz BMG Mitwirkung des Wohnungsgebers Der Wohnungsgeber ist verpflichtet bei der Anmeldung mitzuwirken Hierzu hat der Wohnungsgeber oder eine von ihm beauftragte Person der meldepflichtigen Person den Einzug schriftlich oder gegenüber der Meldebehörde nach Absatz auch elektronisch innerhalb der in Absatz genannten Frist zu bestätigen Er kann sich durch Rückfrage bei der Meldebehörde davon überzeugen dass sich die meldepflichtige Person angemeldet hat Die meldepflichtige Person hat dem Wohnungsgeber die Auskünfte zu geben die für die Bestätigung des Einzugs erforderlich sind Die Bestätigung nach Satz darf nur vom Wohnungsgeber oder einer von ihm beauftragten Person ausgestellt werden Verweigert der Wohnungsgeber oder eine von ihm beauftragte Person die Bestätigung oder erhält die meldepflichtige Person sie aus anderen Gründen nicht rechtzeitig so hat die meldepflichtige Person dies der Meldebehörde unverzüglich mitzuteilen Die Bestätigung des Wohnungsgebers enthält folgende Daten Name und Anschrift des Wohnungsgebers und wenn dieser nicht Eigentümer ist auch den Namen des Eigentümers Einzugsdatum Anschrift der Wohnung sowie Namen der nach Absatz meldepflichtigen Personen Bei einer elektronischen Bestätigung gegenüber der Meldebehörde erhält der Wohnungsgeber ein Zuordnungsmerkmal welches er der meldepflichtigen Person zur Nutzung bei der Anmeldung mitzuteilen hat Absatz und gilt entsprechend Sofern die Meldebehörde weitere Formen der Authentifizierung des Wohnungsgebers vorsieht ist sicherzustellen dass Maßnahmen nach den Artikeln und der Verordnung EU getroffen werden Die Meldebehörde kann von dem Eigentümer der Wohnung und wenn er nicht selbst Wohnungsgeber ist auch vom Wohnungsgeber Auskunft verlangen über Personen welche bei ihm wohnen oder gewohnt haben Es ist verboten eine Wohnungsanschrift für eine Anmeldung nach Absatz einem Dritten anzubieten oder zur Verfügung zu stellen obwohl ein tatsächlicher Bezug der Wohnung durch einen Dritten weder stattfindet noch beabsichtigt ist Bundesmeldegesetz BMG Bußgeldvorschriften Ordnungswidrig handelt wer entgegen Absatz eine Wohnanschrift anbietet oder zur Verfügung stellt Ordnungswidrig handelt wer vorsätzlich oder fahrlässig entgegen Absatz auch in Verbindung mit Absatz Satz oder Absatz Satz oder Satz entgegen Absatz Satz oder Absatz Satz oder Absatz Satz sich nicht nicht richtig oder nicht rechtzeitig anmeldet entgegen Absatz Satz sich nicht oder nicht rechtzeitig abmeldet entgegen Absatz Satz den Einzug nicht nicht richtig oder nicht rechtzeitig bestätigt entgegen Absatz Satz eine Bestätigung ausstellt einer vollziehbaren Anordnung nach Absatz oder oder Absatz zuwiderhandelt entgegen Absatz Satz eine Mitteilung nicht nicht richtig nicht vollständig oder nicht rechtzeitig macht entgegen Absatz Satz oder Satz den Kapitän oder ein Besatzungsmitglied nicht oder nicht rechtzeitig anmeldet oder nicht oder nicht rechtzeitig abmeldet entgegen Absatz Satz einen besonderen Meldeschein nicht oder nicht rechtzeitig unterschreibt entgegen Absatz Satz einen besonderen Meldeschein nicht bereithält entgegen Absatz Satz auch in Verbindung mit Satz einen Meldeschein nicht oder nicht mindestens ein Jahr aufbewahrt oder Daten nicht oder nicht mindestens ein Jahr speichert entgegen Absatz Satz einen Meldeschein nicht oder nicht rechtzeitig vorlegt oder Daten nicht oder nicht rechtzeitig zur Verfügung stellt Die Ordnungswidrigkeit kann in den Fällen des Absatzes mit einer Geldbuße bis zu fünfzigtausend Euro und in den übrigen Fällen mit einer Geldbuße bis zu tausend Euro geahndet werden'''
    }


def retrieve_relevant_context(query):
    """
    Simulates a search of the knowledge base to find relevant context for the query.
    In a real RAG system, this would use an embedding model and a vector database.
    """
    query_lower = query.lower()
    
    # We'll use a simple keyword search for this example.
    for key, text in KNOWLEDGE_BASE.items():
        if re.search(r'\b' + re.escape(key) + r'\b', query_lower):
            return text
            
    return "No relevant context found."


def generate_content(messages):
    """
    Sends the entire message history to the Llama 3 model via the OpenRouter API
    and returns the generated text. The function now uses RAG to provide additional context.
    
    Args:
        messages (list): A list of message dictionaries representing the conversation history.

    Returns:
        str: The generated text from the model, or an error message.
    """
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    
    # Extract the latest user prompt to search for context
    latest_user_prompt = messages[-1]["content"]
    retrieved_context = retrieve_relevant_context(latest_user_prompt)

    # Combine the system prompt with the retrieved context
    rag_prompt = f"Context: {retrieved_context}\n\n{SYSTEM_PROMPT}"

    # Prepend the RAG-enhanced system message to the conversation history
    full_messages = [
        {"role": "system", "content": rag_prompt}
    ] + messages
    
    # The payload structure for OpenRouter's chat completions API
    payload = {
        # Using a valid model name for the Llama 3 8B Instruct model on OpenRouter.
        "model": "meta-llama/llama-3-8b-instruct",
        "messages": full_messages
    }

    try:
        # Make the POST request to the API
        response = requests.post(API_URL, headers=headers, data=json.dumps(payload))
        response.raise_for_status() # Raise an exception for bad status codes (4xx or 5xx)

        # Parse the JSON response
        result = response.json()
        
        # Extract the generated text from the structured response
        if 'choices' in result and len(result['choices']) > 0:
            return result['choices'][0]['message']['content']
        else:
            return "No content generated from the API."

    except requests.exceptions.HTTPError as e:
        # Handle HTTP errors (e.g., incorrect API key, invalid request)
        print(f"HTTP Error: {e.response.status_code}")
        print(f"Error details: {e.response.text}")
        return "An HTTP error occurred. Please check your API key and request."
    except Exception as e:
        # Handle other potential errors
        print(f"An unexpected error occurred: {e}")
        return "An unexpected error occurred."


if __name__ == "__main__":
    # The list that will store our conversation history.
    # We will pass this to the API on every turn.
    conversation_history = []
    
    print("Welcome to the Llama API CLI client!")
    print("Type your message and press Enter. Type 'exit' to quit.")

    while True:
        user_prompt = input("You: ")
        if user_prompt.lower() == 'exit':
            break
        
        # Add the user's message to the conversation history
        conversation_history.append({"role": "user", "content": user_prompt})

        print("Llama: Generating response...")
        response_text = generate_content(conversation_history)
        
        # Add the model's response to the conversation history
        conversation_history.append({"role": "assistant", "content": response_text})

        print(f"Llama: {response_text}")