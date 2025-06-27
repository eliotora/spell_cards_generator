[Setup]
AppName=DnD Spell Viewer
AppVersion=1.1
DefaultDirName={pf}\SpellViewer
DefaultGroupName=DnD Spell Viewer
OutputDir=.
OutputBaseFilename=SpellViewerInstaller
SetupIconFile=dist\app.ico
Compression=lzma
SolidCompression=yes

[Dirs]
Name: "{app}\data"
Name: "{userdocs}\DnD Spell Viewer Exports"

[Files]
Source: "dist\dnd_spell_viewer.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "dist\app.ico"; DestDir: "{app}"; Flags: ignoreversion
Source: "dist\styles\*"; DestDir: "{app}\styles"; Flags: ignoreversion recursesubdirs
Source: "dist\images\*"; DestDir: "{app}\images"; Flags: ignoreversion recursesubdirs
; Source: "dist\ms-playwright\*"; DestDir: "{app}\ms-playwright"; Flags: recursesubdirs
Source: "dist\_internal\*"; DestDir: "{app}\_internal"; Flags: recursesubdirs
; Source: "dist\output\*"; DestDir: "{app}\output"; Flags: recursesubdirs

[Icons]
Name: "{group}\DnD Spell Viewer"; Filename: "{app}\dnd_spell_viewer.exe"; IconFilename: "{app}\app.ico"
Name: "{userdesktop}\DnD Spell Viewer"; Filename: "{app}\dnd_spell_viewer.exe"; IconFilename: "{app}\app.ico"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Créer une icône sur le Bureau"; GroupDescription: "Icônes supplémentaires :"

[Run]
Filename: "{app}\dnd_spell_viewer.exe"; Description: "Lancer l'application"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
Type: filesandordirs; Name: "{app}\data"
; Type: filesandordirs; Name: "{app}\output"
