import pickle

def save_object(obj, filename: str):
    """permet de sauvegarder un objet dans un chemin d'accès en .pickle"""
    try:
        with open(filename, "wb") as f:
            pickle.dump(obj, f, protocol=pickle.HIGHEST_PROTOCOL)
    except Exception as ex:
        print("Error during pickling object (Possibly unsupported):", ex)

def load_object(filename):
    """permet de recuperer un objet depuis un chemin d'accès en .pickle"""
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except Exception as ex:
        print("Error during unpickling object (Possibly unsupported):", ex)

