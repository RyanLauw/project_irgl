using UnityEngine;
using UnityEngine.SceneManagement;
public class MainMenuManager : MonoBehaviour
{
    void Start()
    {
        var session = GameSession.Instance;
        if (session == null) return;
        if (session.Running) SceneManager.LoadScene(GameSession.LevelScenes[session.CurrentLevel]);
        else if (session.HasUsedAttempt) session.OpenFinalScreen();
    }
    public void StartGame() { if (GameSession.Instance != null) GameSession.Instance.BeginRun(); }
}
