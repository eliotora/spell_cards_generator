#ifndef MyAppVersion
  #define MyAppVersion "0.0.0"
#endif

[Setup]
AppName=DnD Spell Viewer
AppVersion={#AppVersion}
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
Source: "dist\assets\*"; DestDir: "{app}\assets"; Flags: ignoreversion recursesubdirs
Source: "dist\_internal\*"; DestDir: "{app}\_internal"; Flags: recursesubdirs
Source: "dist\version.json"; DestDir: "{app}";

[Icons]
Name: "{group}\DnD Spell Viewer"; Filename: "{app}\dnd_spell_viewer.exe"; IconFilename: "{app}\app.ico"
Name: "{userdesktop}\DnD Spell Viewer"; Filename: "{app}\dnd_spell_viewer.exe"; IconFilename: "{app}\app.ico"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Créer une icône sur le Bureau"; GroupDescription: "Icônes supplémentaires :"

[Run]
Filename: "{app}\dnd_spell_viewer.exe"; Description: "Lancer l'application"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
Type: filesandordirs; Name: "{app}\data"
