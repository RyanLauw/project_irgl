using System.Collections.Generic;
using UnityEngine;

public class GridValidator : MonoBehaviour
{
    public static GridValidator Instance;
    public int columns, rows;
    public ShapeData[] targetShapes; // retained for scene compatibility
    private int[,] colors; // -1 = outside, 0 = unpainted, 1..n = player palette
    private LevelData level;
    private HashSet<string> walls;
    private static readonly int[] DX = { 1, -1, 0, 0 };
    private static readonly int[] DY = { 0, 0, 1, -1 };

    void Awake() { Instance = this; }
    void OnDestroy() { if (Instance == this) Instance = null; }
    static string Key(int a, int b, int c, int d)
    {
        if (a > c || (a == c && b > d)) { int t = a; a = c; c = t; t = b; b = d; d = t; }
        return a + "," + b + ":" + c + "," + d;
    }
    public void Initialize(LevelData data)
    {
        level = data; targetShapes = data.targetShapes;
        rows = data.layout.Length; columns = data.layout[0].Length;
        colors = new int[columns, rows]; walls = new HashSet<string>();
        for (int y = 0; y < rows; y++)
            for (int x = 0; x < columns; x++) colors[x,y] = data.layout[y][x] == '1' ? 0 : -1;
        foreach (var wall in data.walls) walls.Add(Key(wall.x1,wall.y1,wall.x2,wall.y2));
    }
    public bool IsInside(int x, int y) { return x >= 0 && y >= 0 && x < columns && y < rows && colors[x,y] >= 0; }
    public void Paint(int x, int y, int color) { if (IsInside(x,y)) colors[x,y] = color; }
    public int ColorAt(int x, int y) { return IsInside(x,y) ? colors[x,y] : -1; }
    public bool HasWall(int x, int y, int nx, int ny) { return walls.Contains(Key(x,y,nx,ny)); }
    public int PaintedCount()
    {
        int n=0; for(int y=0;y<rows;y++) for(int x=0;x<columns;x++) if(colors[x,y]>0) n++;
        return n;
    }
    public int CellCount()
    {
        int n=0; for(int y=0;y<rows;y++) for(int x=0;x<columns;x++) if(colors[x,y]>=0) n++;
        return n;
    }
    public bool CheckWinCondition(out string reason)
    {
        if (PaintedCount() != CellCount()) { reason = Localization.Text("Warnai semua kotak terlebih dahulu.", "Paint every cell first."); return false; }
        int[,] regionIds = new int[columns,rows];
        var regions = new List<List<Vector2Int>>();
        for(int y=0;y<rows;y++) for(int x=0;x<columns;x++)
        {
            if(colors[x,y] <= 0 || regionIds[x,y] != 0) continue;
            var region = new List<Vector2Int>();
            int id = regions.Count+1; var queue = new Queue<Vector2Int>();
            queue.Enqueue(new Vector2Int(x,y)); regionIds[x,y] = id;
            while(queue.Count>0)
            {
                var p = queue.Dequeue(); region.Add(p);
                for(int d=0;d<4;d++)
                {
                    int nx=p.x+DX[d], ny=p.y+DY[d];
                    if(!IsInside(nx,ny) || regionIds[nx,ny]!=0 || colors[nx,ny]!=colors[p.x,p.y] || HasWall(p.x,p.y,nx,ny)) continue;
                    regionIds[nx,ny]=id; queue.Enqueue(new Vector2Int(nx,ny));
                }
            }
            regions.Add(region);
        }
        var matched = new int[regions.Count];
        for(int i=0;i<regions.Count;i++)
        {
            matched[i] = MatchShape(regions[i]);
            if(level.targetShapes.Length>0 && matched[i]<0)
            { reason = Localization.Text("Region ", "Region ") + (i+1) + Localization.Text(" tidak cocok dengan Shape Bank (rotasi boleh).", " does not match the Shape Bank (rotation allowed)."); return false; }
        }
        if(level.requirePairs)
        {
            int[,] counts = new int[regions.Count,2];
            foreach(var symbol in level.symbols) counts[regionIds[symbol.x,symbol.y]-1,symbol.kind]++;
            for(int i=0;i<regions.Count;i++)
                if(counts[i,0]!=1 || counts[i,1]!=1)
                { reason=Localization.Text("Setiap region harus berisi tepat 1 Rose dan 1 Window.", "Each region must contain exactly 1 Rose and 1 Window."); return false; }
        }
        foreach(var rule in level.rules)
        {
            int a=regionIds[rule.x1,rule.y1]-1, b=regionIds[rule.x2,rule.y2]-1;
            if(a==b || a<0 || b<0)
            { reason=Localization.Text("Simbol Gemini/Delta harus menyentuh dua region berbeda.", "Gemini/Delta must touch two distinct regions."); return false; }
            bool identical = matched[a]==matched[b];
            if(identical != rule.same)
            { reason=rule.same ? Localization.Text("Gemini: kedua region harus berbentuk sama.", "Gemini: both regions must have the same shape.") : Localization.Text("Delta: kedua region harus berbentuk berbeda.", "Delta: both regions must have different shapes."); return false; }
        }
        reason=Localization.Text("Semua aturan terpenuhi!", "All rules satisfied!"); return true;
    }
    int MatchShape(List<Vector2Int> cells)
    {
        if(level.targetShapes.Length==0) return -1;
        var rotated=new List<Vector2Int>(cells);
        for(int r=0;r<4;r++)
        {
            int minX=int.MaxValue,minY=int.MaxValue,maxX=int.MinValue,maxY=int.MinValue;
            foreach(var p in rotated) { minX=Mathf.Min(minX,p.x); minY=Mathf.Min(minY,p.y); maxX=Mathf.Max(maxX,p.x); maxY=Mathf.Max(maxY,p.y); }
            int w=maxX-minX+1,h=maxY-minY+1;
            foreach(var shapeIndex in System.Linq.Enumerable.Range(0,level.targetShapes.Length))
            {
                var shape=level.targetShapes[shapeIndex].shapeLayout;
                if(shape.Length!=h || shape[0].Length!=w) continue;
                bool ok=true; var occupied=new HashSet<Vector2Int>();
                foreach(var p in rotated) occupied.Add(new Vector2Int(p.x-minX,p.y-minY));
                for(int y=0;y<h;y++) for(int x=0;x<w;x++)
                    if((shape[y][x]=='1') != occupied.Contains(new Vector2Int(x,y))) ok=false;
                if(ok) return shapeIndex;
            }
            var next=new List<Vector2Int>(); foreach(var p in rotated) next.Add(new Vector2Int(p.y,-p.x));
            rotated=next;
        }
        return -1; // reflection is deliberately disallowed
    }
}
