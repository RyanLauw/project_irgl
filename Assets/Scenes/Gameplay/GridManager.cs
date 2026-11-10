using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;

// All boards and controls are serialized in the scene. Play only binds state/input.
public class GridManager : MonoBehaviour
{
    public static GridManager Instance { get; private set; }
    public PuzzleHUD hud;
    public GridValidator validator;
    public GameObject boardRoot;
    [Range(0, 2)] public int initialLevel;
    public static readonly Color[] Palette = {
        new Color(.90f,.42f,.34f), new Color(.24f,.59f,.72f),
        new Color(.91f,.69f,.28f), new Color(.43f,.69f,.48f),
        new Color(.67f,.49f,.76f), new Color(.90f,.56f,.35f),
        new Color(.38f,.50f,.76f), new Color(.74f,.42f,.55f)
    };
    public LevelData CurrentLevel { get; private set; }
    public int SelectedColor { get; private set; } = 1;
    public int CurrentLevelIndex { get; private set; }
    public bool Completed { get; private set; }
    private LevelData[] levels;
    private CellBehavior[,] cells;
    private readonly Stack<int[,]> undo = new Stack<int[,]>();
    private bool strokeRecorded;

    void Awake() { Instance = this; }
    void OnDestroy() { if (Instance == this) Instance = null; }
    void Start()
    {
        levels = PuzzleLevels.Create();
        if (GameSession.Instance == null || !GameSession.Instance.Running)
        {
            if (GameSession.Instance != null && GameSession.Instance.HasUsedAttempt)
                GameSession.Instance.OpenFinalScreen();
            else SceneManager.LoadScene("MainMenu_Scene");
            return;
        }
        if (GameSession.Instance.CurrentLevel != initialLevel)
        { SceneManager.LoadScene(GameSession.LevelScenes[GameSession.Instance.CurrentLevel]); return; }
        LoadLevel(initialLevel);
    }
    void Update()
    {
        if (GameSession.Instance == null || !GameSession.Instance.Running) return;
        if (hud.skipPanel.activeSelf) { if (Input.GetKeyDown(KeyCode.Escape)) hud.HideSkip(); return; }
        for (int i = 0; i < 8; i++)
            if (Input.GetKeyDown((KeyCode)((int)KeyCode.Alpha1 + i))) SelectColor(i + 1);
        if (Input.GetKeyDown(KeyCode.E)) SelectColor(0);
        if (Input.GetKeyDown(KeyCode.Z)) Undo();
        if (Input.GetKeyDown(KeyCode.Return)) CheckProgress();
        if (Input.GetKeyDown(KeyCode.Escape)) { hud.HideVictory(); hud.HideSkip(); }
        if (!Input.GetMouseButton(0) && !Input.GetMouseButton(1)) strokeRecorded = false;
    }
    public void SelectColor(int id)
    {
        if (id < 0 || id > Palette.Length) return;
        SelectedColor = id;
        hud.RefreshPalette(id);
    }
    public void BeginStroke() { strokeRecorded = false; }
    private int[,] Snapshot()
    {
        var snapshot = new int[validator.columns, validator.rows];
        for (int y=0; y<validator.rows; y++) for (int x=0; x<validator.columns; x++)
            snapshot[x,y] = validator.ColorAt(x,y);
        return snapshot;
    }
    public void PaintCell(int x, int y, bool erase)
    {
        if (Completed || GameSession.Instance == null || !GameSession.Instance.Running || !validator.IsInside(x,y)) return;
        int value = erase ? 0 : SelectedColor;
        if (validator.ColorAt(x,y) == value) return;
        if (!strokeRecorded) { undo.Push(Snapshot()); strokeRecorded = true; }
        validator.Paint(x,y,value);
        cells[x,y].SetVisual(value == 0 ? PuzzleHUD.Paper : Palette[value-1]);
        hud.SetProgress(validator.PaintedCount(), validator.CellCount());
        hud.SetStatus(Localization.Text("Warnai region, lalu tekan PERIKSA.", "Paint the regions, then press CHECK."), false);
    }
    public void Undo()
    {
        if (undo.Count == 0 || Completed) return;
        var snapshot = undo.Pop();
        for (int y=0; y<validator.rows; y++) for (int x=0; x<validator.columns; x++)
        {
            if (cells[x,y] == null) continue;
            int value = snapshot[x,y];
            validator.Paint(x,y,value);
            cells[x,y].SetVisual(value == 0 ? PuzzleHUD.Paper : Palette[value-1]);
        }
        strokeRecorded = false;
        hud.SetProgress(validator.PaintedCount(), validator.CellCount());
        hud.SetStatus(Localization.Text("Satu goresan dibatalkan.", "One stroke undone."), false);
    }
    public void CheckProgress()
    {
        if (GameSession.Instance == null || !GameSession.Instance.CheckDeadline()) return;
        if (Completed) { hud.ShowVictory(); return; }
        string message;
        if (!validator.CheckWinCondition(out message)) { hud.SetStatus(message, false); return; }
        if (!GameSession.Instance.MarkSolved(initialLevel)) return;
        Completed = true;
        if (initialLevel < 2) hud.ShowVictory();
    }
    public void ClearBoard() { if (!Completed) LoadLevel(CurrentLevelIndex); }
    public void NextLevel() { if (Completed) GameSession.Instance.Advance(initialLevel, false); }
    public void RequestSkip() { if (!Completed) hud.ShowSkip(); }
    public void ConfirmSkip() { GameSession.Instance.Advance(initialLevel, true); }
    public void CancelSkip() { hud.HideSkip(); }
    private void LoadLevel(int index)
    {
        if (levels == null) levels = PuzzleLevels.Create();
        if (index < 0 || index >= levels.Length) return;
        CurrentLevelIndex = index;
        CurrentLevel = levels[index];
        Completed = false; undo.Clear(); strokeRecorded = false;
        validator.Initialize(CurrentLevel);
        boardRoot.SetActive(true);
        cells = new CellBehavior[validator.columns, validator.rows];
        foreach (var cell in boardRoot.GetComponentsInChildren<CellBehavior>(true))
        {
            cell.Bind(this);
            cells[cell.gridX,cell.gridY] = cell;
            cell.SetVisual(PuzzleHUD.Paper);
        }
        hud.LoadLevel(index);
        hud.RefreshPalette(SelectedColor);
        hud.SetProgress(0,validator.CellCount());
    }
}
