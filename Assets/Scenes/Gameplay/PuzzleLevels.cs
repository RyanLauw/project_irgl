using System;
using UnityEngine;

[Serializable] public struct ShapeData
{
    public string shapeName;
    public string[] shapeLayout;
    public ShapeData(string name, params string[] layout) { shapeName = name; shapeLayout = layout; }
}

[Serializable] public struct SymbolData
{
    public int x, y, kind; // 0 = rose, 1 = window
    public SymbolData(int x, int y, int kind) { this.x = x; this.y = y; this.kind = kind; }
}

[Serializable] public struct WallData
{
    public int x1, y1, x2, y2; // neighbouring cells separated by an inked line
    public WallData(int x1, int y1, int x2, int y2)
    { this.x1 = x1; this.y1 = y1; this.x2 = x2; this.y2 = y2; }
}

[Serializable] public struct EdgeRule
{
    public int x1, y1, x2, y2;
    public bool same; // Gemini = true, Delta = false
    public EdgeRule(int x1, int y1, int x2, int y2, bool same)
    { this.x1 = x1; this.y1 = y1; this.x2 = x2; this.y2 = y2; this.same = same; }
}

[Serializable] public struct LevelData
{
    public string levelName;
    public string[] layout;
    public ShapeData[] targetShapes;
    public SymbolData[] symbols;
    public WallData[] walls;
    public EdgeRule[] rules;
    public bool requirePairs;
}

// Data traced from the three supplied screenshots. Coordinates start at top left.
public static class PuzzleLevels
{
    public static LevelData[] Create()
    {
        return new [] {
            new LevelData {
                levelName = "01 / THE FIRST DRAFT",
                layout = new [] {
                    "00001010000", "01011111010", "11001111111",
                    "01111111110", "11110111100", "01101111100",
                    "01111111110", "00100011100", "00000010000"
                },
                targetShapes = new [] { new ShapeData("Blueprint Cross", "00010", "11111", "01010") },
                symbols = new SymbolData[0], walls = new WallData[0], rules = new EdgeRule[0]
            },
            new LevelData {
                levelName = "02 / ROSE & GLASS",
                layout = new [] {
                    "1111111111", "1111111111", "1111111111", "1111111111",
                    "1111111111", "1111111111", "1111111111", "1111111111"
                },
                targetShapes = new ShapeData[0], requirePairs = true,
                symbols = new [] {
                    new SymbolData(0,1,0), new SymbolData(5,4,0),
                    new SymbolData(6,4,0), new SymbolData(7,5,0),
                    new SymbolData(5,1,1), new SymbolData(7,2,1),
                    new SymbolData(3,5,1), new SymbolData(5,6,1)
                },
                walls = new [] {
                    new WallData(0,1,0,2), new WallData(1,1,1,2),
                    new WallData(5,3,5,4), new WallData(6,3,6,4),
                    new WallData(4,4,5,4), new WallData(5,4,6,4),
                    new WallData(3,4,3,5), new WallData(2,5,3,5),
                    new WallData(5,5,5,6), new WallData(5,6,6,6)
                }, rules = new EdgeRule[0]
            },
            new LevelData {
                levelName = "03 / TWIN PARADOX",
                layout = new [] {
                    "11111111", "11111111", "11111111", "11111111",
                    "11111111", "11111111", "11111111"
                },
                targetShapes = new [] {
                    new ShapeData("Square", "11", "11"),
                    new ShapeData("Trio", "1", "1", "1"),
                    new ShapeData("Quint", "1", "1", "1", "1", "1")
                },
                symbols = new SymbolData[0],
                walls = new [] {
                    new WallData(2,1,2,2), new WallData(3,1,3,2),
                    new WallData(2,3,2,4), new WallData(3,3,3,4),
                    new WallData(1,2,2,2), new WallData(1,3,2,3),
                    new WallData(3,2,4,2), new WallData(3,3,4,3),
                    new WallData(6,1,7,1), new WallData(6,5,7,5)
                },
                rules = new [] {
                    new EdgeRule(2,1,2,2,true), new EdgeRule(3,1,3,2,false),
                    new EdgeRule(2,3,2,4,false), new EdgeRule(3,3,3,4,true)
                }
            }
        };
    }
}
