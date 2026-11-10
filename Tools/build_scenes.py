"""Offline authoring tool. Generated Unity scenes are already included; do not run to play.
Requires Python 3 and Pillow. Re-running replaces scene layout customizations.
"""
from pathlib import Path
import re, json, hashlib, math
from PIL import Image, ImageDraw, ImageFont
ROOT=Path(__file__).resolve().parents[1]
A=ROOT/'Assets'
GAME=A/'Scenes/Gameplay'
def guid(path):
    m=Path(str(path)+'.meta')
    if m.exists():return re.search(r'guid: (\w+)',m.read_text()).group(1)
    return hashlib.md5(str(path.relative_to(ROOT)).encode()).hexdigest()
def meta(path,kind='DefaultImporter'):
    p=Path(str(path)+'.meta')
    if not p.exists():p.write_text(f'fileFormatVersion: 2\nguid: {guid(path)}\n{kind}:\n  externalObjects: {{}}\n  userData: \n  assetBundleName: \n  assetBundleVariant: \n')
for p in A.rglob('*.cs'):meta(p,'MonoImporter')
G={p.stem:guid(p) for p in A.rglob('*.cs')}
G.update(Image='fe87c0e1cc204ed48ad3b37840f39efc',Text='5f7201a12d95ffc409449d95f23cf332',Button='4e29b1a8efbd4b44bb3f3716e73f07ff',Scaler='0cd44c1031e13a943bb63640046fad76',Raycaster='dc42784cf147c0c48a680349fa168899',Events='76c392e42b5098c458856cdf6ecaaaa1',Input='4f231c4fb786f3946a6b90b886c48677')
FONT=guid(A/'TextMesh Pro/Fonts/LiberationSans.ttf')
SETTINGS=A/'Settings/CompetitionScoring.asset';SETTINGS.parent.mkdir(parents=True,exist_ok=True)
# One shared editable asset; preserve values when re-authoring existing scenes.
if not SETTINGS.exists():
    SETTINGS.write_text('%YAML 1.1\n%TAG !u! tag:unity3d.com,2011:\n--- !u!114 &11400000\nMonoBehaviour:\n  m_ObjectHideFlags: 0\n  m_CorrespondingSourceObject: {fileID: 0}\n  m_PrefabInstance: {fileID: 0}\n  m_PrefabAsset: {fileID: 0}\n  m_GameObject: {fileID: 0}\n  m_Enabled: 1\n  m_EditorHideFlags: 0\n  m_Script: {fileID: 11500000, guid: '+G['ScoreSettings']+', type: 3}\n  m_Name: CompetitionScoring\n  m_EditorClassIdentifier: \n  level1Points: 200\n  level2Points: 300\n  level3Points: 500\n')
meta(SETTINGS,'NativeFormatImporter')
PAPER=(.98,.95,.87,1); INK=(.13,.19,.20,1); BG=(.08,.14,.15,1); GOLD=(.75,.52,.22,1); MUTED=(.42,.46,.43,1); PARCH=(.92,.87,.75,1)
PALETTE=[(.90,.42,.34,1),(.24,.59,.72,1),(.91,.69,.28,1),(.43,.69,.48,1),(.67,.49,.76,1),(.90,.56,.35,1),(.38,.50,.76,1),(.74,.42,.55,1)]
ART=A/'Art/Puzzle';ART.mkdir(parents=True,exist_ok=True)
for name in ['CellTile','Rose','Window','Gemini','Delta']:
    im=Image.new('RGBA',(128,128));d=ImageDraw.Draw(im)
    if name=='CellTile':
        d.rounded_rectangle((1,1,126,126),radius=8,fill='white',outline=(185,190,180,255),width=3)
        d.line((12,8,116,8), fill=(255,255,255,255),width=3)
    elif name=='Rose':
        d.ellipse((3,3,125,125),fill=(250,242,222),outline=(37,51,52),width=5)
        for k in range(8):
            a=k*math.pi/4;x=64+25*math.cos(a);y=64+25*math.sin(a)
            d.ellipse((x-16,y-16,x+16,y+16),fill=(197,63,59),outline=(90,32,32),width=2)
        d.ellipse((49,49,79,79),fill=(244,185,69),outline=(90,32,32),width=3)
    elif name=='Window':
        d.ellipse((3,3,125,125),fill=(250,242,222),outline=(37,51,52),width=5)
        d.polygon([(64,16),(107,64),(64,112),(21,64)],fill=(64,145,173),outline=(27,57,68),width=5)
        d.line((64,20,64,108),fill=(250,242,222),width=7);d.line((25,64,103,64),fill=(250,242,222),width=7)
    else:
        d.rounded_rectangle((3,3,125,125),radius=18,fill=(250,242,222) if name=='Gemini' else (33,48,51),outline=(188,140,72),width=5)
        c=(33,48,51) if name=='Gemini' else (250,242,222)
        d.line((33,46,95,46),fill=c,width=10);d.line((33,81,95,81),fill=c,width=10)
        if name=='Delta':d.line((87,24,41,104),fill=c,width=10)
    p=ART/(name+'.png');im.save(p)
    Path(str(p)+'.meta').write_text(f'''fileFormatVersion: 2
guid: {guid(p)}
TextureImporter:
  internalIDToNameTable: []
  externalObjects: {{}}
  serializedVersion: 13
  mipmaps:
    enableMipMap: 0
    sRGBTexture: 1
  isReadable: 0
  textureSettings:
    serializedVersion: 2
    filterMode: 1
    aniso: 1
    mipBias: 0
    wrapU: 1
    wrapV: 1
    wrapW: 1
  nPOTScale: 0
  maxTextureSize: 2048
  spriteMode: 1
  spriteExtrude: 1
  spriteMeshType: 1
  alignment: 0
  spritePivot: {{x: 0.5, y: 0.5}}
  spritePixelsToUnits: 100
  spriteBorder: {{x: 0, y: 0, z: 0, w: 0}}
  alphaUsage: 1
  alphaIsTransparency: 1
  textureType: 8
  textureShape: 1
  platformSettings: []
  spriteSheet:
    serializedVersion: 2
    sprites: []
    outline: []
    physicsShape: []
    bones: []
    spriteID: {hashlib.md5(name.encode()).hexdigest()}
    internalID: 0
    vertices: []
    indices: 
    edges: []
    weights: []
    secondaryTextures: []
    nameFileIdTable: {{}}
  userData: 
  assetBundleName: 
  assetBundleVariant: 
''')
# Generated screen artwork is included in the project; no generation at runtime.
BACKGROUNDS=['MenuBackground', 'Level01Background', 'Level02Background', 'Level03Background', 'GameOverBackground']
UI_SPRITES=['StartButtonPlaque']
for name in BACKGROUNDS+UI_SPRITES:
    p=(A/'Art/Backgrounds' if name in BACKGROUNDS else A/'Art/UI')/(name+'.png')
    template=Path(str(ART/'Rose.png')+'.meta').read_text()
    template=template.replace(guid(ART/'Rose.png'),guid(p)).replace(hashlib.md5('Rose'.encode()).hexdigest(),hashlib.md5(name.encode()).hexdigest())
    Path(str(p)+'.meta').write_text(template)
