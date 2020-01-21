from pathlib import Path

incFolders = []

for filename in Path('.').rglob('*.h'):
    incFolders.append((filename.parent))

incFolders = list(dict.fromkeys(incFolders))

for folder in incFolders:
    print(folder)
