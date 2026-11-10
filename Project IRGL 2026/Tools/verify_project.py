"""Static Unity reference checks and independent puzzle solvability verification.
Run with Python 3 + PyYAML. Does not claim to execute Unity or C#.
"""
from pathlib import Path
import re,json,collections,random,yaml
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'Assets'
levels=json.loads((ROOT/'Tools/levels.json').read_text())
def normalize(p):
    a=min(x for x,y in p);b=min(y for x,y in p);return frozenset((x-a,y-b) for x,y in p)
def rotations(rows):
    p={(x,y) for y,row in enumerate(rows) for x,c in enumerate(row) if c=='1'};ans=set()
    for _ in range(4):ans.add(normalize(p));p={(y,-x) for x,y in p}
    return ans
def boundary(a,b):return frozenset((a,b))
def solve(lev):
    B={(x,y) for y,r in enumerate(lev['layout']) for x,c in enumerate(r) if c=='1'}
    walls={boundary((x,y),(nx,ny)) for x,y,nx,ny in lev['walls']}
    if lev['shapes']:
        placements=[]
        for t,shape in enumerate(lev['shapes']):
            for form in rotations(shape['rows']):
                for x,y in [(x,y) for y in range(len(lev["layout"])) for x in range(len(lev["layout"][0]))]:
                    p=frozenset((x+a,y+b) for a,b in form)
                    if p<=B and not any(w<=p for w in walls):placements.append((p,t))
        at={c:[(p,t) for p,t in placements if c in p] for c in B}
        def dfs(left,picked,types):
            if not left:return picked
            c=min(sorted(left),key=lambda c:sum(p<=left for p,t in at[c]))
            for p,t in at[c]:
                if not p<=left:continue
                q=types.copy();q.update((a,t) for a in p)
                if any((x,y) in q and (nx,ny) in q and ((q[x,y]==q[nx,ny])!=same) for x,y,nx,ny,same in lev['rules']):continue
                result=dfs(left-p,picked+[(p,t)],q)
                if result is not None:return result
        result=dfs(B,[],{});assert result is not None
        owner={c:i for i,(p,t) in enumerate(result) for c in p}
    else:
        rng=random.Random(271828)
        roses=[(x,y) for x,y,t in lev['symbols'] if t==0];windows=[(x,y) for x,y,t in lev['symbols'] if t==1]
        def neighbors(c):return [p for p in [(c[0]+1,c[1]),(c[0]-1,c[1]),(c[0],c[1]+1),(c[0],c[1]-1)] if p in B and boundary(c,p) not in walls]
        owner=None
        for attempt in range(5000):
            proposed={};targets=rng.sample(windows,len(windows));order=rng.sample(list(range(4)),4);good=True
            for i in order:
                start=roses[i];goal=targets[i];q=collections.deque([start]);prev={start:None}
                while q:
                    p=q.popleft()
                    if p==goal:break
                    options=neighbors(p);rng.shuffle(options)
                    for nxt in options:
                        if nxt in prev or nxt in proposed or (nxt in roses and nxt!=start) or (nxt in windows and nxt!=goal):continue
                        prev[nxt]=p;q.append(nxt)
                if goal not in prev:good=False;break
                p=goal
                while p is not None:proposed[p]=i;p=prev[p]
            if not good:continue
            q=list(proposed)
            while q:
                p=q.pop(rng.randrange(len(q)))
                for nxt in neighbors(p):
                    if nxt not in proposed:proposed[nxt]=proposed[p];q.append(nxt)
            if len(proposed)==len(B):owner=proposed;break
        assert owner is not None
    # Color region adjacency using the eight available palette colors.
    adjacency={i:set() for i in owner.values()}
    for (x,y),i in owner.items():
        for nxt in [(x+1,y),(x,y+1)]:
            if nxt in owner and owner[nxt]!=i and boundary((x,y),nxt) not in walls:
                adjacency[i].add(owner[nxt]);adjacency[owner[nxt]].add(i)
    colors={}
    for i in sorted(adjacency,key=lambda i:-len(adjacency[i])):
        colors[i]=next(c for c in range(1,9) if c not in [colors.get(n) for n in adjacency[i]])
    rows=[''.join(str(colors[owner[x,y]]) if (x,y) in B else '.' for x in range(len(lev['layout'][0]))) for y in range(len(lev['layout']))]
    return rows

