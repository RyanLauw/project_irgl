using UnityEngine;
using UnityEngine.UI;

// Only two text objects on the final Canvas; no restart or navigation controls.
public class EndScreen : MonoBehaviour
{
    public Text headline, finalScore;
    void OnEnable() { Localization.Changed += Refresh; }
    void Start() { Refresh(); }
    void OnDisable() { Localization.Changed -= Refresh; }
    void Refresh()
    {
        headline.text = "GAME OVER";
        int points = GameSession.Instance == null ? 0 : GameSession.Instance.FinalScore;
        finalScore.text = Localization.Text("POIN TOTAL:  ", "TOTAL POINTS:  ") + points;
    }
}
