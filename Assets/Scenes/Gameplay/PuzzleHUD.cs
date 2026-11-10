using UnityEngine;
using UnityEngine.UI;

// Layout, shapes, symbols and bilingual static copy live on the Canvas in each scene.
public class PuzzleHUD : MonoBehaviour
{
    public static readonly Color Paper = new Color(.98f,.95f,.87f);
    public static readonly Color Ink = new Color(.13f,.19f,.20f);
    public Text status, progress, toolLabel;
    public Image[] swatches;
    public GameObject victoryPanel, skipPanel;
    public Button nextButton, skipButton;
    int selected=1, painted, total;
    void OnEnable() { Localization.Changed+=RefreshLanguage; }
    void OnDisable() { Localization.Changed-=RefreshLanguage; }
    void RefreshLanguage()
    {
        SetProgress(painted,total); RefreshPalette(selected);
        SetStatus(Localization.Text("Pilih warna dan lukis region pada papan.","Choose a color and paint regions on the board."),false);
    }
    public void LoadLevel(int index)
    {
        nextButton.gameObject.SetActive(false); skipButton.interactable=true;
        HideVictory(); HideSkip(); RefreshLanguage();
    }
    public void RefreshPalette(int id)
    {
        selected=id;
        for (int i=0;i<swatches.Length;i++) swatches[i].rectTransform.sizeDelta=Vector2.one*(i==id-1?48f:38f);
        toolLabel.text=id==0 ? Localization.Text("PENGHAPUS AKTIF","ERASER SELECTED") : Localization.Text("WARNA ","COLOR ")+id+Localization.Text(" DIPILIH"," SELECTED");
    }
    public void SetProgress(int count,int max)
    { painted=count; total=max; progress.text=count+" / "+max+Localization.Text(" KOTAK DIWARNAI"," CELLS PAINTED"); }
    public void SetStatus(string message,bool success)
    { status.text=message; status.color=success?new Color(.20f,.45f,.31f):Ink; }
    public void ShowVictory()
    {
        nextButton.gameObject.SetActive(true); skipButton.interactable=false;
        SetStatus(Localization.Text("Benar! Semua aturan terpenuhi.","Correct! All rules satisfied."),true);
        HideSkip(); victoryPanel.SetActive(true);
    }
    public void HideVictory() { victoryPanel.SetActive(false); }
    public void ShowSkip() { skipPanel.SetActive(true); }
    public void HideSkip() { skipPanel.SetActive(false); }
}
