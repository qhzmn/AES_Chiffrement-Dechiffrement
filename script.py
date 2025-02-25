import os
import getpass
import configparser
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding

# Fonction pour dériver une clé AES à partir d'un mot de passe et d'un sel
def password_to_aes_value(password: str, sel: bytes) -> bytes:
    kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),  # Utilise SHA256 pour le calcul HMAC
    length=32,  # Longueur de la clé dérivée (32 octets pour AES-256)
    salt=sel,  # Sel utilisé pour dériver la clé
    iterations=100000,  # Nombre d'itérations pour augmenter la sécurité
    backend=default_backend()  # Backend cryptographique par défaut
    )
    return kdf.derive(password.encode())  # Convertit le mot de passe en une clé


# Déchiffrement d'un fichier
def dechiffre_fichier(input_filename, output_filename, password):
    try:
        with open(input_filename, 'rb') as file:
            sel = file.read(32)  # Lire le sel
            iv = file.read(16)    # Lire l'IV
            chiffre_data = file.read()  # Lire les données chiffrées

        value = password_to_aes_value(password, sel)

        # Créer un objet Cipher avec la clé et l'IV dans le mode CBC
        cipher = Cipher(algorithms.AES(value), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()

        padded_data = decryptor.update(chiffre_data) + decryptor.finalize() #déchiffre les données

        # Supprimer le padding
        unpadder = padding.PKCS7(128).unpadder()
        dechiffre_data = unpadder.update(padded_data) + unpadder.finalize()

        # Sauvegarder les données déchiffrées dans le fichier
        with open(output_filename, 'wb') as file:
            file.write(dechiffre_data)
        print("Contenu déchiffré avec succès.")
        return dechiffre_data
    
    except Exception as e:
        print(f"Erreur lors du déchiffrage : {e}")
        return None
    

# Chiffrement d'un fichier
def chiffre_fichier(input_filename, output_filename, password):
    try:
        if not os.path.exists(input_filename):
            print("Fichier introuvable!")
            return

        sel = os.urandom(32)  # Sel aléatoire de 32 octets
        value = password_to_aes_value(password, sel) # Dériver la clé avec le mot de passe et le sel

        iv = os.urandom(16)  # Générer un IV aléatoire de 16 octets
        cipher = Cipher(algorithms.AES(value), modes.CBC(iv), backend=default_backend())
        encryptor = cipher.encryptor()

        with open(input_filename, 'rb') as file:
            file_data = file.read()

        # Appliquer le padding pour que la length des données soit un multiple de 16
        padder = padding.PKCS7(128).padder()
        padded_data = padder.update(file_data) + padder.finalize()

        chiffre_data = encryptor.update(padded_data) + encryptor.finalize()

        with open(output_filename, 'wb') as file:
            file.write(sel)  # Sauvegarder le sel
            file.write(iv)    # Sauvegarder l'IV
            file.write(chiffre_data)  # Sauvegarder les données chiffrées
        print("Contenu chiffré avec succès.")
        
    except Exception as e:
        print(f"Erreur lors du chiffrement : {e}")


# Fonction pour lire une configuration depuis un fichier
def read_config(value, file_name="C:/Users/quent/OneDrive/Documents/perso/program_code/Python/password/config.ini"):
    config = configparser.ConfigParser() # Créer un objet pour lire les fichiers INI
    try:
        if os.path.exists(file_name):
            config.read(file_name)
            return config.get('settings', value, fallback=None) # Retourne la valeur associée à la clé demandée
        else:
            print(f"Le fichier de configuration {file_name} est introuvable.")
            return None
    except Exception as e:
        print(f"Erreur lors de la lecture de la configuration : {e}")
        return None


# Fonction pour mettre à jour la configuration# Créer une nouvelle section si nécessaire
def edit_config(value, valeur, file_name="C:/Users/quent/OneDrive/Documents/perso/program_code/Python/password/config.ini"):
    config = configparser.ConfigParser()
    try:
        if os.path.exists(file_name):
            config.read(file_name)
        else:
            config.add_section('settings') # Créer une nouvelle section si nécessaire
        config['settings'][value] = valeur # Mettre à jour la valeur pour la clé spécifiée
        with open(file_name, 'w') as f:
            config.write(f) # Sauvegarder les modifications dans le fichier
        print("-----Configuration MàJ : succès_!-----")
    except Exception as e:
        print(f"---Erreur lors de la mise à jour de la configuration--- : {e}")


# Fonction pour gérer les entrées utilisateur dans le menu de configuration
def config():
    print("\n1. Nom de fichier")
    print("2. Chemin")
    print("3. Mot de passe (modification)")
    value = input("Choisissez une option : ").strip()
    if value not in ['1', '2', '3']:
        print("Option invalide!")
        return
    
    if value == '1':
        valeur = input("Entrez la valeur : ").strip()
        edit_config('nom_fichier', valeur)
        return valeur
    elif value == '2':
        valeur = input("Entrez la valeur : ").strip()
        edit_config('chemin', valeur)
    elif value == '3':
        return getpass.getpass("Entrez le mot de passe : ")

def fichier_existe(nom_fichier, chemin):
    chemin_complet = os.path.join(chemin, nom_fichier)
    if os.path.isfile(chemin_complet):
        return True
    print("-----Fichier non trouvé_!-----")
    return False
# Fonction principale
def main():
    password = None
    while True:
        try:
            chemin = read_config('chemin') or os.getcwd()
            while not read_config('nom_fichier'):
                print("---Erreur nom fichier---")
                config()
            nom_fichier = read_config('nom_fichier')
            print("\n1. Chiffrer un fichier")
            print("2. Déchiffrer un fichier")
            print("3. Modifier la configuration")
            print("4. Quitter")
            choice = input("Choisissez une option : ").strip()
            
            if choice == '1' and fichier_existe(nom_fichier, chemin):
                if password is None:
                    password = getpass.getpass("Entrez le mot de passe : ")
                chiffre_fichier(os.path.join(chemin, nom_fichier), os.path.join(chemin, nom_fichier), password)
            elif choice == '2' and fichier_existe(nom_fichier, chemin):
                password = getpass.getpass("Entrez le mot de passe : ")
                decrypted_content = dechiffre_fichier(os.path.join(chemin, nom_fichier), os.path.join(chemin, nom_fichier), password)
            elif choice == '3':
                password=config()
            elif choice == '4':
                break
            
        except Exception as e:
            print(f"---Erreur dans le processus principal--- : {e}")


# Lancement du programme
if __name__ == "__main__":
    main()