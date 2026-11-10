using UnityEngine;
using UnityEngine.UI;

[RequireComponent(typeof(Text))]
public class ScoreDisplay : MonoBehaviour
{
    Text label;
    void Awake() { label = GetComponent<Text>(); }
    void Update()
    {
        var session=GameSession.Instance;
        if (session==null) return;
        label.text=Localization.Text("POIN: ","POINTS: ")+session.Run.TotalScore+" / "+session.Run.MaximumScore+
            "    |    "+Localization.Text("LEVEL INI: +","THIS LEVEL: +")+session.Run.PointsForLevel(session.CurrentLevel);
    }
}
