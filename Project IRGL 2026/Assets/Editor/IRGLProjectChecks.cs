using System;
using System.IO;
using UnityEditor;
using UnityEditor.SceneManagement;
using UnityEngine;

// Run in Unity via IRGL > Run Project Checks, or -executeMethod IRGLProjectChecks.RunBatch.
public static class IRGLProjectChecks
{
    static int checks;
    static void Check(bool condition,string name)
    { if (!condition) throw new Exception("IRGL check failed: "+name); checks++; }
    [MenuItem("IRGL/Open Main Menu")]
    public static void OpenMenu()
    {
        if (EditorSceneManager.SaveCurrentModifiedScenesIfUserWantsTo())
            EditorSceneManager.OpenScene("Assets/Scenes/MainMenu/MainMenu_Scene.unity");
    }
    [MenuItem("IRGL/Run Project Checks")]
    public static void Run()
    {
        checks=0; CheckSession(); CheckPuzzles();
        foreach (var scene in EditorBuildSettings.scenes) Check(File.Exists(scene.path),"Build scene "+scene.path);
        Debug.Log("IRGL: "+checks+" checks passed. Test mouse input and layout in Play Mode too.");
    }
    public static void RunBatch() { Run(); }
    static void CheckSession()
    {
        var points=new[]{250,350,600};
        var scored=new CompetitionRun(); scored.Start(0,points); points[0]=999;
        Check(scored.MaximumScore==1200 && scored.TotalScore==0,"Score settings snapshot and zero initial points");
        scored.Solve(0,10); scored.Solve(0,11);
        Check(scored.TotalScore==250,"Solved level scores once, repeated Check cannot farm points");
        scored.Advance(0,false,12); scored.Advance(1,true,13);
        Check(scored.TotalScore==250 && scored.EarnedPointsForLevel(1)==0,"Skipped level scores zero");
        scored.Tick(600);
        Check(scored.TotalScore==250,"Timeout retains points already earned");
        scored.Start(1000);
        Check(scored.TotalScore==0 && scored.MaximumScore==1000,"New run resets score and uses default points");
        for(int i=0;i<3;i++) { scored.Solve(i,1001+i*2); if(i<2) scored.Advance(i,false,1002+i*2); }
        Check(scored.TotalScore==1000,"All three default levels score 1000");
        var zero=new CompetitionRun();zero.Start(0);
        for(int i=0;i<3;i++)zero.Advance(i,true,i+1);
        Check(zero.TotalScore==0,"All skips score zero");
        var r=new CompetitionRun();
        Check(!r.Running && r.Remaining(10000)==600,"No timer before Start");
        Check(r.Start(100),"Start accepted");
        Check(!r.Start(130) && r.Remaining(130)==570,"Double Start cannot reset timer");
        Check(!r.Advance(0,false,130),"Unsolved level cannot advance without Skip");
        Check(r.Advance(0,true,150) && r.CurrentLevel==1,"Skip moves to level 2");
        Check(r.Remaining(180)==520,"Timer survives level transition");
        Check(!r.Advance(0,true,180) && r.CurrentLevel==1,"Stale skip cannot jump another level");
        Check(!r.Solve(0,190),"Cannot return to solve skipped level");
        Check(r.Advance(1,true,210),"Skip level 2");
        Check(r.Advance(2,true,250),"Skip level 3");
        Check(!r.Running && r.Reason==CompetitionRun.FinishReason.AllSkipped && r.SkippedCount==3,"All skips trigger GameOver");
        Check(r.Remaining(900)==450,"Clock freezes after run");
        Check(r.Start(1000) && r.SkippedCount==0 && r.CurrentLevel==0 && r.Remaining(1000)==600,"New run resets state");
        Check(r.Tick(1599.99),"Not expired before deadline");
        Check(!r.Solve(0,1600) && r.Reason==CompetitionRun.FinishReason.TimeExpired,"Deadline takes priority over solve");
        r=new CompetitionRun(); r.Start(0); r.Solve(0,100); r.Advance(0,false,110); r.Advance(1,true,200); r.Advance(2,true,300);
        Check(r.Reason==CompetitionRun.FinishReason.Finished && r.SolvedCount==1 && r.SkippedCount==2,"Mixed result ends the run with retained outcomes");
        r=new CompetitionRun();r.Start(0);
        for (int i=0;i<3;i++) { Check(r.Solve(i,100+i*100),"Solve level "+i); if(i<2) Check(r.Advance(i,false,101+i*100),"Next level "+i); }
        Check(!r.Running && r.SolvedCount==3 && r.Reason==CompetitionRun.FinishReason.Finished,"Three solves end run");
        r=new CompetitionRun();r.Start(0);r.Advance(0,true,20);
        Check(!r.Tick(601) && r.Reason==CompetitionRun.FinishReason.TimeExpired,"Timeout works on level 2 / dialogs");
        r=new CompetitionRun();r.Start(0);r.Advance(0,true,20);r.Advance(1,true,30);
        Check(!r.Advance(2,true,600) && r.Reason==CompetitionRun.FinishReason.TimeExpired,"Timeout wins over last Skip at deadline");
    }
    static void Paint(GridValidator v,string[] rows)
    {
        for (int y=0;y<rows.Length;y++) for (int x=0;x<rows[y].Length;x++)
            if (rows[y][x]!='.') v.Paint(x,y,rows[y][x]-'0');
    }
    static void CheckPuzzles()
    {
        var go=new GameObject("Temporary IRGL validation");
        go.hideFlags=HideFlags.HideAndDontSave;
        try
        {
            var v=go.AddComponent<GridValidator>();var levels=PuzzleLevels.Create();string reason;
            for (int i=0;i<3;i++)
            {
                v.Initialize(levels[i]);Check(!v.CheckWinCondition(out reason),"Empty puzzle rejected "+i);
                Paint(v,SolutionRows.All[i]);Check(v.CheckWinCondition(out reason),"Known solution accepted "+i);
                for (int y=0;y<v.rows;y++) for(int x=0;x<v.columns;x++) v.Paint(x,y,1);
                Check(!v.CheckWinCondition(out reason),"All-one-color rejected "+i);
            }
            // A chiral shape must allow rotations but reject its mirror.
            var shape=levels[0].targetShapes[0];var rows=shape.shapeLayout;
            for (int rotation=0;rotation<4;rotation++)
            {
                var level=new LevelData {layout=rows,targetShapes=new[]{shape},symbols=new SymbolData[0],walls=new WallData[0],rules=new EdgeRule[0]};
                v.Initialize(level);for(int y=0;y<v.rows;y++) for(int x=0;x<v.columns;x++) if(v.IsInside(x,y))v.Paint(x,y,1);
                Check(v.CheckWinCondition(out reason),"Rotation allowed "+rotation);
                var rotated=new string[rows[0].Length];
                for(int y=0;y<rotated.Length;y++){var line=new char[rows.Length];for(int x=0;x<line.Length;x++)line[x]=rows[rows.Length-1-x][y];rotated[y]=new string(line);} rows=rotated;
            }
            var mirror=new string[shape.shapeLayout.Length];
            for(int y=0;y<mirror.Length;y++){char[] line=shape.shapeLayout[y].ToCharArray();Array.Reverse(line);mirror[y]=new string(line);}
            v.Initialize(new LevelData {layout=mirror,targetShapes=new[]{shape},symbols=new SymbolData[0],walls=new WallData[0],rules=new EdgeRule[0]});
            for(int y=0;y<v.rows;y++) for(int x=0;x<v.columns;x++) if(v.IsInside(x,y))v.Paint(x,y,1);
            Check(!v.CheckWinCondition(out reason),"Reflection rejected");
        }
        finally { UnityEngine.Object.DestroyImmediate(go); }
    }
}