def validate(lev,rows):
    colors={(x,y):int(c) for y,row in enumerate(rows) for x,c in enumerate(row) if c not in '.0'}
    B={(x,y) for y,r in enumerate(lev['layout']) for x,c in enumerate(r) if c=='1'}
    if set(colors)!=B:return False
    walls={boundary((x,y),(nx,ny)) for x,y,nx,ny in lev['walls']};seen={};regions=[]
    for cell in sorted(B):
        if cell in seen:continue
        rid=len(regions);r=set();q=[cell];seen[cell]=rid
        while q:
            p=q.pop();r.add(p)
            for n in [(p[0]+1,p[1]),(p[0]-1,p[1]),(p[0],p[1]+1),(p[0],p[1]-1)]:
                if n in colors and n not in seen and colors[n]==colors[p] and boundary(p,n) not in walls:seen[n]=rid;q.append(n)
        regions.append(r)
    shapes=[rotations(s['rows']) for s in lev['shapes']];matched=[]
    for r in regions:
        found=next((i for i,forms in enumerate(shapes) if normalize(r) in forms),-1);matched.append(found)
        if shapes and found<0:return False
        if lev['symbols'] and any(sum((x,y) in r and t==kind for x,y,t in lev['symbols'])!=1 for kind in [0,1]):return False
    for x,y,nx,ny,same in lev['rules']:
        a,b=seen[x,y],seen[nx,ny]
        if a==b or ((matched[a]==matched[b])!=same):return False
    return True

solutions=[];report=[]
for i,lev in enumerate(levels):
    rows=solve(lev);assert validate(lev,rows);solutions.append(rows)
    assert not validate(lev,['0'*len(r) for r in lev['layout']])
    assert not validate(lev,[''.join('1' if c=='1' else '.' for c in r) for r in lev['layout']])
    report.append(f'Level {i+1}: {sum(r.count("1") for r in lev["layout"])} scene cells; solvable with the 8-color palette; incomplete and all-one-color states rejected.')
(ROOT/'Tools/solutions.json').write_text(json.dumps(solutions,indent=2))
# YAML parse and inspect local/external references including inactive UI.
guids={}
for p in A.rglob('*.meta'):
    m=re.search(r'^guid: (\w+)',p.read_text(),re.M)
    if m:guids[m.group(1)]=Path(str(p)[:-5])