# Read the source of truth without changing the existing puzzle layouts.
source=(GAME/'PuzzleLevels.cs').read_text()
levels=[]
for block in source.split('new LevelData {')[1:]:
    layout=re.search(r'layout = new \[\] \{(.*?)\}',block,re.S).group(1)
    shapes=[{'name':n,'rows':re.findall(r'"([01]+)"',r)} for n,r in re.findall(r'new ShapeData\("([^"]+)",(.*?)\)',block)]
    symbols=[list(map(int,p)) for p in re.findall(r'new SymbolData\((\d+),(\d+),(\d+)\)',block)]
    walls=[list(map(int,p)) for p in re.findall(r'new WallData\((\d+),(\d+),(\d+),(\d+)\)',block)]
    rules=[[*map(int,p[:4]),p[4]=='true'] for p in re.findall(r'new EdgeRule\((\d+),(\d+),(\d+),(\d+),(true|false)\)',block)]
    levels.append(dict(layout=re.findall(r'"([01]+)"',layout),shapes=shapes,symbols=symbols,walls=walls,rules=rules))
(ROOT/'Tools/levels.json').write_text(json.dumps(levels,indent=2))
# Preserve the original camera and scene rendering settings as a reusable template.
template=ROOT/'Tools/scene_header.txt'
if not template.exists():
    old=(GAME/'Gameplay_Scene.unity').read_text();template.write_text(old[:old.index('--- !u!1 &1173197322')])
