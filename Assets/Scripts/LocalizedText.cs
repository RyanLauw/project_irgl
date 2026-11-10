using UnityEngine;
using UnityEngine.UI;

[RequireComponent(typeof(Text))]
public class LocalizedText : MonoBehaviour
{
    [TextArea(1, 8)] public string Indonesian;
    [TextArea(1, 8)] public string English;
    [Tooltip("Editor-only preview. Runtime uses the ID / EN button.")]
    public bool previewEnglish;
    void OnValidate()
    { if (!Application.isPlaying) GetComponent<Text>().text = previewEnglish ? English : Indonesian; }
    void OnEnable() { Localization.Changed += Refresh; Refresh(); }
    void OnDisable() { Localization.Changed -= Refresh; }
    public void Refresh() { GetComponent<Text>().text = Localization.Text(Indonesian, English); }
}