known={'fe87c0e1cc204ed48ad3b37840f39efc','5f7201a12d95ffc409449d95f23cf332','4e29b1a8efbd4b44bb3f3716e73f07ff','0cd44c1031e13a943bb63640046fad76','dc42784cf147c0c48a680349fa168899','76c392e42b5098c458856cdf6ecaaaa1','4f231c4fb786f3946a6b90b886c48677'}
local_guids={p.stem:g for g,p in guids.items() if p.suffix=='.cs'}
scenes=sorted((A/'Scenes/Levels').glob('*.unity'))+sorted((A/'Scenes/MainMenu').glob('*.unity'))+sorted((A/'Scenes/Results').glob('*.unity'))
background_guids=[]
for path in scenes:
    raw=path.read_text();docs={}
    for head,body in re.findall(r'--- !u!\d+ &(\d+)\n(.*?)(?=--- !u!|\Z)',raw,re.S):
        assert int(head) not in docs
        docs[int(head)]=next(iter(yaml.safe_load(body).values()))
    for fid in re.findall(r'\{fileID: (-?\d+)\}',raw):assert int(fid)==0 or int(fid) in docs,(path.name,'missing local',fid)
    for g in re.findall(r'guid: (\w+)',raw):assert g in guids or g in known or g.startswith('0000000000000000'),(path.name,'missing GUID',g)
    for d in docs.values():
        if 'm_MethodName' not in str(d):continue
        for call in d.get('m_OnClick',{}).get('m_PersistentCalls',{}).get('m_Calls',[]):
            target=docs[call['m_Target']['fileID']];script=guids[target['m_Script']['guid']]
            assert re.search(r'public void '+call['m_MethodName']+r'\(',script.read_text()),(path.name,script,call)
            assert call['m_TargetAssemblyTypeName']==script.stem+', Assembly-CSharp'
    for d in docs.values():
        if d.get('m_Script',{}).get('guid')==local_guids['LocalizedText']:
            assert d['Indonesian'] and d['English']
    for k,d in docs.items():
        if 'm_Father' in d and d['m_Father']['fileID']:
            parent=docs[d['m_Father']['fileID']]
            assert {'fileID':k} in parent['m_Children'],(path.name,'parent mismatch',k)
    backgrounds=[d for d in docs.values() if d.get('m_Script',{}).get('guid')==local_guids['FullScreenBackground']]
    assert len(backgrounds)==1
    bg_go=backgrounds[0]['m_GameObject']['fileID']
    bg_images=[d for d in docs.values() if d.get('m_GameObject',{}).get('fileID')==bg_go and d.get('m_Script',{}).get('guid')=='fe87c0e1cc204ed48ad3b37840f39efc']
    assert len(bg_images)==1 and bg_images[0]['m_RaycastTarget']==0
    bg_guid=bg_images[0]['m_Sprite']['guid'];background_guids.append(bg_guid)
    assert guids[bg_guid].parent==A/'Art/Backgrounds'
    buttons=[d for d in docs.values() if d.get('m_Script',{}).get('guid')=='4e29b1a8efbd4b44bb3f3716e73f07ff']
    texts=[d for d in docs.values() if d.get('m_Script',{}).get('guid')=='5f7201a12d95ffc409449d95f23cf332']
    if path.stem=='MainMenu_Scene':
        assert len(buttons)==1 and len(texts)==1 and texts[0]['m_Text']=='START'
        assert buttons[0]['m_OnClick']['m_PersistentCalls']['m_Calls'][0]['m_MethodName']=='StartGame'
        target=docs[buttons[0]['m_TargetGraphic']['fileID']]
        assert guids[target['m_Sprite']['guid']]==A/'Art/UI/StartButtonPlaque.png'
        from PIL import Image
        sprite=Image.open(A/'Art/UI/StartButtonPlaque.png');sprite.load()
        assert sprite.mode=='RGBA' and sprite.getchannel('A').getextrema()==(0,255)
    if path.stem=='GameOver_Scene':
        assert len(buttons)==0 and len(texts)==2
        assert {d['m_Text'] for d in texts}=={'GAME OVER','POIN TOTAL:  0'}
    if path.stem.startswith('Level_'):
        i=int(path.stem[-2:])-1
        named={d['m_Name']:k for k,d in docs.items() if 'm_Component' in d}
        def rect(name):
            go=named[name]
            component=next(d for d in docs.values() if d.get('m_GameObject',{}).get('fileID')==go and 'm_SizeDelta' in d)
            return component
        def bounds(name):
            r=rect(name);x=r['m_AnchoredPosition']['x'];y=r['m_AnchoredPosition']['y'];parent=r['m_Father']['fileID']
            while parent:
                p=docs[parent];x+=p['m_AnchoredPosition']['x'];y+=p['m_AnchoredPosition']['y'];parent=p['m_Father']['fileID']
            w=r['m_SizeDelta']['x'];h=r['m_SizeDelta']['y']
            return x-w/2,y-h/2,x+w/2,y+h/2
        def overlaps(a,b):
            return min(a[2],b[2])>max(a[0],b[0]) and min(a[3],b[3])>max(a[1],b[1])
        timer_go=named['Timer 10 Minutes']
        timer=next(d for d in docs.values() if d.get('m_GameObject',{}).get('fileID')==timer_go and d.get('m_Script',{}).get('guid')=='5f7201a12d95ffc409449d95f23cf332')
        from PIL import ImageFont
        font=ImageFont.truetype(str(A/'TextMesh Pro/Fonts/LiberationSans.ttf'),timer['m_FontData']['m_FontSize'])
        assert rect('Timer 10 Minutes')['m_SizeDelta']['y']>=sum(font.getmetrics())+8
        assert timer['m_FontData']['m_VerticalOverflow']==1 and timer['m_Text']=='10:00'
        assert not overlaps(bounds('Timer Label'),bounds('Timer 10 Minutes'))
        for overlay in ['Skip Confirmation Overlay','Victory Overlay']:
            for information in ['Game Title','Current Score','Timer Label','Timer 10 Minutes','Stage','Board Instructions','Region Definition']:
                assert not overlaps(bounds(overlay),bounds(information)),(path.name,overlay,'covers',information)
        report.append(f'{path.name}: timer line fits its Text box with safe overflow; Skip and Victory overlays do not overlap header/footer Text rectangles.')
        cs=[d for d in docs.values() if d.get('m_Script',{}).get('guid')==local_guids['CellBehavior']]
        actual={(d['gridX'],d['gridY']) for d in cs}
        expected={(x,y) for y,row in enumerate(levels[i]['layout']) for x,c in enumerate(row) if c=='1'}
        assert actual==expected and len(cs)==len(expected)
        # No gameplay return/menu buttons, and only one active board in a scene.
        assert 'm_MethodName: BackToMenu' not in raw and 'm_MethodName: LoadLevel' not in raw
    report.append(f'{path.name}: {sum("m_Name" in d and "m_Component" in d for d in docs.values())} GameObjects; YAML, hierarchy, references, callbacks and bilingual fields valid.')