BASE=template.read_text()
def ref(i):return '{fileID: '+str(i)+'}'
def color(c):return '{'+', '.join(f'{k}: {v:g}' for k,v in zip('rgba',c))+'}'
def vec(x,y):return f'{{x: {x:g}, y: {y:g}}}'
def quote(s):return json.dumps(s,ensure_ascii=False)
COMMON='  m_ObjectHideFlags: 0\n  m_CorrespondingSourceObject: {fileID: 0}\n  m_PrefabInstance: {fileID: 0}\n  m_PrefabAsset: {fileID: 0}\n'
class Node:
    def __init__(self,s,name,parent=None,pos=(0,0),size=(100,100),active=True):
        self.s=s;self.name=name;self.parent=parent;self.pos=pos;self.size=size;self.active=active;self.children=[];self.comp=[];self.go=s.id();self.tr=s.id();self.preview={}
        s.nodes.append(self)
        if parent:parent.children.append(self)
    def component(self,kind,data='',unitytype=None):
        i=self.s.id();self.comp.append(i)
        if unitytype:
            body=COMMON+f'  m_GameObject: {ref(self.go)}\n'+data
            self.s.docs.append((unitytype,i,kind,body))
        else:
            body=COMMON+f'  m_GameObject: {ref(self.go)}\n  m_Enabled: 1\n  m_EditorHideFlags: 0\n  m_Script: {{fileID: 11500000, guid: {G[kind]}, type: 3}}\n  m_Name: \n  m_EditorClassIdentifier: \n'+data
            self.s.docs.append((114,i,'MonoBehaviour',body))
        return i
    def image(self,c=PAPER,ray=False,sprite=None):
        self.component('CanvasRenderer','  m_CullTransparentMesh: 1\n',222)
        asset_path=(A/'Art/Backgrounds'/(sprite+'.png')) if sprite in BACKGROUNDS else (A/'Art/UI'/(sprite+'.png')) if sprite in UI_SPRITES else (ART/(sprite+'.png')) if sprite else None
        sp=f'{{fileID: 21300000, guid: {guid(asset_path)}, type: 3}}' if sprite else ref(0)
        i=self.component('Image',f'''  m_Material: {{fileID: 0}}
  m_Color: {color(c)}
  m_RaycastTarget: {int(ray)}
  m_RaycastPadding: {{x: 0, y: 0, z: 0, w: 0}}
  m_Maskable: 1
  m_OnCullStateChanged:
    m_PersistentCalls:
      m_Calls: []
  m_Sprite: {sp}
  m_Type: 0
  m_PreserveAspect: {int(bool(sprite))}
  m_FillCenter: 1
  m_FillMethod: 4
  m_FillAmount: 1
  m_FillClockwise: 1
  m_FillOrigin: 0
  m_UseSpriteMesh: 0
  m_PixelsPerUnitMultiplier: 1
''');self.preview.update(c=c,sprite=sprite);return i
    def text(self,id,en=None,font=20,c=INK,align=4,bold=False,overflow=False):
        self.component('CanvasRenderer','  m_CullTransparentMesh: 1\n',222)
        i=self.component('Text',f'''  m_Material: {{fileID: 0}}
  m_Color: {color(c)}
  m_RaycastTarget: 0
  m_RaycastPadding: {{x: 0, y: 0, z: 0, w: 0}}
  m_Maskable: 1
  m_OnCullStateChanged:
    m_PersistentCalls:
      m_Calls: []
  m_FontData:
    m_Font: {{fileID: 12800000, guid: {FONT}, type: 3}}
    m_FontSize: {font}
    m_FontStyle: {int(bold)}
    m_BestFit: 0
    m_MinSize: 10
    m_MaxSize: {font}
    m_Alignment: {align}
    m_AlignByGeometry: 0
    m_RichText: 1
    m_HorizontalOverflow: {int(overflow)}
    m_VerticalOverflow: {int(overflow)}
    m_LineSpacing: 1
  m_Text: {quote(id)}
''')
        if en is not None:self.component('LocalizedText',f'  Indonesian: {quote(id)}\n  English: {quote(en)}\n')
        self.preview.update(text=id,en=en,font=font,c=c,bold=bold,align=align);return i
    def button(self,target,typename,method,id,en=None,c=GOLD,arg=None,font=22,sprite=None):
        img=self.image(c,True,sprite)
        i=self.component('Button',f'''  m_Navigation:
    m_Mode: 0
    m_WrapAround: 0
    m_SelectOnUp: {{fileID: 0}}
    m_SelectOnDown: {{fileID: 0}}
    m_SelectOnLeft: {{fileID: 0}}
    m_SelectOnRight: {{fileID: 0}}
  m_Transition: 1
  m_Colors:
    m_NormalColor: {{r: 1, g: 1, b: 1, a: 1}}
    m_HighlightedColor: {{r: 0.9, g: 0.9, b: 0.9, a: 1}}
    m_PressedColor: {{r: 0.75, g: 0.75, b: 0.75, a: 1}}
    m_SelectedColor: {{r: 1, g: 1, b: 1, a: 1}}
    m_DisabledColor: {{r: 0.6, g: 0.6, b: 0.6, a: 0.5}}
    m_ColorMultiplier: 1
    m_FadeDuration: 0.1
  m_Interactable: 1
  m_TargetGraphic: {ref(img)}
  m_OnClick:
    m_PersistentCalls:
      m_Calls:
      - m_Target: {ref(target)}
        m_TargetAssemblyTypeName: {typename}, Assembly-CSharp
        m_MethodName: {method}
        m_Mode: {3 if arg is not None else 1}
        m_Arguments:
          m_ObjectArgument: {{fileID: 0}}
          m_ObjectArgumentAssemblyTypeName: UnityEngine.Object, UnityEngine
          m_IntArgument: {arg if arg is not None else 0}
          m_FloatArgument: 0
          m_StringArgument: 
          m_BoolArgument: 0
        m_CallState: 2
''')
        Node(self.s,'Label',self,size=(self.size[0]-12,self.size[1]-4)).text(id,en,font,PAPER,bold=True)
        return i,img
