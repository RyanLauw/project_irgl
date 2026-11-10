using UnityEngine;
using UnityEngine.UI;

[RequireComponent(typeof(Text))]
public class CompetitionTimer : MonoBehaviour
{
    Text label;
    void Awake()
    {
        label = GetComponent<Text>();
        // A short editable RectTransform must never hide the countdown line.
        label.verticalOverflow = VerticalWrapMode.Overflow;
        label.horizontalOverflow = HorizontalWrapMode.Overflow;
        label.raycastTarget = false;
    }
    void OnEnable() { Refresh(); }
    void Update() { Refresh(); }
    void Refresh()
    {
        if (label == null) label = GetComponent<Text>();
        var session = GameSession.Instance;
        int seconds = session == null ? 600 : Mathf.Clamp(Mathf.CeilToInt((float)session.RemainingSeconds), 0, 600);
        label.text = (seconds / 60).ToString("00") + ":" + (seconds % 60).ToString("00");
        label.color = seconds <= 60 ? new Color(.98f, .42f, .32f) : new Color(.98f, .95f, .87f);
    }
}