assert len(background_guids)==5 and len(set(background_guids))==5
assert len({__import__('hashlib').sha256(guids[g].read_bytes()).hexdigest() for g in background_guids})==5
report.append('V6: five distinct fullscreen background Sprites; Main Menu has exactly one START button with an embedded transparent painted plaque Sprite; GameOver has two Text objects and zero buttons.')
# Inspect persistence routing without claiming execution of C# or PlayerPrefs.
session=(A/'Scripts/GameSession.cs').read_text()
# Check both conditional-compilation branches, without executing Unity.
def editor_branch(source,enabled):
    selected=[];stack=[];active=True
    for line in source.splitlines():
        if line.strip()=='#if UNITY_EDITOR':
            stack.append((active,enabled));active=active and enabled
        elif line.strip()=='#else':
            parent,condition=stack[-1];active=parent and not condition
        elif line.strip()=='#endif':
            active=stack.pop()[0]
        elif active:selected.append(line)
    assert not stack
    return '\n'.join(selected)
editor=editor_branch(session,True);player=editor_branch(session,False)
assert 'PlayerPrefs' not in editor and 'BeginEditorPlaySession' in editor
assert 'RuntimeInitializeLoadType.AfterSceneLoad' in editor
assert 'Instance.Run = new CompetitionRun();' in editor
assert 'Instance.editorAttemptUsed = false;' in editor and 'Instance.editorFinalScore = 0;' in editor
assert 'Instance.endScreenLoaded = false;' in editor
assert 'SceneManager.LoadScene("MainMenu_Scene")' in editor
assert 'return editorAttemptUsed;' in editor and 'editorAttemptUsed = true;' in editor
assert 'BeginEditorPlaySession' not in player and 'editorAttemptUsed' not in player
assert 'PlayerPrefs.GetInt(AttemptKey, 0) == 1' in player
begin=session.split('public void BeginRun()')[1].split('public bool CheckDeadline()')[0]
assert begin.index('if (HasUsedAttempt)')<begin.index('Run.Start')
assert begin.index('PlayerPrefs.SetInt(AttemptKey, 1)')<begin.index('SaveScore()')<begin.index('SceneManager.LoadScene')
assert 'PlayerPrefs.Save();' in session and 'if (accepted) SaveScore();' in session
for p in A.rglob('*.cs'):
    if 'Editor' not in p.parts:
        assert 'DeleteKey' not in p.read_text() and 'DeleteAll' not in p.read_text() and 'BackToMenu' not in p.read_text()
assert 'session.HasUsedAttempt' in (A/'Scenes/MainMenu/MainMenuManager.cs').read_text()
assert 'GameSession.Instance.HasUsedAttempt' in (A/'Scenes/Gameplay/GridManager.cs').read_text()
assert 'FinalScore' in (A/'Scripts/EndScreen.cs').read_text()
assert len(re.findall(r'  - enabled: 1', (ROOT/'ProjectSettings/EditorBuildSettings.asset').read_text()))==5
original=ROOT.parents[1]/'revision_v3/IRGL 2026/Assets/Scenes/Gameplay/PuzzleLevels.cs'
if original.exists():assert original.read_bytes()==(A/'Scenes/Gameplay/PuzzleLevels.cs').read_bytes()
timer_script=(A/'Scripts/CompetitionTimer.cs').read_text()
assert 'label.verticalOverflow = VerticalWrapMode.Overflow;' in timer_script
assert 'void OnEnable() { Refresh(); }' in timer_script
report.append('V6 static policy inspection: timer refreshes on enable and preserves overflow; Editor starts a fresh in-memory attempt once per Play; the build retains persistent attempt/score writes and rejects used attempts. No return/restart controls. PlayerPrefs and Editor runtime remain unexecuted.')
# MonoBehaviours have matching class/file names.
for p in A.rglob('*.cs'):
    for cl in re.findall(r'class (\w+)\s*:\s*MonoBehaviour',p.read_text()):assert cl==p.stem,(p,cl)
report.append('No Unity Editor or C# compiler was available: Play Mode, import and actual runtime rendering remain unexecuted.')
print('\n'.join(report));(ROOT/'Docs/STATIC_VERIFICATION.txt').write_text('\n'.join(report)+'\n')