class Scene:
    def __init__(self):self.nodes=[];self.docs=[];self.next=10000
    def id(self):self.next+=1;return self.next
    def patch(self,i,data):
        for j,(t,k,n,b) in enumerate(self.docs):
            if k==i:self.docs[j]=(t,k,n,b+data);return
    def write(self,path,prefab=False):
        out=['%YAML 1.1\n%TAG !u! tag:unity3d.com,2011:\n' if prefab else BASE]
        def doc(t,i,name,b):out.append(f'--- !u!{t} &{i}\n{name}:\n{b}')
        for n in self.nodes:
            doc(1,n.go,'GameObject',COMMON+'  serializedVersion: 6\n  m_Component:\n'+''.join('  - component: '+ref(i)+'\n' for i in [n.tr]+n.comp)+f'  m_Layer: 5\n  m_Name: {quote(n.name)}\n  m_TagString: Untagged\n  m_Icon: {{fileID: 0}}\n  m_NavMeshLayer: 0\n  m_StaticEditorFlags: 0\n  m_IsActive: {int(n.active)}\n')
            children='  m_Children:\n'+''.join('  - '+ref(c.tr)+'\n' for c in n.children) if n.children else '  m_Children: []\n'
            doc(224,n.tr,'RectTransform',COMMON+f'''  m_GameObject: {ref(n.go)}
  m_LocalRotation: {{x: 0, y: 0, z: 0, w: 1}}
  m_LocalPosition: {{x: 0, y: 0, z: 0}}
  m_LocalScale: {{x: 1, y: 1, z: 1}}
  m_ConstrainProportionsScale: 0
'''+children+f'''  m_Father: {ref(n.parent.tr if n.parent else 0)}
  m_LocalEulerAnglesHint: {{x: 0, y: 0, z: 0}}
  m_AnchorMin: {{x: 0.5, y: 0.5}}
  m_AnchorMax: {{x: 0.5, y: 0.5}}
  m_AnchoredPosition: {vec(*n.pos)}
  m_SizeDelta: {vec(*n.size)}
  m_Pivot: {{x: 0.5, y: 0.5}}
''')
        for args in self.docs:doc(*args)
        if not prefab:doc(1660057539,9223372036854775807,'SceneRoots','  m_ObjectHideFlags: 0\n  m_Roots:\n  - {fileID: 519420032}\n'+''.join('  - '+ref(n.tr)+'\n' for n in self.nodes if not n.parent))
        path.parent.mkdir(parents=True,exist_ok=True);path.write_text(''.join(out));meta(path)
    def base(self,background):
        service=Node(self,'Competition Session');service.component('GameSession',f'  scoring: {{fileID: 11400000, guid: {guid(SETTINGS)}, type: 2}}\n')
        canvas=Node(self,'Canvas',size=(1600,900))
        canvas.component('Canvas','''  m_Enabled: 1
  serializedVersion: 3
  m_RenderMode: 0
  m_Camera: {fileID: 0}
  m_PlaneDistance: 100
  m_PixelPerfect: 0
  m_ReceivesEvents: 1
  m_OverrideSorting: 0
  m_OverridePixelPerfect: 0
  m_SortingBucketNormalizedSize: 0
  m_VertexColorAlwaysGammaSpace: 0
  m_AdditionalShaderChannelsFlag: 25
  m_UpdateRectTransformForStandalone: 0
  m_SortingLayerID: 0
  m_SortingOrder: 0
  m_TargetDisplay: 0
''',223)
        canvas.component('Scaler','''  m_UiScaleMode: 1
  m_ReferencePixelsPerUnit: 100
  m_ScaleFactor: 1
  m_ReferenceResolution: {x: 1600, y: 900}
  m_ScreenMatchMode: 1
  m_MatchWidthOrHeight: 0.5
  m_PhysicalUnit: 3
  m_FallbackScreenDPI: 96
  m_DefaultSpriteDPI: 96
  m_DynamicPixelsPerUnit: 1
  m_PresetInfoIsWorld: 0
''')
        canvas.component('Raycaster','''  m_IgnoreReversedGraphics: 1
  m_BlockingObjects: 0
  m_BlockingMask:
    serializedVersion: 2
    m_Bits: 4294967295
''')
        events=Node(self,'EventSystem');events.component('Events','  m_FirstSelected: {fileID: 0}\n  m_sendNavigationEvents: 1\n  m_DragThreshold: 10\n')
        events.component('Input','  m_HorizontalAxis: Horizontal\n  m_VerticalAxis: Vertical\n  m_SubmitButton: Submit\n  m_CancelButton: Cancel\n  m_InputActionsPerSecond: 10\n  m_RepeatDelay: 0.5\n  m_ForceModuleActive: 0\n')
        lang=Node(self,'Language Controller');self.lang=lang.component('LanguageButton')
        bg=Node(self,'Full Screen Background - '+background,canvas,size=(1600,900))
        bg.image((1,1,1,1),False,background)
        bg.component('FullScreenBackground')
        return canvas
    def language(self,canvas):Node(self,'Language ID EN',canvas,(657,397),(166,44)).button(self.lang,'LanguageButton','ToggleLanguage','ID  /  EN',c=INK)
    def preview(self,path,en=False):
        im=Image.new('RGBA',(1600,900),(20,35,38));d=ImageDraw.Draw(im)
        fontpath=str(A/'TextMesh Pro/Fonts/LiberationSans.ttf')
        for n in self.nodes:
            active=n.active;p=n.parent;x,y=n.pos
            while p:active=active and p.active;x+=p.pos[0];y+=p.pos[1];p=p.parent
            if not active or not n.preview:continue
            v=n.preview;w,h=n.size;l,t=800+x-w/2,450-y-h/2
            c=tuple(round(k*255) for k in v.get('c',PAPER))
            if 'text' in v:
                value=v.get('en') if en and v.get('en') is not None else v['text'];font=ImageFont.truetype(fontpath,v['font']);lines=[]
                for raw in value.split('\n'):
                    cur=''
                    for word in raw.split(' '):
                        test=(cur+' '+word).strip()
                        if d.textlength(test,font=font)>w and cur:lines.append(cur);cur=word
                        else:cur=test
                    lines.append(cur)
                lineheight=v['font']*1.16;top=t+(h-lineheight*len(lines))/2
                for line in lines:
                    xx=l+(w-d.textlength(line,font=font))/2 if v['align']%3==1 else l
                    d.text((xx,top),line,font=font,fill=c,stroke_width=1 if v['bold'] else 0);top+=lineheight
            elif v.get('sprite'):
                asset_path=A/'Art/Backgrounds'/(v['sprite']+'.png') if v['sprite'] in BACKGROUNDS else A/'Art/UI'/(v['sprite']+'.png') if v['sprite'] in UI_SPRITES else ART/(v['sprite']+'.png')
                asset=Image.open(asset_path).convert("RGBA").resize((int(w),int(h)),Image.Resampling.LANCZOS)
                if c!=(255,255,255,255):
                    from PIL import ImageChops
                    asset=ImageChops.multiply(asset,Image.new('RGBA',asset.size,c))
                im.alpha_composite(asset,(round(l),round(t)))
            else:
                if c[3]<255:
                    layer=Image.new('RGBA',(max(1,round(w)),max(1,round(h))),c)
                    im.alpha_composite(layer,(round(l),round(t)))
                else:d.rectangle((l,t,l+w,t+h),fill=c)
        path.parent.mkdir(parents=True,exist_ok=True);im.convert('RGB').save(path.with_suffix('.jpg'),quality=93)
