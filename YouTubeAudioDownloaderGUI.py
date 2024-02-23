import tkinter as tk
from tkinter import filedialog, messagebox
from pytube import YouTube
import threading
import os

def browse_folder():
    """
    Ouvre un dialogue pour permettre à l'utilisateur de sélectionner un dossier de destination.
    Met à jour le champ du dossier de destination avec le chemin sélectionné.
    """
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        folder_path.set(folder_selected)  # Met à jour la variable liée au champ d'entrée du dossier.

def download_audio():
    """
    Lance le processus de téléchargement dans un thread séparé.
    Ceci évite de bloquer l'interface utilisateur pendant le téléchargement de l'audio.
    """
    threading.Thread(target=download_audio_thread, daemon=True).start()

def download_audio_thread():
    """
    Télécharge l'audio de la vidéo YouTube spécifiée par l'URL.
    Affiche des messages de statut avec des couleurs appropriées selon le résultat du téléchargement.
    """
    video_url = url_entry.get()  # Obtient l'URL de la vidéo depuis le champ d'entrée.
    destination = folder_path.get()  # Obtient le chemin du dossier de destination.
    if not video_url or not destination:
        # Affiche un message si l'URL ou le dossier de destination n'est pas fourni.
        messagebox.showinfo("Information", "Veuillez fournir une URL de vidéo et sélectionner un dossier de destination.")
        return
    try:
        update_status("Téléchargement en cours...", "black")  # Message de statut pour le processus en cours.
        video = YouTube(video_url)  # Crée un objet YouTube.
        audio = video.streams.filter(only_audio=True).first()  # Sélectionne le flux audio.
        out_file = audio.download(output_path=destination)  # Télécharge l'audio dans le dossier spécifié.

        # Renomme le fichier téléchargé en ajoutant l'extension .mp3.
        base, ext = os.path.splitext(out_file)
        new_file = base + '.mp3'
        os.rename(out_file, new_file)

        update_status(f"Téléchargement terminé ! Fichier sauvegardé sous : {new_file}", "green")  # Message de succès.
    except Exception as e:
        # Gère les exceptions et affiche un message d'erreur.
        update_status(f"Erreur : {e}", "red")

def update_status(message, color):
    """
    Met à jour le message de statut dans l'interface utilisateur.
    Utilise la couleur spécifiée pour le texte du message.

    Args:
        message (str): Le message à afficher.
        color (str): La couleur du texte du message (ex. "red", "green", "black").
    """
    status_label.config(text=message, fg=color)  # Configure le label avec le message et la couleur.
    root.update_idletasks()  # Force la mise à jour de l'interface utilisateur.

# Configuration de la fenêtre principale de l'interface utilisateur.
root = tk.Tk()
root.title("Le Convertisseur MP3 de Hans")

# Configuration de la grille pour une expansion automatique des éléments.
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

# Création et configuration du cadre principal pour contenir les widgets.
frame = tk.Frame(root)
frame.grid(padx=10, pady=10, sticky="nsew")
frame.columnconfigure(1, weight=1)
for i in range(5):
    frame.rowconfigure(i, weight=1)

# Widgets pour la saisie de l'URL de la vidéo.
url_label = tk.Label(frame, text="URL de la vidéo YouTube:")
url_label.grid(row=0, column=0, sticky="w")
url_entry = tk.Entry(frame)
url_entry.grid(row=0, column=1, sticky="ew", padx=5)

# Widgets pour la sélection du dossier de destination.
folder_path = tk.StringVar()
folder_label = tk.Label(frame, text="Dossier de destination:")
folder_label.grid(row=1, column=0, sticky="w")
folder_entry = tk.Entry(frame, textvariable=folder_path)
folder_entry.grid(row=1, column=1, sticky="ew", padx=5)
browse_button = tk.Button(frame, text="Parcourir", command=browse_folder)
browse_button.grid(row=1, column=2, sticky="ew")

# Bouton pour initier le téléchargement de l'audio.
download_button = tk.Button(frame, text="Télécharger Audio", command=download_audio)
download_button.grid(row=2, column=0, columnspan=3, pady=10, sticky="ew")

# Label pour afficher les messages de statut du téléchargement.
status_label = tk.Label(root, text="")
status_label.grid(row=3, padx=10, sticky="w")

# Démarre la boucle d'événements de l'interface utilisateur.
root.mainloop()
