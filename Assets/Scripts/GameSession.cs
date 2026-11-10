using UnityEngine;
using UnityEngine.SceneManagement;

// Editor: one attempt per Play session. Player build: one persistent local attempt.
public class GameSession : MonoBehaviour
{
    public const string AttemptKey = "IRGL.Competition.AttemptUsed";
    public const string ScoreKey = "IRGL.Competition.FinalScore";
    [Header("Shared scoring asset - edit this asset before Start")]
    public ScoreSettings scoring;
    public static GameSession Instance { get; private set; }
    public CompetitionRun Run { get; private set; } = new CompetitionRun();

    bool sessionAttemptUsed;
    int sessionFinalScore;

    public bool HasUsedAttempt
    {
        get { return sessionAttemptUsed; }
    }

    public int FinalScore
    {
        get { return sessionFinalScore; }
    }

    public bool Running { get { return Run.Running; } }
    public int CurrentLevel { get { return Run.CurrentLevel; } }
    public CompetitionRun.FinishReason Reason { get { return Run.Reason; } }
    public int[] Outcomes { get { return Run.Outcomes; } }
    public int SolvedCount { get { return Run.SolvedCount; } }
    public int SkippedCount { get { return Run.SkippedCount; } }
    public double RemainingSeconds { get { return Run.Remaining(Time.realtimeSinceStartupAsDouble); } }
    public static readonly string[] LevelScenes = { "Level_01", "Level_02", "Level_03" };
    bool endScreenLoaded;
    [RuntimeInitializeOnLoadMethod(RuntimeInitializeLoadType.SubsystemRegistration)]
    static void ResetStatic() { Instance = null; }
#if UNITY_EDITOR
    // Also handles Enter Play Mode with Domain Reload / Scene Reload disabled.
    [RuntimeInitializeOnLoadMethod(RuntimeInitializeLoadType.AfterSceneLoad)]
    static void BeginEditorPlaySession()
    {
        if (Instance == null) Instance = Object.FindFirstObjectByType<GameSession>();
        if (Instance != null)
        {
            Instance.Run = new CompetitionRun();
            Instance.sessionAttemptUsed = false;
            Instance.sessionFinalScore = 0;
            Instance.endScreenLoaded = false;
            DontDestroyOnLoad(Instance.gameObject);
        }
        // Stop/Play is a fresh test and always opens the menu in the Editor.
        if (SceneManager.GetActiveScene().name != "MainMenu_Scene")
            SceneManager.LoadScene("MainMenu_Scene");
    }
#endif
    void Awake()
    {
        if (Instance != null && Instance != this) { Destroy(gameObject); return; }
        Instance = this; DontDestroyOnLoad(gameObject); Application.runInBackground = true;
    }
    void OnDestroy() { if (Instance == this) Instance = null; }
    void Update() { CheckDeadline(); }
    public void BeginRun()
    {
        if (Running) return;
        if (HasUsedAttempt) { OpenFinalScreen(); return; }
        if (!Run.Start(Time.realtimeSinceStartupAsDouble, scoring == null ? null : scoring.Snapshot())) return;

        sessionAttemptUsed = true;
        SaveScore();

        // In builds, commits both keys before loading the level.
        endScreenLoaded = false;
        SceneManager.LoadScene(LevelScenes[0]);
    }
    public bool CheckDeadline()
    {
        bool alive = Run.Tick(Time.realtimeSinceStartupAsDouble);
        ShowEndIfNeeded(); return alive;
    }
    public bool MarkSolved(int level)
    {
        bool accepted = Run.Solve(level, Time.realtimeSinceStartupAsDouble);
        if (accepted) SaveScore();
        ShowEndIfNeeded(); return accepted;
    }
    public void Advance(int level, bool skip)
    {
        if (!Run.Advance(level, skip, Time.realtimeSinceStartupAsDouble)) { ShowEndIfNeeded(); return; }
        if (Running) SceneManager.LoadScene(LevelScenes[CurrentLevel]);
        else ShowEndIfNeeded();
    }

    void SaveScore()
    {
        sessionFinalScore = Run.TotalScore;
    }

    void ShowEndIfNeeded()
    {
        if (Running || Reason == CompetitionRun.FinishReason.None || endScreenLoaded) return;
        SaveScore();
        OpenFinalScreen();
    }
    public void OpenFinalScreen()
    {
        endScreenLoaded = true;
        if (SceneManager.GetActiveScene().name != "GameOver_Scene")
            SceneManager.LoadScene("GameOver_Scene");
    }
}