TITLES=['THE FIRST DRAFT','ROSE & GLASS','TWIN PARADOX']
TITLES_ID=['SKETSA PERTAMA','MAWAR & KACA','PARADOKS KEMBAR']
DESC_ID=[
'Bentuk setiap region sesuai shape bank. Rotasi 90 derajat boleh; pencerminan tidak. Bentuk boleh dipakai berulang.',
'Setiap region harus mengandung tepat 1 Rose dan 1 Window. Bentuk dan ukuran region bebas.',
'Pakai bentuk bank. Bandingkan bentuk dua region di sisi simbol Gemini atau Delta.']
DESC_EN=[
'Match every region to the shape bank. 90-degree rotations are allowed; reflections are not. Shapes can be reused.',
'Each region must contain exactly 1 Rose and 1 Window. Regions can have any shape or size.',
'Use the shape bank. Compare the shapes of the two regions beside each Gemini or Delta symbol.']
scene_paths=[]
for idx,lev in enumerate(levels):
    s=Scene();c=s.base(BACKGROUNDS[idx+1]);
    Node(s,'Header Contrast',c,(0,396),(1600,108)).image((.04,.08,.11,.88))
    Node(s,'Footer Contrast',c,(-285,-400),(890,100)).image((.04,.08,.11,.92))
    manager=Node(s,'GameManager');gm=manager.component('GridManager');validator=manager.component('GridValidator');hud=manager.component('PuzzleHUD')
    Node(s,'Game Title',c,(-433,404),(630,42)).text("Proffesor's Blueprint",font=31,c=PAPER,bold=True,align=3)
    score=Node(s,'Current Score',c,(-433,366),(630,28));score.text('POIN: 0 / 1000    |    LEVEL INI: +'+str([200,300,500][idx]),font=21,c=PAPER,align=3,bold=True);score.component('ScoreDisplay')
    Node(s,'Timer Label',c,(76,425),(330,28)).text('SISA WAKTU TOTAL','TOTAL TIME REMAINING',19,PAPER,bold=True)
    timer=Node(s,'Timer 10 Minutes',c,(76,378),(250,64));timer.text('10:00',font=42,c=PAPER,bold=True,overflow=True);timer.component('CompetitionTimer')
    Node(s,'Stage',c,(385,398),(244,40)).text(f'LEVEL 0{idx+1} / 03',font=24,c=PAPER,bold=True)
    frame=Node(s,'Board Frame',c,(-285,-4),(880,696));frame.image(GOLD)
    mat=Node(s,'Board Mat',frame,size=(866,682));mat.image((.82,.75,.60,1))
    Node(s,'Board Interior',mat,size=(844,660)).image(INK)
    board=Node(s,f'Level 0{idx+1} - Board',mat,pos=(0,24),size=(820,554))
    w=len(lev['layout'][0]);h=len(lev['layout']);step=int(min(790/w,534/h));cellsize=step-3
    cellsroot=Node(s,'Cells - Editable',board,size=(w*step,h*step))
    def center(x,y):return ((x-(w-1)/2)*step,((h-1)/2-y)*step)
    for y,row in enumerate(lev['layout']):
        for x,v in enumerate(row):
            if v!='1':continue
            cell=Node(s,f'Cell_{x:02}_{y:02}',cellsroot,center(x,y),(cellsize,cellsize));cell.image(PAPER,True,'CellTile');cell.component('CellBehavior',f'  gridX: {x}\n  gridY: {y}\n')
    lines=Node(s,'Fixed Walls',board)
    for x,y,nx,ny in lev['walls']:
        a=center(x,y);b=center(nx,ny);pos=((a[0]+b[0])/2,(a[1]+b[1])/2)
        vertical=x!=nx
        wall=Node(s,f'Wall_{x}_{y}_{nx}_{ny}',lines,pos,(20,step+9) if vertical else (step+9,20));wall.image((.035,.08,.11,1))
        Node(s,'Cyan Wall Core',wall,size=(14,step+5) if vertical else (step+5,14)).image((.05,.79,.93,1))
        Node(s,'Light Center Stripe',wall,size=(4,step+1) if vertical else (step+1,4)).image((.77,.98,1,1))
    symbols=Node(s,'Symbols',board)
    for x,y,kind in lev['symbols']:
        name='Rose' if kind==0 else 'Window';Node(s,f'{name}_{x}_{y}',symbols,center(x,y),(40,40)).image((1,1,1,1),False,name)
    for x,y,nx,ny,same in lev['rules']:
        a=center(x,y);b=center(nx,ny);name='Gemini' if same else 'Delta'
        Node(s,f'{name}_{x}_{y}',symbols,((a[0]+b[0])/2,(a[1]+b[1])/2),(34,34)).image((1,1,1,1),False,name)
    side=Node(s,'Rules and Tools - Edit This Canvas',c,(480,-4),(520,724));side.image(PAPER)
    Node(s,'Heading Backing',side,(0,304),(496,90)).image(INK)
    Node(s,'Level Title',side,(0,304),(470,75)).text(TITLES_ID[idx],TITLES[idx],30,PAPER,bold=True)
    Node(s,'Rule Description ID EN',side,(0,207),(470,100)).text(DESC_ID[idx],DESC_EN[idx],24,INK,3,True)
    Node(s,'Bank Title',side,(0,137),(470,32)).text('Shape Bank','Shape Bank',24,INK,3,True)
    bank=Node(s,f'Shape Bank Level {idx+1}',side,(0,74 if idx==2 else 25),(470,100 if idx==2 else 194));bank.image(PARCH)
    if lev['shapes']:
        width=448/len(lev['shapes'])
        for k,shape in enumerate(lev['shapes']):
            root=Node(s,'Shape '+shape['name'],bank,(-224+width*(k+.5),0),(width,114))
            rows=shape['rows'];block=min(18,64/len(rows));ox=-(len(rows[0])-1)*block/2;oy=(13 if idx==2 else 20)+(len(rows)-1)*block/2
            for y,row in enumerate(rows):
                for x,v in enumerate(row):
                    if v=='1':Node(s,f'ShapeCell_{x}_{y}',root,(ox+x*block,oy-y*block),(block-2,block-2)).image(INK)
            Node(s,'Shape Name',root,(0,-36 if idx==2 else -43),(width,24)).text(shape['name'],font=20,c=INK,bold=True)
    else:
        for name,x in [('Rose',-90),('Window',90)]:
            Node(s,name+' Example',bank,(x,18),(42,42)).image((1,1,1,1),False,name)
            Node(s,name+' Label',bank,(x,-28),(150,34)).text('1 '+name,font=24,c=INK,bold=True)
        Node(s,'Plus',bank,(0,10),(35,40)).text('+',font=25,c=INK)
    if idx==2:
        for same,row_y in [(True,-8),(False,-61)]:
            rule_name='Gemini' if same else 'Delta'
            demo=Node(s,rule_name+' Visual Explanation',side,(0,row_y),(470,48));demo.image(PARCH)
            Node(s,'Rule Name',demo,(-150,11),(154,24)).text(rule_name.upper(),font=20,c=INK,bold=True,align=3)
            Node(s,'Meaning ID EN',demo,(-150,-12),(154,24)).text('Bentuk sama' if same else 'Bentuk berbeda','Same shape' if same else 'Different shapes',18,INK,3,True)
            for right in [False,True]:
                form=['11','11'] if same or not right else ['1','1','1']
                mini=Node(s,'Region B' if right else 'Region A',demo,(132 if right else 4,0),(50,40))
                for y,line in enumerate(form):
                    for x,v in enumerate(line):
                        if v=='1':Node(s,f'Example Cell_{x}_{y}',mini,((x-(len(line)-1)/2)*12,((len(form)-1)/2-y)*12),(10,10)).image(PALETTE[0] if right else PALETTE[1])
            Node(s,'Rule Symbol',demo,(69,0),(30,30)).image((1,1,1,1),False,rule_name)
    tool=Node(s,'Selected Tool',side,(0,-107),(470,32)).text('WARNA 1 DIPILIH',font=21,c=INK,align=3,bold=True)
    pal=Node(s,'Palette',side,(0,-148),(470,60));pal.image(PARCH);swatches=[]
    for i,pc in enumerate(PALETTE):
        n=Node(s,f'Color {i+1}',pal,(-199.5+i*57,0),(48,48) if i==0 else (38,38));_,im=n.button(gm,'GridManager','SelectColor',str(i+1),c=pc,arg=i+1,font=19);swatches.append(im)
    Node(s,'Erase Button',side,(-158,-202),(146,42)).button(gm,'GridManager','SelectColor','HAPUS [E]','ERASE [E]',MUTED,arg=0,font=20)
    Node(s,'Undo Button',side,(0,-202),(146,42)).button(gm,'GridManager','Undo','UNDO [Z]','UNDO [Z]',MUTED,font=20)
    Node(s,'Reset Button',side,(158,-202),(146,42)).button(gm,'GridManager','ClearBoard','ULANGI','RESET',MUTED,font=20)
    progress=Node(s,'Progress',side,(0,-243),(470,32)).text(f'0 / {sum(r.count("1") for r in lev["layout"])} KOTAK DIWARNAI',font=21,c=INK,align=3,bold=True)
    Node(s,'Check Button',side,(-122,-290),(226,50)).button(gm,'GridManager','CheckProgress','PERIKSA','CHECK',GOLD)
    skip,_=Node(s,'Skip Level Button',side,(122,-290),(226,50)).button(gm,'GridManager','RequestSkip','LEWATI >','SKIP >',INK)
    messagebar=Node(s,'Status Bar',frame,(0,-302),(836,76));messagebar.image(PAPER)
    status=Node(s,'Validation Status',messagebar,size=(810,70)).text('Pilih warna dan lukis region pada papan.',font=23,c=INK,bold=True)
    nextnode=Node(s,'Next Level Button',c,(480,-386),(520,44),False);nextbutton,_=nextnode.button(gm,'GridManager','NextLevel','LEVEL BERIKUTNYA >','NEXT LEVEL >',GOLD)
    Node(s,'Board Instructions',c,(-285,-379),(880,38)).text('Klik + seret: warnai   |   Klik kanan: hapus   |   1-8: pilih warna','Click + drag: paint   |   Right click: erase   |   1-8: choose color',21,PAPER,bold=True)
    Node(s,'Region Definition',c,(-285,-415),(880,34)).text('Biru tebal = tembok. Celah tipis = masih terhubung.','Thick blue = wall. Thin gap = connected.',21,PAPER,bold=True)
    victory=Node(s,'Victory Overlay',c,(0,-5),(1600,694),False);victory.image((.04,.08,.09,.68),True)
    vp=Node(s,'Victory Card',victory,size=(730,350));vp.image(PAPER)
    Node(s,'Victory Heading',vp,(0,108),(660,58)).text('PUZZLE SELESAI!','PUZZLE COMPLETE!',32,INK,bold=True)
    Node(s,'Victory Message',vp,(0,26),(640,90)).text('Semua aturan terpenuhi.\nTimer masih berjalan; lanjutkan ke level berikutnya.','All rules are satisfied.\nThe timer is still running; continue to the next level.',24,INK,bold=True)
    Node(s,'Continue Button',vp,(120,-98),(365,52)).button(gm,'GridManager','NextLevel','LEVEL BERIKUTNYA >','NEXT LEVEL >')
    Node(s,'View Board Button',vp,(-232,-98),(200,52)).button(hud,'PuzzleHUD','HideVictory','LIHAT PAPAN','VIEW BOARD',MUTED,font=22)
    confirm=Node(s,'Skip Confirmation Overlay',c,(0,-5),(1600,694),active=False);confirm.image((.04,.08,.09,.68),True)
    cp=Node(s,'Skip Card',confirm,size=(730,350));cp.image(PAPER)
    Node(s,'Skip Heading',cp,(0,108),(660,58)).text('LEWATI LEVEL INI?','SKIP THIS LEVEL?',32,INK,bold=True)
    Node(s,'Skip Explanation',cp,(0,22),(640,100)).text('Level ini dicatat sebagai dilewati. Kamu tidak bisa kembali.\nTimer tetap berjalan.','This level will be marked as skipped. You cannot return.\nThe timer keeps running.',24,INK,bold=True)
    Node(s,'Cancel Skip',cp,(-170,-100),(300,52)).button(gm,'GridManager','CancelSkip','LANJUT BERMAIN','KEEP PLAYING',MUTED)
    Node(s,'Confirm Skip',cp,(170,-100),(300,52)).button(gm,'GridManager','ConfirmSkip','YA, LEWATI','YES, SKIP',GOLD)
    s.language(c)
    s.patch(gm,f'  hud: {ref(hud)}\n  validator: {ref(validator)}\n  boardRoot: {ref(board.go)}\n  initialLevel: {idx}\n')
    s.patch(hud,f'  status: {ref(status)}\n  progress: {ref(progress)}\n  toolLabel: {ref(tool)}\n  swatches:\n'+''.join('  - '+ref(v)+'\n' for v in swatches)+f'  victoryPanel: {ref(victory.go)}\n  skipPanel: {ref(confirm.go)}\n  nextButton: {ref(nextbutton)}\n  skipButton: {ref(skip)}\n')
    p=A/f'Scenes/Levels/Level_0{idx+1}.unity';s.write(p);scene_paths.append(p)
    s.preview(ROOT/f'Tools/Previews/Level_0{idx+1}_ID.png');s.preview(ROOT/f'Tools/Previews/Level_0{idx+1}_EN.png',True)
    confirm.active=True
    s.preview(ROOT/f'Tools/Previews/Level_0{idx+1}_Skip_ID.jpg');s.preview(ROOT/f'Tools/Previews/Level_0{idx+1}_Skip_EN.jpg',True)
    confirm.active=False
    victory.active=True
    s.preview(ROOT/f'Tools/Previews/Level_0{idx+1}_Victory_ID.jpg');s.preview(ROOT/f'Tools/Previews/Level_0{idx+1}_Victory_EN.jpg',True)
    victory.active=False
