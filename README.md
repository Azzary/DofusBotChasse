# DofusBotChasse

You need the autopilot (using a potion or digging into the game files)

IMPORTANT: change 'targets/spell.png' by your spell icon.


Dofus option:
- Limite de passage en mode creature = 0
- Afficher les perssonnages en transparance
- ne pas afficher les coordonnées de la carte
- interface clasique
- havre sac clasique
- si vous avez la motive 7 screens de votre perso en mode creature (a placer dans target/personnageX)
- etre en canal general (etoile blanche, pas de message)
- optionel mode solo

for install all the dependencies
```
pip install -r requirements.txt
```

you need to dl: https://github.com/UB-Mannheim/tesseract/wiki
if you change the path change it in 'ImageManaget.py' to.
pytesseract.pytesseract.tesseract_cmd = r'NEW_PATH' 

You need chrome and chromedriver download to use it with selenium.
Download the file of the same version as your google chrome, and place it in the folder where bot.py is.
https://chromedriver.chromium.org/downloads

Launch dofus on and select a character, then change the name of the game window in config.json to yours 'Name Dofus x.xx.xxx'.

before you start, make sure that your zaap.json file only contains your character's zaaps (zaap_all.json contains all the zaaps if you ever delete any one).
Important you needed the "Champs de Cania" zaap (oui quand meme)

Not having a hunt is easier, because we don't see anything in the console with the selenium logs, otherwise when you could write in console 1 to start at the current position(player), else at the position of the hunt.


# Error
"ModuleNotFoundError: No module named 'win32xxx'"
try to install like that: https://github.com/mhammond/pywin32/releases


"pywintypes.error: (1400, 'GetWindowRect', 'Handle de fenêtre non valide.')"
Name of the Dofus window is not correct.