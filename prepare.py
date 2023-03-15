import stanza
import dill

# Download the Stanza model
stanza.download('en')

# Load the Stanza model
nlp = stanza.Pipeline('en')

# Serialize the Stanza model using dill
with open('stanza_model.pkl', 'wb') as f:
    dill.dump(nlp, f)

# Load the Stanza model from disk
with open('stanza_model.pkl', 'rb') as f:
    nlp = dill.load(f)