# Fullscreen illustration and a single START button; no menu language/navigation UI.
s=Scene();c=s.base('MenuBackground');m=Node(s,'MainMenuManager');mm=m.component('MainMenuManager')
Node(s,'START',c,(0,-274),(480,150)).button(mm,'MainMenuManager','StartGame','START',c=(1,1,1,1),font=38,sprite='StartButtonPlaque')
p=A/'Scenes/MainMenu/MainMenu_Scene.unity';s.write(p);scene_paths.insert(0,p);s.preview(ROOT/'Tools/Previews/Menu.png')
# Only a distinct full-screen background, GAME OVER and the persistent point total.
s=Scene();c=s.base('GameOverBackground');e=Node(s,'EndScreen');end=e.component('EndScreen')
headline=Node(s,'GAME OVER',c,(0,75),(1350,150)).text('GAME OVER',font=100,c=PAPER,bold=True)
finalscore=Node(s,'Total Points',c,(0,-65),(1350,85)).text('POIN TOTAL:  0',font=50,c=(1,.82,.43,1),bold=True)
s.patch(end,f'  headline: {ref(headline)}\n  finalScore: {ref(finalscore)}\n')
p=A/'Scenes/Results/GameOver_Scene.unity';s.write(p);scene_paths.append(p);s.preview(ROOT/'Tools/Previews/GameOver_Scene.png')
for stale in [A/'Scenes/Results/Results_Scene.unity',A/'Scenes/Results/Results_Scene.unity.meta']:
    if stale.exists():stale.unlink()
# Reusable prefab, with correct script attachment, available for future board edits.
s=Scene();n=Node(s,'CellPrefab',size=(64,64));n.image(PAPER,True,'CellTile');n.component('CellBehavior','  gridX: 0\n  gridY: 0\n');s.write(A/'Scenes/CellPrefab.prefab',True)
# Remove the obsolete single gameplay scene to avoid opening the runtime-built version.
for p in [GAME/'Gameplay_Scene.unity',GAME/'Gameplay_Scene.unity.meta']:
    if p.exists():p.unlink()
# Build starts at Main Menu; each individual scene has a unique, consistent name.
(ROOT/'ProjectSettings/EditorBuildSettings.asset').write_text('%YAML 1.1\n%TAG !u! tag:unity3d.com,2011:\n--- !u!1045 &1\nEditorBuildSettings:\n  m_ObjectHideFlags: 0\n  serializedVersion: 2\n  m_Scenes:\n'+''.join(f'  - enabled: 1\n    path: {p.relative_to(ROOT)}\n    guid: {guid(p)}\n' for p in scene_paths)+'  m_configObjects: {}\n')
for p in sorted(A.rglob('*')):
    if p.is_dir():
        m=Path(str(p)+'.meta')
        if not m.exists():m.write_text(f'fileFormatVersion: 2\nguid: {guid(p)}\nfolderAsset: yes\nDefaultImporter:\n  externalObjects: {{}}\n  userData: \n  assetBundleName: \n  assetBundleVariant: \n')
ps=ROOT/'ProjectSettings/ProjectSettings.asset';v=ps.read_text();v=re.sub(r'  runInBackground: \d+', '  runInBackground: 1',v);v=re.sub(r'  defaultScreenWidth: \d+','  defaultScreenWidth: 1600',v);v=re.sub(r'  defaultScreenHeight: \d+','  defaultScreenHeight: 900',v);ps.write_text(v)
print('Authored:',*[str(p.relative_to(ROOT)) for p in scene_paths],sep='\n')
print('Serialized board cells:',[sum(r.count('1') for r in lev['layout']) for lev in levels])
